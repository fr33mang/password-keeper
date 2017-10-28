from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
#mail = Mail()
moment = Moment()
db = SQLAlchemy()
api = Api()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main.views import StorageApi

    api.add_resource(StorageApi, '/storage')
    api.init_app(app)   

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth
    app.register_blueprint(auth)

    return app
