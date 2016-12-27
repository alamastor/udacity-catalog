from flask import url_for

from app.models import Item


def test_edit_item_page_401_if_logged_out(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'update_item_page', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.status_code == 401


def test_edit_item_page_200(test_app, dummy_items, logged_in):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'update_item_page', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.status_code == 200


def test_edit_item_page_has_form(test_app, dummy_items, logged_in):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'update_item_page', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.html.find('form', class_='item-form')


def test_post_form_returns_401_logged_out(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.post(url_for(
        'update_item', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.status_code == 401


def test_post_form_redirects(test_app, dummy_items, logged_in):
    item = dummy_items[0]
    res = test_app.post(url_for(
        'update_item', item_name=item.name, catagory_name=item.catagory
    ), data={
        'name': 'fork', 'catagory': 'cake', 'description': 'a descripticon'
    })
    assert res.status_code == 302


def test_post_redirects_to_item_page(test_app, logged_in, dummy_items):
    item = dummy_items[0]
    res = test_app.post(url_for(
        'update_item', item_name=item.name, catagory_name=item.catagory
    ), data={
        'name': 'fork', 'catagory': 'cake', 'description': 'a descripticon'
    })
    assert res.location == url_for(
        'read_item', item_name='fork', catagory_name='cake', _external=True
    )


def test_post_form_updates_item(test_app, dummy_items, logged_in):
    item_tuple = dummy_items[0]
    test_app.post(url_for(
        'update_item',
        item_name=item_tuple.name,
        catagory_name=item_tuple.catagory
    ), data={
        'name': 'fork', 'catagory': 'cake', 'description': 'a new description'
    })
    item = Item.fetch_by_name_and_catagory_name('fork', 'cake')
    assert item.description == 'a new description'


def test_post_page_returns_404_if_items_does_not_exist(
    test_app, logged_in, dummy_catagories
):
    catagory = dummy_catagories[0]
    res = test_app.post(url_for(
        'update_item',
        item_name='non item',
        catagory_name=catagory
    ), data={
        'name': 'fork', 'catagory': 'cake', 'description': 'a new description'
    })
