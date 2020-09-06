from flask import request, json, Blueprint
from . import json_response
from ..models.users import User, UserSchema

user_api = Blueprint('user', __name__)
user_schema = UserSchema


@user_api.route("/user", methods=['POST'])
def sign_up():
    if not request.method == 'POST':
        return json_response({'errorMsg': 'invalid method'}, 405)

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    already_exist_user = User.find_user_by_email(email)
    if already_exist_user:
        return json_response({'errorMsg': 'user already exists'}, 409)

    user = User(
        email=email,
        username=username,
        password=password
    )
    user_uuid = user.save()

    return json_response({'uuid': user_uuid}, 201)

