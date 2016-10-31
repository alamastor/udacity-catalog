from flask import Response
import pytest
from bs4 import BeautifulSoup

from app import app
from app.db import db
from app.models.catagory import Catagory


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
def dummy_catagories():
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
def dummy_items():
    items = [
        'Stick',
        'Goggles',
        'Snowboard',
        'Shinguards',
        'Frisbee',
        'Bat',
        'Raquette',
        'Helmet',
        'Gloves',
        'Net',
        'Ball',
        'Disk',
        'Boots',
        'Sock'
    ]
    return items
