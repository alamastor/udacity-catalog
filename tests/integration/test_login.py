from flask import url_for, session


def test_home_page_has_login_form(test_app):
    html = test_app.get(url_for('home')).html
    assert html.find('form', class_='login-form')


def test_post_to_login_page_returns_302(test_app):
    res = test_app.post(url_for('login'))
    assert res.status_code == 302


def test_post_to_login_page_redirects_back(test_app):
    res = test_app.post(
        url_for('login'), headers={'referer': url_for('home')}
    )
    assert res.location == url_for('home', _external=True)


def test_post_to_login_logs_user_in(test_app):
    assert not session.get('logged_in', False)
    res = test_app.post(url_for('login'))
    assert session['logged_in']


def test_logged_in_session_has_logout_form(test_app):
    test_app.post(url_for('login'))
    html = test_app.get(url_for('home')).html
    assert html.find('form', class_='logout-form')
