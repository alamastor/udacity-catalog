from collections import namedtuple

from flask import Response, url_for
import pytest
from bs4 import BeautifulSoup

from app import app
from app.db import db
from app.models.catagory import Catagory
from app.models.item import Item


class CustomResponse(Response):

    @property
    def html(self):
        return BeautifulSoup(self.data.decode('utf-8'), 'html.parser')


def setup_db(scope='session'):
    yield
    os.remove(app.config['DB_FILE'])


@pytest.fixture
def test_db():
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
    test_app.post(url_for('login'))
