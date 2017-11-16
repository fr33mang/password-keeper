from flask import Blueprint

auth = Blueprint('auth', __name__)
jwt_auth = Blueprint('jwt_auth', __name__)

from . import views, jwt_views
