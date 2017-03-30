from flask import url_for, session


def test_home_page_has_login_button(test_app):
    html = test_app.get(url_for('home')).html
    assert html.find('button', class_='g-signin2')


def test_post_to_login_page_returns_204(test_app, mock):
    mock.patch('app.views.login.verify_token', return_value=True)
    res = test_app.post(url_for('login'))
    assert res.status_code == 204


def test_invalid_post_to_login_page_returns_401(test_app, mock):
    mock.patch('app.views.login.verify_token', return_value=False)
    res = test_app.post(url_for('login'))
    assert res.status_code == 401


def test_post_to_login_with_valid_token_logs_user_in(test_app, mock):
    assert not session.get('logged_in', False)
    mock.patch('app.views.login.verify_token', return_value=True)
    res = test_app.post(url_for('login'))
    assert session['logged_in']


def test_post_to_login_with_invalid_token_doesnt_log_user_in(test_app, mock):
    assert not session.get('logged_in', False)
    mock.patch('app.views.login.verify_token', return_value=False)
    res = test_app.post(url_for('login'))
    assert not session.get('logged_in', False)


def test_logged_in_session_has_logout_button(test_app, logged_in):
    html = test_app.get(url_for('home')).html
    assert html.find('button', id='logout-button')