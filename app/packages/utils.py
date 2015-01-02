import requests
from flask import current_app as app
import re


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
    print url
    data = requests.get(url, headers=headers)
    if data.links == {}:
        return len(data.json())

    last_url = data.links['last']['url']
    print last_url
    match = re.match(r'.*page=(?P<no>\d+)', last_url)
    if match is None:
        return len(data.json())

    page = match.groupdict()['no']
    url = github_paginated_url(name, author, string, page)
    data = requests.get(url, headers=headers)
    return (int(page) - 1) * 5 + len(data.json())


def github_data(name, author):
    headers = {
        "Authorization": "token " + app.config.get("API_KEY"),
        "Accept": "application/vnd.github.VERSION.html"
    }

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
