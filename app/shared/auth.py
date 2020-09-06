from datetime import datetime, timedelta
from flask import request, json, Response, g, abort
from functools import wraps
from ..models.users import User
from ..models.logout import Logout

import jwt
import os


class Auth:
    @staticmethod
    def generate_user_token(user_uuid: str, user_email: str) -> dict:
        result = {'data': {}, 'error': {}}
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'email': user_email,
                'uuid': user_uuid
            }

            token = jwt.encode(
                payload=payload,
                key=os.getenv('USER_JWT_SECRET_KEY'),
                algorithm='HS256'
            ).decode('utf-8')

            result['data'] = {'token': token}
            return result
        except Exception:
            result['error'] = {'errorMsg': 'error in generating user token'}
            return result

    @staticmethod
    def decode_user_token(token: str) -> dict:
        result = {'data': {}, 'error': {}}

        try:
            payload = jwt.decode(token, os.getenv('USER_JWT_SECRET_KEY'))
            result['data'] = {'email': payload['email'], 'uuid': payload['uuid']}
            return result
        except jwt.ExpiredSignatureError:
            result['error'] = {'errorMsg': 'token expired'}
            return result
        except jwt.InvalidTokenError:
            result['error'] = {'errorMsg': 'invalid token'}
            return result

    # decorator
    @staticmethod
    def token_required(func):

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401, {'errorMsg': 'authentication token is not available'})

            authorization = request.headers.get('Authorization')
            token = authorization.split(" ")[1]
            data = Auth.decode_user_token(token)
            if data['error']:
                abort(401, data['error'])

            already_logout = Logout.check_logout(token)
            if already_logout:
                abort(401, {'errorMsg': 'already log-out. please log-in again'})

            user_uuid = data['data']['uuid']
            check_user = User.find_user_by_uuid(user_uuid)
            if not check_user:
                abort(401, {'error': 'user does not exist'})
            if check_user.email != data['data']['email']:
                abort(401, {'error': 'wrong email'})

            g.user = {'uuid': user_uuid}
            return func(*args, **kwargs)

        return decorated_auth
