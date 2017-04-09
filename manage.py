#!/usr/bin/env python3
"""Executable script for running / managing app. Run to see options."""

import os
import binascii

from flask_script import Manager, Server, prompt_bool

from app import app
from app.db import db
from app.models.item import Item
from app.models.catagory import Catagory


manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def create_tables():
    """Initial database setup."""
    db.init_app(app)
    db.create_all()


@manager.command
def populate():
    """Populate database with dummy data."""
    description = (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer '
        'dignissim arcu vitae placerat vestibulum. Donec nec augue diam. Donec '
        'lobortis laoreet turpis vehicula faucibus. Cras scelerisque consequat '
        'tempus. Maecenas arcu urna, auctor a cursus in, sodales quis dui. Cum '
        'sociis natoque penatibus et magnis dis parturient montes, nascetur '
        'ridiculus mus. Nunc ex ipsum, dapibus sed nunc quis, porta laoreet '
        'neque. Etiam nec fringilla lacus. Ut viverra tincidunt leo id tempor.'
    )
    items = [
        ('ball', 'soccer', description),
        ('stick', 'basketball', description),
        ('goggles', 'soccer', description),
        ('snowboard', 'soccer', description),
        ('shinguards', 'frisbee', description),
        ('frisbee', 'soccer', description),
        ('bat', 'soccer', description),
        ('raquette', 'soccer', description),
        ('helmet', 'soccer', description),
        ('gloves', 'soccer', description),
        ('net', 'soccer', description),
        ('ball', 'basketball', description),
        ('disk', 'soccer', description),
        ('boots', 'soccer', description),
        ('sock', 'soccer', description),
    ]
    for item in items:
        if not Catagory.exists(item[1]):
            catagory = Catagory.create(name=item[1])
        Item.create(item[0], catagory_name=item[1], description=item[2])


@manager.command
def drop_tables():
    """Drop database tables and wipe data."""
    if prompt_bool('Confirm delete all data?'):
        db.drop_all()


@manager.command
def generate_key():
    """Generate a new secret key for the app."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(base_dir, 'instance')):
        os.makedirs(os.path.join(base_dir, 'instance'))
    key_file = os.path.join(base_dir, 'instance', 'app_key.py')
    if not os.path.exists(key_file) or prompt_bool(
        'Secret key already exists, are you sure you want to delete '
        'it and create a new one?'
    ):
        key = binascii.hexlify(os.urandom(32)).decode('utf-8')
        with open(key_file, 'w') as w:
            w.write("SECRET_KEY = '%s'" % key)
        print('created secret key at %s' % key_file)


if __name__ == '__main__':
    manager.run()
