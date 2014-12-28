import pytest
import json
from app.packages.models import *
from httmock import urlmatch, HTTMock, response
from loader import Load


json_data = []
with open('tests/api_test_data.json', 'r') as f:
    json_data = json.load(f)


# Setup http catch for atom
def atom_mock(test_name):
    global json_data
    content = json.dumps(json_data[test_name])

    @urlmatch(netloc=r'atom.io')
    def request_handler(url, request):
        headers = {'content-type': 'application/json'}
        if url.query == 'page=1':
            return response(200, content, headers, None, 5, request)
        if url.query == 'page=2':
            return response(200, '[]', headers, None, 5, request)
    return request_handler


def test_request_exit(session):
    loader = Load(db.app, session)
    with HTTMock(atom_mock('test1')):
        loader.run()
    assert (loader.i - 1) == 2


def test_meta_missing(session):
    loader = Load(db.app, session)
    with HTTMock(atom_mock('meta_miss')):
        loader.run()
    assert loader.no_of_packages == 1
    assert loader.skipped_packages == 1
    assert loader.no_of_updates == 0
    assert loader.new_packages == 0


def clear_data():
    db.drop_all()
    db.create_all()


def test_loader_first_run(session):
    clear_data()
    loader = Load(db.app, session)
    with HTTMock(atom_mock('first_run')):
        loader.run()

    package = Package.query.first()
    assert package.name == "linter"
    assert package.downloads.order_by(Downloads.id.desc()).first().downloads == 145375
    assert package.stars == 609
    assert package.version.first().number == "0.9.0"
    assert package.dependencies.count() == 3
    assert package.license.name == "MIT"
    return session


def test_loader_second_run(session):
    loader = Load(db.app, session)
    with HTTMock(atom_mock('update_run_1')):
        loader.run()

    package = Package.query.first()
    assert package.name == "linter"
    assert package.downloads.order_by(Downloads.id.desc()).first().downloads == 145999
    assert package.stars == 699
    assert package.version.order_by(Version.id.desc()).first().number == "0.9.2"
    assert package.dependencies.count() == 4
    assert Dependency.query.count() == 4
    assert package.license.name == "Apache-2.0"
    return session


def test_loader_third_run(session):
    loader = Load(db.app, session)
    with HTTMock(atom_mock('update_run_2')):
        loader.run()

    package = Package.query.first()
    assert package.name == "linter"
    assert package.dependencies.count() == 2
    assert Dependency.query.count() == 4
    assert package.license.name == "Apache-2.0"
    assert package.author == "atomlinter"
    return session
