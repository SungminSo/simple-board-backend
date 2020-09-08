from .. import create_app

import pytest


@pytest.fixture(scope='session')
def flask_app():
    app = create_app('test')
    app.app_context().pust()

    yield app

    app.app_context().pop()


@pytest.fixture(scope='session')
def flask_client(flask_app):
    return flask_app.test_client()
