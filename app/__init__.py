import os
from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless as flask_restless
from extensions import cache


db = SQLAlchemy()


def create_app(environment='DEVELOPMENT'):
    if os.environ.get("ATOM_SETTINGS") == "PRODUCTION":
        environment = "PRODUCTION"

    app = Flask(__name__)
    app.config.from_object(config[environment])
    db.init_app(app)
    cache.init_app(app)

    from packages import packages
    app.register_blueprint(packages, url_prefix='/api/packages')
    create_restless_api(app)

    # Register views
    register_views(app)
    return app


def create_restless_api(app):
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

    from app.packages import api_creator
    api_creator(manager)


def register_views(app):
    # Serve base html
    from app.views import base_html_renderer
    app.add_url_rule("/", defaults={"path": ""}, methods=["get"], view_func=base_html_renderer)
    app.add_url_rule("/<path:path>", methods=["get"], view_func=base_html_renderer)


from app import views
