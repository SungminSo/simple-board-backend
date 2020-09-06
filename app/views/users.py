from flask import request, Blueprint
from . import json_response
from ..models.users import User, UserSchema
from ..models.logout import Logout
from ..shared.auth import Auth

user_api = Blueprint('user', __name__)
user_schema = UserSchema


@user_api.route("/sign-up", methods=['POST'])
def sign_up():
    if not request.method == 'POST':
        return json_response({'errorMsg': 'invalid method'}, 405)

    try:
        req_data = request.get_json()
        email = req_data['email']
        username = req_data['username']
        password = req_data['password']
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    user_already_exists = User.find_user_by_email(email)
    if user_already_exists:
        return json_response({'errorMsg': 'user already exists'}, 409)

    user = User(
        email=email,
        username=username,
        password=password,
        is_admin=False
    )
    user_uuid = user.save()

    return json_response({'uuid': user_uuid}, 201)


@user_api.route("/log-in", methods=['POST'])
def log_in():
    if not request.method == 'POST':
        return json_response({'errorMsg': 'invalid method'}, 405)

    try:
        req_data = request.get_json()
        email = req_data['email']
        password = req_data['password']
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    if len(email) == 0 or len(password) == 0:
        return json_response({'errorMsg': 'please check your email and password'}, 400)

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
    if not request.method == 'PATCH':
        return json_response({'errorMsg': 'invalid method'}, 405)

    auth_token = request.headers.get('Authorization')
    token = auth_token.split(" ")[1]

    logout = Logout(token)
    logout_at = logout.save()

    return json_response({'logout_at': logout_at}, 200)


