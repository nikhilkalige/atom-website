from flask import Blueprint

packages = Blueprint('packages', __name__)


from . import views, models
from utils import github_data


def post_get_single(result=None, **kw):
    result.update(result.pop("get_json"))
    result.update(github_data(result['name'], result['author'], result['url']))


# runs for search request
def post_get_many(result=None, search_params=None, **kw):
    for item in result["objects"]:
        item.update(item.pop("get_json"))


def search_filter(search_params=None, **kw):
    if (search_params is None) or search_params.get("name") is None:
        return

    def filter_string(name):
        filter = []
        filter.append(dict(name='name',
                           val='%' + name + '%',
                           op='like'
                           )
                      )
        filter.append(dict(name="keywords__name",
                           val=name,
                           op="any"
                           ))
        return filter

    search_params['filters'] = []
    args = search_params['name'].split()
    for item in args:
        search_params['filters'].extend(filter_string(item))

    search_params['disjunction'] = True


def api_creator(apimanager):
    apimanager.create_api(models.Package, primary_key='name', methods=['GET'],
                          include_methods=['get_json'],
                          include_columns=[],
                          postprocessors={
        'GET_SINGLE': [post_get_single],
        'GET_MANY': [post_get_many]
    })
    apimanager.create_api(models.Package, primary_key='name',
                          collection_name='search',
                          methods=['GET'],
                          results_per_page=24,
                          include_methods=['get_json'],
                          include_columns=[],
                          preprocessors={
                              'GET_MANY': [search_filter]
                          },
                          postprocessors={
                              'GET_MANY': [post_get_many]
                          })
