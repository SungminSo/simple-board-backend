from flask import request, Blueprint
from . import json_response
from ..models.users import User, UserSchema
from ..shared.auth import Auth

user_api = Blueprint('user', __name__)
user_schema = UserSchema


@user_api.route("/sign-up", methods=['POST'])
def sign_up():
    if not request.method == 'POST':
        return json_response({'errorMsg': 'invalid method'}, 405)

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user_already_exists = User.find_user_by_email(email)
    if user_already_exists:
        return json_response({'errorMsg': 'user already exists'}, 409)

    user = User(
        email=email,
        username=username,
        password=password
    )
    user_uuid = user.save()

    return json_response({'uuid': user_uuid}, 201)


@user_api.route("/log-in", methods=['POST'])
def log_in():
    if not request.method == 'POST':
        return json_response({'errorMsg': 'invalid method'}, 405)

    email = request.form.get('email')
    password = request.form.get('password')

    if len(email) == 0 or len(password) == 0:
        return json_response({'errorMsg': 'please check your email and password'}, 400)

    user = User.find_user_by_email(email)

    if not user:
        return json_response({'errorMsg': 'invalid email'}, 400)

    if not user.check_password(password):
        return json_response({'errorMsg': 'invalid password'}, 400)

    token = Auth.generate_user_token(user.uuid, user.email)

    return json_response({'token': token}, 200)
