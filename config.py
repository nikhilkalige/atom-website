import os
import ConfigParser


os.environ['PYTHONINSPECT'] = 'True'
basedir = os.path.abspath(os.path.dirname(__file__))
parser = ConfigParser.ConfigParser()
parser.read(os.path.join(basedir, "secret_config.cfg"))


class Default:
    PORT = 8080
    API_KEY = parser.get("github", "api_key")
    CACHE_TYPE = 'memcached'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:' + \
        parser.get("develop", "db_password").strip('"') + \
        '@localhost/atom-website-develop'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:qaswqasw@localhost/atom-website'


class Developement(Default):
    DEBUG = True


class Testing(Default):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:' + \
        parser.get("test", "db_password").strip('"') + '@localhost/atom-website-test'


class Production(Default):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:' + \
        parser.get("production", "db_password").strip('"') + \
        '@localhost/atom'


config = {
    'DEFAULT': Default,
    'DEVELOPMENT': Developement,
    'TESTING': Testing,
    'PRODUCTION': Production
}
