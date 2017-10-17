from flask import render_template, session, redirect, url_for, current_app, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from .. import db, api
from ..models import User, Password
#from ..email import send_email
from . import main
#from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


password_marshaller = {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "login": fields.String,
    "password": fields.String,
    "url": fields.String,
}

user_marshaller = {
    'id': fields.String,
    'username': fields.String,
}

password_parser = reqparse.RequestParser()
password_parser.add_argument("id")
password_parser.add_argument("title")
password_parser.add_argument("description")
password_parser.add_argument("login")
password_parser.add_argument("password")
password_parser.add_argument("url")

class HelloWorld(Resource):
    def get(self):
        return { hello: "world" }

class User(Resource):
    def get(self, user_id):
        return { 'user': User.query.filter(id=user_id).first() }

class UserList(Resource):
    @marshal_with(user_marshaller)
    def get(self):
        return User.query.all()

class StorageApi(Resource):
    @marshal_with(password_marshaller)
    def get(self, password_id):
        return { 'password': Password.query.filter(id=password_id).first() }

    def post(self):
        args = password_parser.parse_args()
        print(args)

    def put(self, password_id):
        pass

    def delete(self, password_id):
        pass
