from flask import request, Blueprint
from . import json_response
from ..models.users import User, UserSchema
from ..shared.auth import Auth

user_api = Blueprint('user', __name__)
user_schema = UserSchema


@user_api.route("/user", methods=['POST'])
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

