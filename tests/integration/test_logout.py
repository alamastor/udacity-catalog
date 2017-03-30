from flask import url_for, session


def test_logout_returns_204(test_app):
    res = test_app.post(url_for('logout'))
    assert res.status_code == 204
    

def test_logout_removes_logout_from_session(test_app, logged_in):
    res = test_app.post(url_for('logout'))
    assert not session.get('logged_in', False)