from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask_sitemap import Sitemap
import app
import os
import logging
from logging.handlers import RotatingFileHandler

from loader import Load

basedir = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(basedir, "logs")
LOG_FILE = "package_loader.log"
SITEMAP_DIR = os.path.join(basedir, "app/static/sitemap")
SITEMAP_NAME = "sitemap.xml"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

app_instance = app.create_app()

# add logging
formatter = logging.Formatter('%(asctime)s:  %(message)s')
# create directory
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

handler = RotatingFileHandler(
    os.path.join(LOG_DIR, LOG_FILE), maxBytes=512 * 1024, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app_instance.logger.addHandler(handler)


# create context for shell access
def _make_context():
    ctx = app_instance.test_request_context()
    ctx.push()
    from app.packages import models
    return {
        "app": app_instance,
        "db": app.db,
        "models": models
    }

# init flask migrate
migrate = Migrate(app_instance, app.db)

manager = Manager(app_instance)
manager.add_command("runserver", Server())
manager.add_command(
    "shell", Shell(make_context=_make_context, use_ipython=True))
manager.add_command('db', MigrateCommand)
manager.add_command('load', Load(app_instance, app.db.session))
server = Server(host="0.0.0.0", port=9000)


@manager.command
def sitemap():
    app_instance.config["SERVER_NAME"] = "atom.shortcircuits.io"
    sitemap = Sitemap(app=app_instance)

    @app_instance.route('/package/<name>')
    def package(name):
        pass

    @app_instance.route("/")
    def index():
        pass

    @app_instance.route('/search')
    def search():
        pass

    @sitemap.register_generator
    def package_urls():
        import datetime
        from app.packages.models import Package, Downloads

        yield 'index', {}, datetime.datetime.now().isoformat(), "daily", 1
        yield 'search', {}, datetime.datetime.now().isoformat(), "daily", 0.5

        package_list = Package.query.all()
        for item in package_list:
            latest = item.downloads.order_by(Downloads.date.desc()).first()
            time = latest.date.isoformat() if latest is not None else ""
            yield 'package', {'name': item.name}, time, "daily", 0.5

    out = sitemap.sitemap()
    if not os.path.exists(SITEMAP_DIR):
        os.makedirs(SITEMAP_DIR)

    f = open(os.path.join(SITEMAP_DIR, SITEMAP_NAME), 'w')
    f.write(out)
    f.close()

if __name__ == "__main__":
    manager.run()
