from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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
