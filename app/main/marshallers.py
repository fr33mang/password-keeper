
from flask_restful import reqparse, fields


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