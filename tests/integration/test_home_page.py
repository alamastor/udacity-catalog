from flask import url_for

from app.models.catagory import Catagory
from app.models.item import Item


def test_home_page_returns_200(test_app):
    res = test_app.get(url_for('home'))
    assert res.status_code == 200


def test_home_page_shows_titles(test_app):
    html = test_app.get(url_for('home')).html
    assert 'Catalog App' in html.a
    assert 'Catagories' in html.find_all('section')[0].h2
    assert 'Latest Items' in html.find_all('section')[1].h2


def test_home_page_shows_catagories(test_app, dummy_catagories):
    html = test_app.get(url_for('home')).html
    catagory_eles = html.find_all('section')[0].ul.find_all('li')
    assert [e.text for e in catagory_eles] == dummy_catagories


def test_home_page_shows_items(test_app, dummy_items):
    html = test_app.get(url_for('home')).html
    item_eles = html.find_all('section')[1].ul.find_all('li')
    item_pairs = []
    for pair in item_eles:
        item_pairs.append(tuple(x.strip() for x in pair.text.split('-')))
    assert item_pairs == [(x.name, x.catagory) for x in dummy_items]
