

from flask import Blueprint, send_file

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/')
def home():
    return send_file('templates/home.html')