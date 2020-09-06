from datetime import datetime, timedelta
from flask import json, Response

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
