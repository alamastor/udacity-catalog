from sqlalchemy.orm.exc import NoResultFound
import pytest

from .pages import (
    HomePage, CreateItemPage, ItemPage, EditItemPage, DeleteItemPage
)
from app.models import Item


def test_edit_item(test_app, dummy_catagories, dummy_items):
    # User visits home page and logs in.
    current_page = HomePage(test_app).visit()
    current_page.login()
    current_page = HomePage(test_app).visit()
    assert current_page.is_logged_in

    # User clicks link to add item.
    current_page = CreateItemPage(
        test_app, current_page.add_item_link.url
    ).visit()

    # User submits add item form and is redirected to the new item's
    # page.
    assert current_page.header.text == 'Add Item'
    current_page.add_item(
        catagory='soccer',
        name='Corner Flag',
        description='A clag for a forner.'
    )
    assert current_page.response.status_code == 302
    current_page = ItemPage(test_app, current_page.response.location).visit()
    assert current_page.header == 'Corner Flag'

    # User decides to edit item.
    edit_item_page = EditItemPage(test_app, current_page.edit_item_link.url)
    current_page = edit_item_page.visit()

    assert current_page.header.text == 'Edit Item'
    assert 'Corner Flag' in current_page.html.decode()
    assert 'A clag for a forner.' in current_page.html.decode()
    assert current_page.html.find('option', selected=True).text == 'soccer'

    # User submits edit item form and is redirected to the item's page.
    current_page.edit_item(
        catagory='soccer',
        name='Corner Flag',
        description='A flag for a corner.'
    )
    assert current_page.response.status_code == 302
    current_page = ItemPage(test_app, current_page.response.location).visit()
    assert current_page.header == 'Corner Flag'
    assert 'A flag for a corner.' in current_page.html.decode()

    # User decides to delete item.
    current_page = delete_item_page = DeleteItemPage(
        test_app, current_page.delete_item_link.url
    ).visit()

    assert current_page.header.text == 'Delete Item'

    # User clicks the confirm delete buttom and is redirected to
    # home page.
    current_page.confirm_delete()
    assert current_page.response.status_code == 302
    current_page = ItemPage(test_app, current_page.response.location).visit()
    sections = current_page.html.find_all('h2')
    assert sections[0].text == 'Catagories'
    assert sections[1].text == 'Latest Items'
    with pytest.raises(NoResultFound):
        Item.fetch_by_name_and_catagory_name('Corner Flag', 'Soccer')
