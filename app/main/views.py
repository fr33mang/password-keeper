from flask import render_template, session, redirect, url_for, current_app, \
    request, abort
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db, api, login_manager
from ..models import User, Password
#from ..email import send_email
from . import main
#from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

USER_MARSHALLER = {
    'id': fields.String,
    'username': fields.String,
}

PASSWORD_MARSHALLER = {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "login": fields.String,
    "password": fields.String,
    "url": fields.String,
}

MASTER_PASSWORD_HASH_ARGS = reqparse.RequestParser()
MASTER_PASSWORD_HASH_ARGS.add_argument("master_password_hash")

PASSWORD_POST_ARGS = MASTER_PASSWORD_HASH_ARGS
PASSWORD_POST_ARGS.add_argument("title")
PASSWORD_POST_ARGS.add_argument("description")
PASSWORD_POST_ARGS.add_argument("login")
PASSWORD_POST_ARGS.add_argument("password")
PASSWORD_POST_ARGS.add_argument("url")

PASSWORD_PUT_ARGS = PASSWORD_POST_ARGS
PASSWORD_PUT_ARGS.add_argument("id")

PASSWORD_DELETE_ARGS = reqparse.RequestParser()
PASSWORD_DELETE_ARGS.add_argument("id")

class StorageApi(Resource):
    @jwt_required
    @marshal_with(PASSWORD_MARSHALLER)
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(email=username).first()

        return Password.query.filter_by(owner=user.id).all() 

    @jwt_required
    def post(self):
        master_password_hash = MASTER_PASSWORD_HASH_ARGS.parse_args()["master_password_hash"]

        username = get_jwt_identity()
        user = User.query.filter_by(email=username).first()

        if not user.verify_password(master_password_hash):
            return abort(403, "Invalid master password")

        args = PASSWORD_POST_ARGS.parse_args()

        new_password = Password(
            title= args["title"],
            description =args["description"],
            login = args["login"],
            password = args["password"],
            url = args["url"],
            owner = user.id )

        db.session.add(new_password)
        db.session.commit()

    @jwt_required
    def put(self):
        args = PASSWORD_PUT_ARGS.parse_args()

        changed_password = Password.query.get(args["id"])

        username = get_jwt_identity()
        user = User.query.filter_by(email=username).first()

        if not changed_password:
            return abort(404)

        if changed_password.owner != user.id:
            return abort(403)

        master_password_hash = MASTER_PASSWORD_HASH_ARGS.parse_args()[
            "master_password_hash"]

        if not user.verify_password(master_password_hash):
            return abort(403, "Invalid master password")

        changed_password.title = args["title"]
        changed_password.description = args["description"]
        changed_password.login = args["login"]
        changed_password.password = args["password"]
        changed_password.url = args["url"]  

        db.session.commit()

    @jwt_required
    def delete(self):
        args = PASSWORD_DELETE_ARGS.parse_args()

        username = get_jwt_identity()
        user = User.query.filter_by(email=username).first()

        removed_password = Password.query.get(args["id"])

        if not removed_password:
            return abort(404)

        if removed_password.owner != user.id:
            return abort(403)

        db.session.delete(removed_password)
        db.session.commit()

