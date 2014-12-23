import requests
from . import packages
from models import Package, Downloads
from flask import jsonify
from datetime import timedelta


@packages.route('/stats', methods=['GET'])
def stats():
    resp = dict()
    resp["count"] = Package.get_count()
    resp["day"] = Downloads.get_downloads_count(timedelta(days=1))
    resp["week"] = Downloads.get_downloads_count(timedelta(days=7))
    resp["month"] = Downloads.get_downloads_count(timedelta(days=30))
    return jsonify(resp)

@packages.route('/featured', methods=['GET'])
def featured():
    package_list = requests.get("https://atom.io/api/packages/featured")
    theme_list = requests.get("https://atom.io/api/themes/featured")
