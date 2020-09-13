from flask import request, Blueprint
from sqlalchemy import exc

from . import json_response
from ..models import db
from ..models.users import User
from ..models.logout import Logout
from ..shared.auth import Auth

user_api = Blueprint('user', __name__)


@user_api.route("/sign-up", methods=['POST'])
def sign_up():
    try:
        req_data = request.get_json()
        email = req_data['email']
        username = req_data['username']
        password = req_data['password']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(email) == 0 or len(username) == 0 or len(password) == 0:
            return json_response({'errorMsg': 'please check your email, username and password'}, 400)
    except TypeError:
        return json_response({'errorMsg': 'please check your email, username and password data type'}, 400)

    user_already_exists = User.find_user_by_email(email)
    if user_already_exists:
        return json_response({'errorMsg': 'user already exists'}, 409)

    user = User(
        email=email,
        username=username,
        password=password,
        is_admin=False
    )

    # create a savepoint in case of race condition
    db.session.begin_nested()
    try:
        user_uuid = user.save()
        db.session.commit()
        return json_response({'uuid': user_uuid}, 201)
    except exc.IntegrityError:
        db.session.rollback()
        return json_response({'errorMsg': 'fail to create user'}, 409)


@user_api.route("/log-in", methods=['POST'])
def log_in():
    try:
        req_data = request.get_json()
        email = req_data['email']
        password = req_data['password']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(email) == 0 or len(password) == 0:
            return json_response({'errorMsg': 'please check your email, username and password'}, 400)
    except TypeError:
        return json_response({'errorMsg': 'please check your email, username and password data type'}, 400)

    user = User.find_user_by_email(email)

    if not user:
        return json_response({'errorMsg': 'invalid email'}, 400)

    if not user.check_password(password):
        return json_response({'errorMsg': 'invalid password'}, 400)

    result = Auth.generate_user_token(user.uuid, user.email)
    if not result['data']:
        return json_response(result['error'], 500)
    else:
        return json_response(result['data'], 200)


@user_api.route("/log-out", methods=['PATCH'])
@Auth.token_required
def log_out():
    auth_token = request.headers.get('Authorization')
    token = auth_token.split(" ")[1]

    logout = Logout(token)
    logout_at = logout.save()
    db.session.commit()

    return json_response({'logout_at': logout_at}, 200)
