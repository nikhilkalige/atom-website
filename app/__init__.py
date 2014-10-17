from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless as flask_restless

db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config[environment])
    db.init_app(app)

    create_restless_api(app)
    from packages import packages
    app.register_blueprint(packages, url_prefix='/package')
    return app


def create_restless_api(app):
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

    from app.packages.models import Package
    manager.create_api(Package, methods=['GET'])

#app.config.from_object(config)
#db = SQLAlchemy(app)
#from app import views, models


