from flask import url_for

from .pages import HomePage, CatagoryPage, ItemPage


def test_logged_out_user(test_app, dummy_catagories, dummy_items):
    # User visits home page and sees list of catagories and items.
    home_page = HomePage(test_app)
    current_page = home_page.visit()
    assert [c.text for c in current_page.catagories] == dummy_catagories
    assert current_page.items == [(x.name, x.catagory) for x in dummy_items]

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
    current_page = ItemPage(test_app, current_page.items[0].url).visit()

    # The description of the item is visible on the page.
    assert current_page.description == dummy_items[0].description
