from flask import Response
import pytest
from bs4 import BeautifulSoup

from app import app


class CustomResponse(Response):

    @property
    def html(self):
        return BeautifulSoup(self.data.decode('utf-8'), 'html.parser')


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.response_class = CustomResponse
    with app.test_client() as client:
        ctx = app.test_request_context()
        ctx.push()
        yield client
    ctx.pop()
