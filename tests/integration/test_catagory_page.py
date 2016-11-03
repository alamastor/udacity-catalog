from flask import url_for

def test_catagory_page_returns_200(test_app, dummy_catagories):
    res = test_app.get(url_for('catagory', catagory='soccer'))
    assert res.status_code == 200


def test_page_shows_titles(test_app):
    html = test_app.get(url_for('catagory', catagory='soccer')).html
    assert 'Catalog App' == html.h1.text
    assert 'Catagories' == html.find_all('section')[0].h2.text
    assert 'soccer Items' == html.find_all('section')[1].h2.text


def test_catagory_page_shows_catagories(test_app, dummy_catagories):
    html = test_app.get(url_for('catagory', catagory='soccer')).html
    catagory_eles = html.find_all('section')[0].ul.find_all('li')
    assert [e.text for e in catagory_eles] == dummy_catagories



def test_page_shows_items_for_only_that_catagory(test_app, dummy_items):
    dummy_items = [i.name for i in dummy_items if i.catagory == 'soccer']
    html = test_app.get(url_for('catagory', catagory='soccer')).html
    items = [i.text for i in html.find_all('section')[1].ul.find_all('li')]
    assert items == dummy_items
