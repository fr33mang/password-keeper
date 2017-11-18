from flask import request, jsonify, redirect

from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from . import jwt_auth

from ..models import User

@jwt_auth.route('/token/auth', methods=['POST'])
def auth():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        resp = jsonify({'access_token': access_token})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

    return jsonify({'msg': "Неверный логин или пароль"}), 401


@jwt_auth.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'access_token': access_token})
    set_access_cookies(resp, access_token)
    return resp, 200

@jwt_auth.route('/token/remove', methods=['POST'])
@jwt_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
