from flask import url_for
from sqlalchemy.orm.exc import NoResultFound
import pytest

from app.models import Item


def test_delete_item_page_401_if_logged_out(test_app, dummy_item):
    res = test_app.get(url_for(
        'delete_item_page',
        item_name=dummy_item.name,
        catagory_name=dummy_item.catagory
    ))
    assert res.status_code == 401


def test_delete_item_page_200(test_app, logged_in, dummy_item):
    res = test_app.get(url_for(
        'delete_item_page',
        item_name=dummy_item.name,
        catagory_name=dummy_item.catagory
    ))
    assert res.status_code == 200


def test_delete_has_form(test_app, logged_in, dummy_item):
    res = test_app.get(url_for(
        'delete_item_page',
        item_name=dummy_item.name,
        catagory_name=dummy_item.catagory
    ))
    assert res.html.find('form', class_='delete-item-form')


def test_logged_out_delete_post_401(test_app, dummy_item, csrf_token):
    res = test_app.post(
        url_for(
            'delete_item_page',
            item_name=dummy_item.name,
            catagory_name=dummy_item.catagory
        ),
        data={'_csrf_token': csrf_token}
    )
    assert res.status_code == 401


def test_delete_redirects(test_app, logged_in, dummy_item, csrf_token):
    res = test_app.post(
        url_for(
            'delete_item_page',
            item_name=dummy_item.name,
            catagory_name=dummy_item.catagory
        ),
        data={'_csrf_token': csrf_token}
    )
    assert res.status_code == 302


def test_delete_redirects_to_home(test_app, logged_in, dummy_item, csrf_token):
    res = test_app.post(
        url_for(
            'delete_item_page',
            item_name=dummy_item.name,
            catagory_name=dummy_item.catagory
        ),
        data={'_csrf_token': csrf_token}
    )
    assert res.location == url_for('home', _external=True)


def test_delete_deletes(test_app, logged_in, dummy_item, csrf_token):
    assert Item.fetch_by_name_and_catagory_name(
        dummy_item.name, dummy_item.catagory
    )
    test_app.post(
        url_for(
            'delete_item_page',
            item_name=dummy_item.name,
            catagory_name=dummy_item.catagory
        ),
        data={'_csrf_token': csrf_token}
    )
    with pytest.raises(NoResultFound):
        Item.fetch_by_name_and_catagory_name(
            dummy_item.name, dummy_item.catagory
        )


def test_delete_non_existant_404(test_app, logged_in, csrf_token):
    res = test_app.post(
        url_for(
            'delete_item_page',
            item_name='fake',
            catagory_name='item'
        ),
        data={'_csrf_token': csrf_token}
    )
    assert res.status_code == 404
