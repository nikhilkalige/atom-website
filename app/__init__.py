from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config[environment])
    db = SQLAlchemy(app)
    return app, db

#app.config.from_object(config)
#db = SQLAlchemy(app)

from app import views, models

