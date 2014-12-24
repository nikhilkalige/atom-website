import requests
from . import packages
from models import Package, Downloads
from flask import jsonify
from datetime import timedelta


@packages.route('/stats', methods=['GET'])
def stats():
    resp = dict()
    resp["count"] = Package.get_count()
    resp["day"] = Downloads.get_overall_downloads_count(timedelta(days=1))
    resp["week"] = Downloads.get_overall_downloads_count(timedelta(days=7))
    resp["month"] = Downloads.get_overall_downloads_count(timedelta(days=30))
    return jsonify(resp)


@packages.route('/featured', methods=['GET'])
def featured():
    package_list = requests.get("https://atom.io/api/packages/featured")
    theme_list = requests.get("https://atom.io/api/themes/featured")
    featured_list = package_list.json() + theme_list.json()

    json_data = []
    for item in featured_list:
        obj = Package.get_package(item['name'])
        if obj is not None:
            json_data.append(obj.get_json())

    return jsonify(results=json_data)
