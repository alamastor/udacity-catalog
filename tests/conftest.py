from collections import namedtuple
import os

from flask import Response, url_for
import pytest
from bs4 import BeautifulSoup

from app import app
from app.db import db
from app.models.catagory import Catagory
from app.models.item import Item
from app.csrf import generate_csrf_token


class CustomResponse(Response):

    @property
    def html(self):
        return BeautifulSoup(self.data.decode('utf-8'), 'html.parser')


@pytest.fixture
def setup_db(scope='session'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # In memory db.


@pytest.fixture
def test_db(setup_db):
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture
def test_app(test_db):
    app.config['TESTING'] = True
    app.response_class = CustomResponse
    with app.test_client() as client:
        ctx = app.test_request_context()
        ctx.push()
        yield client
    ctx.pop()


@pytest.fixture
def dummy_catagories(test_db):
    catagories = [
        'soccer',
        'basketball',
        'baseball',
        'frisbee',
    ]
    for catagory in catagories:
        if not Catagory.exists(catagory):
            Catagory.create(catagory)
    return catagories


@pytest.fixture
def dummy_items(test_db):
    ItemTuple = namedtuple('Item', ['name', 'catagory', 'description'])
    items = [
        ItemTuple('ball', 'soccer', 'a soccer ball'),
        ItemTuple('stick', 'basketball', 'a basketball stick'),
        ItemTuple('goggles', 'soccer', ''),
        ItemTuple('snowboard', 'soccer', ''),
        ItemTuple('shinguards', 'frisbee', ''),
        ItemTuple('frisbee', 'soccer', ''),
        ItemTuple('bat', 'soccer', ''),
        ItemTuple('raquette', 'soccer', ''),
        ItemTuple('helmet', 'soccer', ''),
        ItemTuple('gloves', 'soccer', ''),
        ItemTuple('net', 'soccer', ''),
        ItemTuple('ball', 'basketball', ''),
        ItemTuple('disk', 'soccer', ''),
        ItemTuple('boots', 'soccer', ''),
        ItemTuple('sock', 'soccer', ''),
    ]
    for item in items:
        if Catagory.exists(item.catagory):
            Item.create(
                item.name,
                catagory_name=item[1],
                description=item.description
            )
        else:
            catagory = Catagory.create(name=item[1])
            Item.create(
                item.name, catagory=catagory, description=item.description
            )
    return items


@pytest.fixture
def logged_in(test_app):
    with test_app.session_transaction() as sess:
        sess['logged_in'] = True


@pytest.fixture
def dummy_item(dummy_items):
    return dummy_items[0]


@pytest.fixture
def csrf_token(test_app):
    with test_app.session_transaction() as sess:
        token = generate_csrf_token()
        sess['_csrf_token'] = token
    return token