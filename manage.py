from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import users, boards, articles, logout

import os

app = create_app(os.getenv('FLASK_ENV') or 'dev')

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
