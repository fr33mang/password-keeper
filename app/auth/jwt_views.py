from flask import request, jsonify

from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, current_user
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

    return jsonify({'login': False}), 401


# Same thing as login here, except we are only setting a new cookie
# for the access token.
@jwt_auth.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@jwt_auth.route('/token/remove', methods=['POST'])
@jwt_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
