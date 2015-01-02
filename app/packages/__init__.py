from flask import Blueprint

packages = Blueprint('packages', __name__)


from . import views, models
from utils import get_readme


def post_get_single(result=None, **kw):
    result.update(result.pop("get_json"))
    result["readme"] = get_readme(result['name'], result['author'])


# runs for search request
def post_get_many(result=None, search_params=None, **kw):
    for item in result["objects"]:
        item.update(item.pop("get_json"))


def api_creator(apimanager):
    apimanager.create_api(models.Package, primary_key='name', methods=['GET'],
                          include_methods=['get_json'],
                          include_columns=[],
                          postprocessors={
        'GET_SINGLE': [post_get_single],
        'GET_MANY': [post_get_many]
    })

#app = Flask(__name__)


#from flask.ext.sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)
#app.config.from_object('config')
#db = SQLAlchemy(app)

#from app import views, models
