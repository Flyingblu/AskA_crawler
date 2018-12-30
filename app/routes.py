from app import flask_app
from app import acrawler
from flask import request


@flask_app.route('/v2/linc/')
def index():
    return acrawler.get_qs(request.args.get('p'))
