from flask import url_for


def test_post_without_csrf_returns_403(
    test_app, logged_in, dummy_catagories
):
    res = test_app.post(url_for('create_item'), data={
        'name': 'fork', 'catagory': 'soccer', 'description': 'a description'
    })
    assert res.status_code == 403