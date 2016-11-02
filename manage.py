#!/usr/bin/env python3
from flask.ext.script import Manager, Server

from app import app
from app.db import db
from app.models.item import Item
from app.models.catagory import Catagory


manager = Manager(app)

app.config.from_pyfile('../debug_config.py')
manager.add_command('runserver', Server(host='0.0.0.0', use_debugger=True))


@manager.command
def create_tables():
    db.init_app(app)
    db.create_all()


@manager.command
def populate():
    items = [
        ('ball', 'soccer'),
        ('stick', 'basketball'),
        ('goggles', 'soccer'),
        ('snowboard', 'soccer'),
        ('shinguards', 'frisbee'),
        ('frisbee', 'soccer'),
        ('bat', 'soccer'),
        ('raquette', 'soccer'),
        ('helmet', 'soccer'),
        ('gloves', 'soccer'),
        ('net', 'soccer'),
        ('ball', 'basketball'),
        ('disk', 'soccer'),
        ('boots', 'soccer'),
        ('sock', 'soccer'),
    ]
    for item in items:
        if Catagory.exists(item[1]):
            Item.create(item[0], catagory_name=item[1])
        else:
            catagory = Catagory.create(name=item[1])
            Item.create(item[0], catagory=catagory)


@manager.command
def drop_tables():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
