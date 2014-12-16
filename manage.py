from flask import Flask
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.sqlalchemy import SQLAlchemy
import app
import os
import logging
from logging.handlers import RotatingFileHandler

from loader import Load

basedir = os.path.dirname(__file__)
LOG_FILE = basedir + "/logs/package_loader.log"

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')


#from app.packages import models
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

app_instance = app.create_app("DEVELOPMENT")
# add logging
formatter = logging.Formatter('%(asctime)s:  %(message)s')
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app_instance.logger.addHandler(handler)

manager = Manager(app_instance)
manager.add_command("runserver", Server())
manager.add_command('db', MigrateCommand)
manager.add_command('load', Load(app_instance, app.db))
server = Server(host="0.0.0.0", port=9000)

if __name__ == 	"__main__":
    manager.run()
