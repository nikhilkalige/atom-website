from app import db
import datetime


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(50))
    link = db.Column(db.String(140))
    description = db.Column(db.String())
    downloads = db.relationship('Downloads', backref='package', lazy='dynamic')
    version = db.relationship('Version', backref='package', lazy='dynamic')

    def __repr__(self):
        return 'Package: %s' % self.name

    @classmethod
    def get_count(self):
        return Package.query.count()


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)

    def __repr__(self):
        return 'Ver: {} on {}'.format(self.number, self.date)


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
        while self.query.filter(self.date == time).count() <= 0:
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
    def get_downloads_count(self, period):
        current_time = DbFlags.get_update_time()
        current_entries = self.query.filter(self.date == current_time).all()
        old_time = self.nearest_last_entry(current_time - period)
        old_entries = self.query.filter(self.date == old_time).all()

        current_downloads = self.__count_downloads(current_entries)
        old_downloads = self.__count_downloads(old_entries)
        return current_downloads - old_downloads
