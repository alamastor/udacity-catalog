from flask import url_for

def test_home_page_return_200(test_app):
    res = test_app.get(url_for('home'))
    assert res.status_code == 200
