import requests
import re
import datetime
import functools
from flask import current_app as app
from app import cache


def cache_timeout(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        now = datetime.datetime.now()
        deadline = now.replace(hour=23, minute=59)
        period = (deadline - now)
        f.cache_timeout = period.seconds
        return f(*args, **kwargs)

    return decorated_function


def github_url(name, author):
    return "https://api.github.com/repos/" + author + "/" + name


def github_readme(name, author):
    return github_url(name, author) + "/readme"


def github_paginated_url(name, author, string, page=None):
    url = github_url(name, author) + '/' + string + '?' + 'per_page=5'
    if page is not None:
        return url + '&page=' + page

    return url


def get_readme(name, author, headers):
    data = requests.get(github_readme(name, author), headers=headers)
    return data.content if data.status_code == requests.codes.ok else ""


def get_count(name, author, string, headers):
    url = github_paginated_url(name, author, string)
    data = requests.get(url, headers=headers)
    if data.links == {}:
        return len(data.json())

    last_url = data.links['last']['url']
    match = re.match(r'.*page=(?P<no>\d+)', last_url)
    if match is None:
        return len(data.json())

    page = match.groupdict()['no']
    url = github_paginated_url(name, author, string, page)
    data = requests.get(url, headers=headers)
    return (int(page) - 1) * 5 + len(data.json())


@cache_timeout
@cache.memoize()
def github_data(name, author, url):
    headers = {
        "Authorization": "token " + app.config.get("API_KEY"),
        "Accept": "application/vnd.github.VERSION.html"
    }

    if url != "":
        match = re.match(r'.*\/(?P<name>.*)\/', url)
        if match is not None:
            author = match.groupdict()['name']

    json_obj = dict()
    json_obj['readme'] = get_readme(name, author, headers)
    pull_count = get_count(name, author, 'pulls', headers)
    issue_count = get_count(name, author, 'issues', headers)

    json_obj['issues'] = {
        'url': 'https://github.com/' + author + '/' + name + '/issues',
        'count': (issue_count - pull_count)
    }
    json_obj['pull'] = {
        'url': 'https://github.com/' + author + '/' + name + '/pulls',
        'count': pull_count
    }

    return json_obj
