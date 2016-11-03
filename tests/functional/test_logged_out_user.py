from flask import url_for

from .pages import HomePage, CatagoryPage


def test_logged_out_user(test_app, dummy_catagories, dummy_items):
    # User visits home page and sees list of catagories and items.
    home_page = HomePage(test_app)
    current_page = home_page.visit()
    assert [c.text for c in current_page.catagories] == dummy_catagories
    assert current_page.items == dummy_items

    # User follows link to a catagory.
    catagory = current_page.catagories[0]
    catagory_page = CatagoryPage(test_app, catagory.url)
    current_page = catagory_page.visit()

    # Catagories are still visible.
    assert [c.text for c in current_page.catagories] == dummy_catagories

    # Items are visible for just that catagory.
    items = [i.name for i in dummy_items if i.catagory == catagory.text]
    assert [i.text for i in current_page.items] == items

    # User clicks a link to an item.
    item = items[0]
    current_page = ItemPage(test_app, item.url).visit()

    # The description of the item is visible on the page.
    assert item.description == current_page.description
