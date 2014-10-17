from . import packages


@packages.route('/')
@packages.route('/index')
def index():
    return "Hello, World!"
