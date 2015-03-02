import requests
from . import packages
from models import Package, Downloads
from flask import jsonify
from datetime import timedelta
from app import cache
from utils import cache_timeout


@packages.route('/stats', methods=['GET'])
@cache_timeout
@cache.cached()
def stats():
    resp = dict()
    resp["count"] = Package.get_count()
    resp["day"] = Downloads.get_overall_downloads_count(timedelta(days=1))
    resp["week"] = Downloads.get_overall_downloads_count(timedelta(days=7))
    resp["month"] = Downloads.get_overall_downloads_count(timedelta(days=30))
    return jsonify(resp)


@packages.route('/featured', methods=['GET'])
@cache_timeout
@cache.cached()
def featured():
    package_list = requests.get("https://atom.io/api/packages/featured")
    theme_list = requests.get("https://atom.io/api/themes/featured")
    featured_list = package_list.json() + theme_list.json()
    # limit data to multiples of three
    length = ((len(featured_list) + 2) / 3) * 3
    featured_list = featured_list[:(length - 2)]

    json_data = []
    for item in featured_list:
        obj = Package.get_package(item['name'])
        if obj is not None:
            json_data.append(obj.get_json())

    for item in ["docblockr", "git-log"]:
        obj = Package.get_package(item)
        json_data.append(obj.get_json())

    return jsonify(results=json_data)
