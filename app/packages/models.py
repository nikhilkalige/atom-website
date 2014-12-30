from app import db
import datetime
import json


dependencies = db.Table(
    'dependencies',
    db.Column('dependency_id', db.Integer, db.ForeignKey('dependency.id')),
    db.Column('package_id', db.Integer, db.ForeignKey('package.id'))
)


keywords = db.Table(
    'keywords',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id')),
    db.Column('package_id', db.Integer, db.ForeignKey('package.id'))
)


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(50))
    url = db.Column(db.String(140))
    description = db.Column(db.Text())
    stars = db.Column(db.Integer, default=0)
    downloads = db.relationship('Downloads', backref='package', lazy='dynamic')
    version = db.relationship('Version', backref='package', lazy='dynamic')
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'), nullable=True)
    dependencies = db.relationship('Dependency', secondary=dependencies,
        lazy='dynamic', backref=db.backref('packages', lazy='dynamic'))
    keywords = db.relationship('Keyword', secondary=keywords,
        lazy='dynamic', backref=db.backref('packages', lazy='dynamic'))

    def __repr__(self):
        return 'Package: %s' % self.name

    @classmethod
    def get_count(self):
        return Package.query.count()

    @classmethod
    def get_package(self, name):
        return self.query.filter(self.name == name).first()

    def get_json(self):
        json_data = dict()
        # add following parameters to dict
        for label in ['name', 'author', 'url', 'description', 'stars']:
            json_data[label] = getattr(self, label)

        version_obj = self.version.order_by(Version.id.desc()).first()
        version_data = version_obj.get_json()
        downloads_data = Downloads.get_json(self.downloads)
        deps_models = self.dependencies.all()
        keys_models = self.keywords.all()

        json_data['version'] = version_data
        json_data['downloads'] = downloads_data
        json_data['downloads_list'] = Downloads.get_list(self.downloads)
        json_data['license'] = {} if self.license is None else self.license.get_json()
        json_data['dependencies'] = [item.get_json() for item in deps_models]
        json_data['keywords'] = [item.get_json() for item in keys_models]
        return json_data


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)

    def __repr__(self):
        return 'Ver: {} on {}'.format(self.number, self.date)

    def get_json(self):
        json_data = dict()
        json_data['number'] = self.number
        json_data['date'] = self.date.isoformat()

        return json_data


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255))
    package = db.relationship('Package', backref='license', lazy='dynamic')

    def __repr__(self):
        return 'Lic: {} at {}'.format(self.name, self.url)

    def get_json(self):
        json_data = dict()
        json_data['name'] = self.name
        json_data['url'] = self.url

        return json_data


class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255))

    def __repr__(self):
        return 'Dep: {} at {}'.format(self.name, self.url)

    def get_json(self):
        json_data = dict()
        json_data['name'] = self.name
        json_data['url'] = self.url

        return json_data


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Key: {} '.format(self.name)

    def get_json(self):
        return self.name


class DbFlags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    flag = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return 'DbFlags: {} {}'.format(self.date, self.flag)

    @classmethod
    def get_update_time(self):
        return self.query.filter(self.id == 1).first().date


class Downloads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    downloads = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)

    @classmethod
    def nearest_last_entry(self, time):
        last_date = self.query.order_by(False).first().date
        while self.query.filter(self.date == time).count() <= 0:
            if last_date >= time:
                time = last_date
                break
            time -= datetime.timedelta(days=1)

        return time

    @classmethod
    def __count_downloads(self, entries):
        count = 0
        for entry in entries:
            count += entry.downloads

        return count

    # period should be a datetime.timedelta
    @classmethod
    def get_overall_downloads_count(self, period):
        current_time = DbFlags.get_update_time()
        current_entries = self.query.filter(self.date == current_time).all()
        old_time = self.nearest_last_entry(current_time - period)
        old_entries = self.query.filter(self.date == old_time).all()

        current_downloads = self.__count_downloads(current_entries)
        old_downloads = self.__count_downloads(old_entries)
        return current_downloads - old_downloads

    @classmethod
    def get_package_downloads_count(self, query, period):
        current_time = query.first().date
        time = current_time - period
        last_date = query.order_by(False).first().date

        while query.filter(self.date == time).first() is None:
            if last_date >= time:
                time = last_date
                break
            time -= datetime.timedelta(days=1)

        count = query.filter(self.date == time).first().downloads
        return count

    @classmethod
    def get_json(self, query):
        json_data = dict()
        query = query.order_by(self.id.desc())
        json_data['total'] = query.first().downloads
        count = self.get_package_downloads_count(query, datetime.timedelta(days=30))
        json_data['month'] = json_data['total'] - count
        count = self.get_package_downloads_count(query, datetime.timedelta(days=7))
        json_data['week'] = json_data['total'] - count
        count = self.get_package_downloads_count(query, datetime.timedelta(days=1))
        json_data['day'] = json_data['total'] - count

        return json_data

    @classmethod
    def get_list(self, query):
        models = query.order_by(self.id.desc()).limit(50).all()
        return [item.downloads for item in models]
