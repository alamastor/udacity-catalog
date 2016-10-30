from flask import url_for

def test_home_page_returns_200(test_app):
    res = test_app.get(url_for('home'))
    assert res.status_code == 200


def test_home_page_shows_titles(test_app):
    html = test_app.get(url_for('home')).html
    assert 'Catalog App' in html.h1
    assert 'Catagories' in html.find_all('section')[0].h2
    assert 'Latest Items' in html.find_all('section')[1].h2
