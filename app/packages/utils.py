import requests
from flask import current_app as app


def github_url(name, author):
    return "https://api.github.com/repos/" + author + "/" + name + "/readme"


def get_readme(name, author):
    headers = {
        "Authorization": "token " + app.config.get("API_KEY"),
        "Accept": "application/vnd.github.VERSION.html"
    }
    data = requests.get(github_url(name, author), headers=headers)
    return data.content if data.status_code == requests.codes.ok else ""
