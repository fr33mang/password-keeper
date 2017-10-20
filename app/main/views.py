from flask import render_template, session, redirect, url_for, current_app, \
    request, abort
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_login import login_required, current_user
from .. import db, api, login_manager
from ..models import User, Password
#from ..email import send_email
from . import main
#from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

user_marshaller = {
    'id': fields.String,
    'username': fields.String,
}

class User(Resource):
    def get(self, user_id):
        return { 'user': User.query.filter(id=user_id).first() }

class UserList(Resource):
    @marshal_with(user_marshaller)
    def get(self):
        return User.query.all()


password_marshaller = {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "login": fields.String,
    "password": fields.String,
    "url": fields.String,
}

password_post_args = reqparse.RequestParser()
password_post_args.add_argument("title")
password_post_args.add_argument("description")
password_post_args.add_argument("login")
password_post_args.add_argument("password")
password_post_args.add_argument("url")

password_put_args = password_post_args
password_put_args.add_argument("id")

password_delete_args = reqparse.RequestParser()
password_delete_args.add_argument("id")

class StorageApi(Resource):
    @login_required
    @marshal_with(password_marshaller)
    def get(self):
        return Password.query.filter_by(owner=current_user.id).all() 

    @login_required
    def post(self):
        args = password_post_args.parse_args()

        new_password = Password(
            title= args["title"],
            description =args["description"],
            login = args["login"],
            password = args["password"],
            url = args["url"],
            owner = current_user.id )

        db.session.add(new_password)
        db.session.commit()

    @login_required
    def put(self):
        args = password_put_args.parse_args()

        changed_password = Password.query.get(args["id"])

        if not changed_password:
            return abort(404)

        if changed_password.owner != current_user:
            return abort(403)

        changed_password.title = args["title"]
        changed_password.description = args["description"]
        changed_password.login = args["login"]
        changed_password.password = args["password"]
        changed_password.url = args["url"]

        db.session.commit()

    @login_required
    def delete(self):
        args = password_delete_args.parse_args()

        removed_password = Password.query.get(args["id"])

        if not removed_password:
            return abort(404)

        if removed_password.owner != current_user:
            return abort(403)

        db.session.delete(removed_password)
        db.session.commit()
