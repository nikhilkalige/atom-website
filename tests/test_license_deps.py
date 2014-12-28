from loader import Load
from app import db
from app.packages.models import *


license_data = [
    "Apache 2",
    "Apache2",
    "MIT",
    {u'url': u'https://github.com/coryroloff/LICENSE', u'name': u'MIT'},
    {u'url': u'https://github.com/coryroloff/LICENSE', u'type': u'MIT'}
]

deps_data = [
    {
        "chai": "^1.9.1",
        "emissary": "^1.0.0",
        "event-kit": "http://github.com/event-kit",
    },
    {
        "chai": "^1.9.1",
        "emissary": "^1.0.0",
        "jquery": "^0.8.1",
    }
]


def test_license(session):
    loader = Load(db.app, session)
    for lic in license_data:
        model = loader.update_license({'license': lic})

    assert License.query.count() == 3
    assert License.query.filter_by(name='Apache-2.0').count() == 1
    assert License.query.filter_by(name='MIT').count() == 2
    assert loader.update_license({}) == None


def test_dependency(session):
    loader = Load(db.app, session)
    assert loader.update_dependencies({}) == []
    assert loader.update_dependencies({'dependencies': []}) == []

    for deps in deps_data:
        model_list = loader.update_dependencies({'dependencies': deps})
        assert len(model_list) == 3

    model = Dependency.query.filter_by(name='event-kit').first()
    assert model.url == 'http://github.com/event-kit'
