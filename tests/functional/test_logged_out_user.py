from flask import url_for

from .pages import HomePage


def test_logged_out_user(test_app, dummy_catagories, dummy_items):
    # User visits home page and sees list of catagories and items
    home_page = HomePage(test_app)
    home_page.visit()
    assert home_page.catagories == dummy_catagories
    assert home_page.items == dummy_items[-10:]
