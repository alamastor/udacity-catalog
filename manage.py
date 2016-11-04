#!/usr/bin/env python3
from flask_script import Manager, Server

from app import app
app.config.from_pyfile('../debug_config.py')
from app.db import db
from app.models.item import Item
from app.models.catagory import Catagory


manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', use_debugger=True))


@manager.command
def create_tables():
    db.init_app(app)
    db.create_all()


@manager.command
def populate():
    items = [
        ('ball', 'soccer', DESCRIPTION),
        ('stick', 'basketball', DESCRIPTION),
        ('goggles', 'soccer', DESCRIPTION),
        ('snowboard', 'soccer', DESCRIPTION),
        ('shinguards', 'frisbee', DESCRIPTION),
        ('frisbee', 'soccer', DESCRIPTION),
        ('bat', 'soccer', DESCRIPTION),
        ('raquette', 'soccer', DESCRIPTION),
        ('helmet', 'soccer', DESCRIPTION),
        ('gloves', 'soccer', DESCRIPTION),
        ('net', 'soccer', DESCRIPTION),
        ('ball', 'basketball', DESCRIPTION),
        ('disk', 'soccer', DESCRIPTION),
        ('boots', 'soccer', DESCRIPTION),
        ('sock', 'soccer', DESCRIPTION),
    ]
    for item in items:
        if Catagory.exists(item[1]):
            Item.create(item[0], catagory_name=item[1], description=item[2])
        else:
            catagory = Catagory.create(name=item[1])
            Item.create(item[0], catagory=catagory, description=item[2])


DESCRIPTION = (
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer '
    'dignissim arcu vitae placerat vestibulum. Donec nec augue diam. Donec '
    'lobortis laoreet turpis vehicula faucibus. Cras scelerisque consequat '
    'tempus. Maecenas arcu urna, auctor a cursus in, sodales quis dui. Cum '
    'sociis natoque penatibus et magnis dis parturient montes, nascetur '
    'ridiculus mus. Nunc ex ipsum, dapibus sed nunc quis, porta laoreet '
    'neque. Etiam nec fringilla lacus. Ut viverra tincidunt leo id tempor.'
)


@manager.command
def drop_tables():
    db.drop_all()


if __name__ == '__main__':
    manager.run()