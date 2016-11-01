#!/usr/bin/env python3
from flask.ext.script import Manager, Server

from app import app
from app.db import db

manager = Manager(app)

app.config.from_pyfile('../debug_config.py')
manager.add_command('runserver', Server(host='0.0.0.0', use_debugger=True))


@manager.command
def create_tables():
    db.init_app(app)
    db.create_all()


@manager.command
def drop_tables():
    db.drop_tables()


if __name__ == '__main__':
    manager.run()
