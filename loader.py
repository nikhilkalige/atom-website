from flask.ext.script import Command
from app.packages.models import Package, Downloads, DbFlags
#from app import db
import requests
import datetime
import sys
import traceback
import re
import time

atom_link = "https://atom.io/api/packages?page="



class Load(Command):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.start_time = time.time()
        self.no_of_updates = 0
        self.no_of_packages = 0
        self.new_packages = 0
        self.skipped_packages = 0

    def flag_db(self, status):
        entry = DbFlags.query.filter(DbFlags.id == 1).all()
        if not entry:
            # create a default entry
            entry = DbFlags(date=datetime.date.today(), flag=False)
            self.db.session.add(entry)
            self.db.session.commit()

        # update the entry with status and date
        if status is False:
            entry.date = datetime.date.today()
        entry.flag = status
        self.db.session.commit()

    def run(self):
        i = 1
        self.flag_db(True)
        while True:
            req = requests.get(atom_link + repr(i))
            i = i + 1
            if (req.status_code != requests.codes.ok) or (req.json() == []):
                end_time = time.time()
                lapse = end_time - self.start_time
                self.app.logger.info("\nTotal Pages: %d\n"
                    "Total Packages: %d\n"
                    " Updated : %d\n"
                    " New     : %d\n"
                    " Skipped : %d\n"
                    "Run time: %dm %ds\n",
                    i-1, self.no_of_packages, self.no_of_updates, self.new_packages, self.skipped_packages, lapse/60, lapse%60)
                break

            for value in req.json():
                name = value.get('name')
                self.no_of_packages += 1
                if name is not None and type(name) is dict:
                    name = name.get('name')

                meta = value.get('metadata')
                if meta is None:
                    self.skipped_packages += 1
                    continue

                link = meta.get('repository')
                if link is not None and type(link) is dict:
                    link = link.get('url')

                if meta.get('author') is not None:
                    if type(meta.get('author')) is dict:
                        author = meta.get('author')
                        author = author.get('author') or author.get('name')
                    else:
                        author = meta.get('author')
                elif link is not None:
                    m = re.match(r'^.*com?[:\/](?P<name>.*)/', link)
                    if m is None:
                        # no author so skip
                        self.skipped_packages += 1
                        self.app.logger.error("Author: %s", link)
                        continue
                    author = m.groupdict()['name']
                else:
                    print("author error", name)

                down_no = 0 if value.get('downloads') is None else value.get('downloads')

                query = Package.query.filter_by(name=name).first()
                if query is None:
                    self.new_packages += 1
                    query = Package(name=name,
                                    author=author,
                                    link=link,
                                    description=meta.get('description')
                                    )
                else:
                    self.no_of_updates += 1

                self.db.session.add(query)
                downl_model = Downloads(downloads=down_no, package=query)

                self.db.session.add(downl_model)
                self.db.session.commit()

        # we are done updating db, unflag db
        self.flag_db(False)
