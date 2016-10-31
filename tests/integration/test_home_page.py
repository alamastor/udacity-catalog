from flask import url_for

from app.models.catagory import Catagory


def test_home_page_returns_200(test_app):
    res = test_app.get(url_for('home'))
    assert res.status_code == 200


def test_home_page_shows_titles(test_app):
    html = test_app.get(url_for('home')).html
    assert 'Catalog App' in html.h1
    assert 'Catagories' in html.find_all('section')[0].h2
    assert 'Latest Items' in html.find_all('section')[1].h2


def test_home_page_shows_catagories(test_app, test_db):
    catagories = [
        'soccer',
        'basketball',
        'baseball',
        'frisbee',
    ]
    for catagory in catagories:
        Catagory.create(catagory)
    html = test_app.get(url_for('home')).html
    catagory_eles = html.find_all('section')[0].ul.find_all('li')
    assert catagories == [e.text for e in catagory_eles]
