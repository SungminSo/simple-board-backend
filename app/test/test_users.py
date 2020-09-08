from json import dumps
from ..models.users import User


def test_sign_up(client):
    email = 'user1@gmail.com'
    username = 'user1'
    password = 'password'

    # Normal signup process
    resp = client.post('/api/v1/sign-up',
                       dumps({'email': email, 'username': username, 'password': password}))
    assert 201 == resp.status_code

    # Test already existing user's signup
    resp = client.post('/api/v1/sign-up',
                       dumps({'email': email, 'username': username, 'password': password}))
    assert 409 == resp.status_code
