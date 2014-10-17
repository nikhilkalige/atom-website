import os

os.environ['PYTHONINSPECT'] = 'True'
basedir = os.path.abspath(os.path.dirname(__file__))


class Default:
    PORT = 8080
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qaswqasw@localhost/atom-website'


class Developement(Default):
    DEBUG = True

config = {
    'DEFAULT': Default,
    'DEVELOPMENT': Developement
}
