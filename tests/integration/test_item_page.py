from flask import url_for


def test_item_page_returns_200(test_app, dummy_items):
    res = test_app.get(url_for(
        'item', catagory_name='soccer', item_name='ball'
    ))
    assert res.status_code == 200


def test_item_page_shows_title(test_app, dummy_items):
    res = test_app.get(url_for(
        'item', catagory_name='soccer', item_name='ball'
    ))
    title = res.html.h2.text
    assert title == 'ball'


def test_item_page_shows_description(test_app, dummy_items):
    item = dummy_items[0]
    res = test_app.get(url_for(
        'item', item_name=item.name, catagory_name=item.catagory
    ))
    description = res.html.p.text
    assert description == item.description
