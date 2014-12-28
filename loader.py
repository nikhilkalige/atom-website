from flask.ext.script import Command
from app.packages.models import Package, Downloads, DbFlags, Version, License, Dependency, Keyword
#from app import db
from urlparse import urlparse
import requests
import datetime
import sys
import traceback
import re
import time
import semantic_version


author_regex = r'^(?P<name>[^<(]+?)?[ \t]*(?:<(?:[^>(]+?)>)?[ \t]*(?:\((?:[^)]+?)\)|$)'
atom_url = "https://atom.io/api/packages?page="
npm_url = "https://www.npmjs.com/package/"
license_url = 'http://opensource.org/licenses/'
license_map = {
    'bsd': 'BSD-2-Clause',
    'mit': 'MIT',
    'x11': 'MIT',
    'mit/x11': 'MIT',
    'apache 2.0': 'Apache-2.0',
    'apache2.0': 'Apache-2.0',
    'apache-2.0': 'Apache-2.0',
    'apachev2.0': 'Apache-2.0',
    'apache2': 'Apache-2.0',
    'apache 2': 'Apache-2.0',
    'apache-2': 'Apache-2.0',
    'apache': 'Apache-2.0',
    'gpl': 'GPL-3.0',
    'gplv3': 'GPL-3.0',
    'gplv2': 'GPL-2.0',
    'gpl3': 'GPL-3.0',
    'gpl2': 'GPL-2.0',
    'lgpl': 'LGPL-2.1',
    'lgplv2.1': 'LGPL-2.1',
    'lgplv2': 'LGPL-2.1'
}


class Load(Command):

    def __init__(self, app, db):
        self.app = app
        self.dbsession = db
        self.start_time = time.time()
        self.no_of_updates = 0
        self.no_of_packages = 0
        self.new_packages = 0
        self.skipped_packages = 0

    def flag_db(self, status):
        entry = DbFlags.query.filter(DbFlags.id == 1).first()
        if not entry:
            # create a default entry
            entry = DbFlags(date=datetime.date.today(), flag=False)
            self.dbsession.add(entry)
            self.dbsession.commit()

        # update the entry with status and date
        if status is False:
            entry.date = datetime.date.today()
        entry.flag = status
        self.dbsession.commit()

    def get_name(self, data):
        name = data.get('name')
        if name is not None and type(name) is dict:
            name = name.get('name')

        return name

    def get_link(self, meta):
        link = meta.get('repository')
        if link is not None and type(link) is dict:
            link = link.get('url')

        return link

    def get_author(self, meta, link):
        if meta.get('author') is not None:
            if type(meta.get('author')) is dict:
                author = meta.get('author')
                author = author.get('author') or author.get('name')
            else:
                author = meta.get('author')
                m = re.match(author_regex, author)
                if m is not None:
                    author = m.groupdict()['name']
        elif link is not None:
            m = re.match(r'^.*com?[:\/](?P<name>.*)/', link)
            if m is None:
                author = None
            author = m.groupdict()['name']
        else:
            print("author error")

        return author

    def update_package(self, package_model, meta, name, license_model, deps_model, keys_model):
        link = self.get_link(meta)
        author = self.get_author(meta, link)
        if author is None:
            self.skipped_packages += 1
            self.app.logger.error("Author: %s", link)
            return None

        if package_model is None:
            self.new_packages += 1
            package_model = Package(name=name)
        else:
            self.no_of_updates += 1

        package_model.author = author
        package_model.url = link
        package_model.description = meta.get('description'),
        package_model.license = license_model
        package_model.dependencies = deps_model
        package_model.keywords = keys_model

        return package_model

    def update_downloads(self, query, data):
        count = data.get('downloads') or 0
        model = Downloads(downloads=count, package=query)
        self.dbsession.add(model)

    def update_version(self, query, meta):
        ver_no = meta.get('version') or '0.0.0'
        sem_ver = semantic_version.Version.coerce(ver_no, partial=True)

        model = query.version.order_by(Version.id.desc()).first()
        if (model is None) or (sem_ver > semantic_version.Version(model.number, partial=True)):
            ver_model = Version(number=str(sem_ver), package=query)
            self.dbsession.add(ver_model)
            return True
        else:
            return False

    def update_license(self, meta):
        url = None
        name = meta.get('license')
        if name is None:
            return None

        if type(name) is dict:
            lic_dict = name
            name = lic_dict.get('name') or lic_dict.get('type')
            url = lic_dict.get('url')

        if url is None:
            name_string = name.replace(" ", "").lower()
            if license_map.get(name_string) is not None:
                name = license_map.get(name_string)
                url = license_url + name

        model = License.query.filter_by(name=name, url=url).first()
        if model is None:
            model = License(name=name, url=url)

        self.dbsession.add(model)
        return model

    def update_dependencies(self, meta):
        deps = meta.get('dependencies')
        if deps is None or type(deps) is not dict:
            return []

        deps_list = []
        for key in deps.keys():
            model = Dependency.query.filter_by(name=key).first()
            if model is None:
                if urlparse(deps.get(key)).scheme != "":
                    url = deps.get(key)
                else:
                    url = npm_url + key

                model = Dependency(name=key, url=url)
                self.dbsession.add(model)

            deps_list.append(model)

        return deps_list

    def update_keywords(self, meta):
        words = meta.get('keywords')
        if type(words) is not list:
            return []

        words_list = []
        for key in words:
            model = Keyword.query.filter_by(name=key).first()
            if model is None:
                model = Keyword(name=key)
                self.dbsession.add(model)

            words_list.append(model)

        return words_list

    def write_log(self, end_time):
        lapse = end_time - self.start_time
        self.app.logger.info(
            "\nTotal Pages: %d\n"
            "Total Packages: %d\n"
            " Updated : %d\n"
            " New     : %d\n"
            " Skipped : %d\n"
            "Run time: %dm %ds\n",
            (self.i - 1), self.no_of_packages, self.no_of_updates,
            self.new_packages, self.skipped_packages, (lapse / 60),
            lapse % 60
        )

    def run(self):
        self.i = 1
        self.flag_db(True)
        while True:
            req = requests.get(atom_url + repr(self.i))
            self.i = self.i + 1
            if (req.status_code != requests.codes.ok) or (req.json() == []):
                self.write_log(time.time())
                break

            for value in req.json():
                name = self.get_name(value)
                self.no_of_packages += 1

                meta = value.get('metadata')
                if meta is None:
                    self.skipped_packages += 1
                    continue

                package_model = Package.query.filter_by(name=name).first()
                if package_model is None or self.update_version(package_model, meta) is True:
                    # update existing or create new package
                    license_model = self.update_license(meta)
                    deps_model = self.update_dependencies(meta)
                    keys_model = self.update_keywords(meta)
                    package_model = self.update_package(package_model, meta, name,
                                                        license_model, deps_model,
                                                        keys_model)
                    self.update_version(package_model, meta)
                    if package_model is None:
                        continue

                package_model.stars = value.get('stargazers_count') or 0
                self.update_downloads(package_model, value)

                self.dbsession.add(package_model)
                self.dbsession.commit()

        # we are done updating db, unflag db
        self.flag_db(False)
