from flask import Flask
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.sqlalchemy import SQLAlchemy
from app import app
import os

from loader import Load

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')


from app import models
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command('db', MigrateCommand)
manager.add_command('load', Load())
server = Server(host="0.0.0.0", port=9000)

if __name__ == 	"__main__":
	manager.run()
