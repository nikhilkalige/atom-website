from flask.ext.script import Command
from app.packages.models import Package, Downloads
#from app import db
import requests
import datetime
import sys
import traceback
import re

atom_link = "https://atom.io/api/packages?page="


class Load(Command):
    def __init__(self, db):
        self.db = db

    def run(self):
        i = 1
        while True:
            req = requests.get(atom_link + repr(i))
            i = i + 1
            if (req.status_code != requests.codes.ok) or (req.json() == []):
                if i is 3:
                    break

            for value in req.json():
                name = value.get('name')
                if name is not None and type(name) is dict:
                    name = name.get('name')

                meta = value.get('metadata')
                if meta is None:
                    continue

                link = meta.get('repository')
                if link is not None and type(link) is dict:
                    link = link.get('url')

                if meta.get('author') is None and link is not None:
                    print(link)
                    m = re.match(r'^.*com?\/(?P<name>.*)/', link)
                    author = m.groupdict()['name']

                elif type(meta.get('author')) is dict:
                    author = meta.get('author')
                    author = author.get('author') or author.get('name')

                else:
                    author = meta.get('author')

                down_no = 0 if value.get('downloads') is None else value.get('downloads')

                query = Package.query.filter_by(name=name).first()
                if query is None:
                    query = Package(name=name,
                                    author=author,
                                    link=link,
                                    description=meta.get('description')
                                    )

                self.db.session.add(query)
                downl_model = Downloads(downloads=down_no, package=query)

                self.db.session.add(downl_model)
                self.db.session.commit()
