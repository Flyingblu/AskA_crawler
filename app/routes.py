from app import flask_app
from app import acrawler


@flask_app.route('/')
@flask_app.route('/index')
def index():
    return acrawler.get_qs()
