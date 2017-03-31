from flask import url_for, session


def test_logout_returns_204(test_app, csrf_token):
    res = test_app.post(url_for('logout'), data={'_csrf_token': csrf_token})
    assert res.status_code == 204
    

def test_logout_removes_logout_from_session(test_app, logged_in, csrf_token):
    res = test_app.post(url_for('logout'), data={'_csrf_token': csrf_token})
    assert not session.get('logged_in', False)