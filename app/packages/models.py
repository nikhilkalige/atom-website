from app import db
import datetime


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(50))
    link = db.Column(db.String(140))
    description = db.Column(db.String())
    downloads = db.relationship('Downloads', backref='package', lazy='dynamic')

    def __repr__(self):
        return 'Package: %s' % self.name

    @classmethod
    def get_count(self):
        return Package.query.count()


class DbFlags(db.model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    flag = db.Column(db.Boolean, nullable=False)


class Downloads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    downloads = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.date.today, nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
