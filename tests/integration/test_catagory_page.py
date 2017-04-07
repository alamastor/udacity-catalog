from flask import url_for

def test_catagory_page_returns_200(test_app, dummy_catagories):
    res = test_app.get(url_for('catagory', catagory_name='soccer'))
    assert res.status_code == 200


def test_page_shows_titles(test_app, dummy_catagories):
    html = test_app.get(url_for('catagory', catagory_name='soccer')).html
    assert 'Catalog App' == html.a.text
    assert 'Catagories' == html.find_all('section')[0].h2.text
    assert 'soccer Items' == html.find_all('section')[1].h2.text


def test_catagory_page_shows_catagories(test_app, dummy_catagories):
    html = test_app.get(url_for('catagory', catagory_name='soccer')).html
    catagory_eles = html.find_all('section')[0].ul.find_all('li')
    assert [e.text.strip() for e in catagory_eles] == dummy_catagories



def test_page_shows_items_for_only_that_catagory(test_app, dummy_items):
    dummy_items = [i.name for i in dummy_items if i.catagory == 'soccer']
    html = test_app.get(url_for('catagory', catagory_name='soccer')).html
    lis = html.find_all('section')[1].ul.find_all('li')
    items = [i.text.strip() for i in lis]
    assert items == dummy_items
