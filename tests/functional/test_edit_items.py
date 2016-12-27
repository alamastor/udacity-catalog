from .pages import HomePage, CreateItemPage, ItemPage, EditItemPage


def test_edit_item(test_app, dummy_catagories, dummy_items):
    # User visits home page and logs in.
    current_page = HomePage(test_app).visit()
    current_page.login()
    assert current_page.response.status_code == 302
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
        catagory='Soccer',
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

    # User submits edit item form and is redirected to the item's page.
    current_page.edit_item(
        catagory='Soccer',
        name='Corner Flag',
        description='A clag for a forner.'
    )
    assert current_page.response.status_code == 302
    current_page = ItemPage(test_app, current_page.response.location).visit()
    assert current_page.header == 'Corner Flag'
