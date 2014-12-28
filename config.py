import os

os.environ['PYTHONINSPECT'] = 'True'
basedir = os.path.abspath(os.path.dirname(__file__))


class Default:
    PORT = 8080
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qaswqasw@localhost/atom-website'


class Developement(Default):
    DEBUG = True


class Testing(Default):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qaswqasw@localhost/atom-website-test'

config = {
    'DEFAULT': Default,
    'DEVELOPMENT': Developement,
    'TESTING': Testing
}
