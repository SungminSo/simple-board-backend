from flask import Flask
from .config import config_by_name

from .models import db, bcrypt

from .views.users import user_api
from .views.boards import board_api


def create_app(config_name: str) -> Flask:
    # app initialization
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # initialize db and bcrypt
    bcrypt.init_app(app)
    db.init_app(app)

    # for health check
    @app.route('/', methods=['GET'])
    def ping():
        return 'pong'

    app.register_blueprint(user_api, url_prefix='/api/v1')
    app.register_blueprint(board_api, url_prefix='/api/v1')

    return app
