from flask import Response
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
    return items
