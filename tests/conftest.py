import pytest

from app import create_app
from app import db as _db


@pytest.yield_fixture(scope='session')
def app(request):
    app = create_app('TESTING')
    # Establish application context
    ctx = app.app_context()
    ctx.push()
    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app, request):
    _db.create_all()
    _db.app = app
    yield _db

    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db, request):
    # connection = db.engine.connect()
    # transaction = connection.begin()

    # options = dict(bind=connection, binds={})
    # session = db.create_scoped_session(options=options)

    # db.session = session
    # yield session

    # transaction.rollback()
    # connection.close()
    # session.remove()
    db.session.begin_nested()
    yield db.session

    db.session.rollback()
