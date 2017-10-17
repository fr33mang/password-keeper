from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import config

bootstrap = Bootstrap()
#mail = Mail()
moment = Moment()
db = SQLAlchemy()
api = Api()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main.views import UserList, StorageApi

    api.add_resource(UserList, '/users')
    api.add_resource(StorageApi, '/storage')
    api.init_app(app)   

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
