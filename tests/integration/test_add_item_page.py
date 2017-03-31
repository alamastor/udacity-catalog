import pytest
from flask import url_for

from app.models import Catagory, Item


def test_logged_out_get_returns_401(test_app):
    res = test_app.get(url_for('create_item_page'))
    assert res.status_code == 401


def test_get_returns_200(test_app, logged_in):
    res = test_app.get(url_for('create_item_page'))
    assert res.status_code == 200


def test_page_has_form(test_app, logged_in):
    res = test_app.get(url_for('create_item_page'))
    assert res.html.find('form', class_='item-form')


def test_form_has_all_catagories_in_form(
    test_app, logged_in, dummy_catagories
):
    catatgories = [c.name for c in Catagory.fetch_all()]
    res = test_app.get(url_for('create_item_page'))
    form = res.html.find('form', class_='item-form')
    options = [o['value'] for o in form.find_all('option')]
    assert options == catatgories


def test_logged_out_post_returns_401(test_app, csrf_token):
    res = test_app.post(
        url_for('create_item'), data={'_csrf_token': csrf_token}
    )
    assert res.status_code == 401


@pytest.mark.usefixtures('dummy_catagories', 'dummy_items')
def test_post_redirects(test_app, logged_in, csrf_token):
    res = test_app.post(url_for('create_item'), data={
        'name': 'fork',
        'catagory': 'soccer',
        'description': 'a descripticon',
        '_csrf_token': csrf_token
    })
    assert res.status_code == 302


@pytest.mark.usefixtures('dummy_catagories', 'dummy_items')
def test_post_redirects_to_item_page(test_app, logged_in, csrf_token):
    res = test_app.post(url_for('create_item'), data={
        'name': 'fork',
        'catagory': 'soccer',
        'description': 'a descripticon',
        '_csrf_token': csrf_token,
    })
    assert res.location == url_for(
        'read_item', item_name='fork', catagory_name='soccer', _external=True
    )


@pytest.mark.usefixtures('dummy_catagories', 'dummy_items')
def test_post_adds_to_db(test_app, logged_in, csrf_token):
    test_app.post(url_for('create_item'), data={
        'name': 'fork', 
        'catagory': 'soccer',
        'description': 'a descripticon',
        '_csrf_token': csrf_token
    })
    item = Item.fetch_by_name_and_catagory_name('fork', 'soccer')
    assert item.description == 'a descripticon'


def test_invalid_name_show_validation_error(test_app, logged_in, csrf_token):
    res = test_app.post(url_for('create_item'), data={
        'name': 'f' * 251,
        'catagory': 'cake',
        'description': 'a descripticon',
        '_csrf_token': csrf_token
    })
    assert res.html.find(class_='error').text


def test_invalid_post_keeps_values_in_input(
    test_app, logged_in, dummy_catagories, csrf_token
):
    res = test_app.post(url_for('create_item'), data={
        'name': 'f' * 251, 
        'catagory': 'soccer',
        'description': 'a description',
        '_csrf_token': csrf_token
    })
    form = res.html.find('form', class_='item-form')
    assert form.find(attrs={'name': 'name'})['value'] == 'f' * 251
    assert form.find(attrs={'name': 'description'}).text == 'a description'
    assert form.find(attrs={'selected': True})['value'] == 'soccer'