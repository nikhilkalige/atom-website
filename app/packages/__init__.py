from flask import Flask


app = Flask(__name__)


from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
#app.config.from_object('config')
#db = SQLAlchemy(app)

from app import views, models