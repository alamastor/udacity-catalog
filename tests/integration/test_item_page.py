from flask import url_for


def test_item_page_returns_200(test_app, dummy_items):
    res = test_app.get(url_for(
        'read_item', catagory_name='soccer', item_name='ball'
    ))
    assert res.status_code == 200


def test_item_page_shows_title(test_app, dummy_items):
    res = test_app.get(url_for(
        'read_item', catagory_name='soccer', item_name='ball'
    ))
    title = res.html.h2.text
    assert title == 'ball'


def test_item_page_shows_description(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    description = res.html.p.text
    assert description == item.description


def test_item_page_shows_catagory(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    catagory = res.html.h3.text
    assert catagory == item.catagory


def test_logged_out_doesnt_have_edit_link(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    assert not res.html.find('a', class_='edit-item')


def test_logged_in_has_edit_link(test_app, dummy_items, logged_in):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.html.find('a', class_='edit-item')


def test_logged_out_doesnt_have_delete_link(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    assert not res.html.find('a', class_='delete-item')


def test_logged_in_has_delete_link(test_app, dummy_items, logged_in):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'read_item', item_name=item.name, catagory_name=item.catagory
    ))
    assert res.html.find('a', class_='delete-item')
