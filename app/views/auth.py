"""Auth endpoints."""
from flask import session, request
from oauth2client import client, crypt

from ..app import app


@app.route('/login', methods=['POST'])
def login():
    """Post endpoint to login with Google accounts. Set logged in in session
    and return 204 on success, otherwise return 401.
    """
    token = request.form.get('idtoken')
    if verify_token(token):
        session['logged_in'] = True
        return '', 204
    else:
        return '', 401


def verify_token(token):
    """Verify ID token with Google."""
    try:
        idinfo = client.verify_id_token(token, app.config['GOOGLE_CLIENT_ID'])
        if idinfo['iss'] not in [
            'accounts.google.com',
            'https://accounts.google.com'
        ]:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return False
    return True


@app.route('/logout', methods=['POST'])
def logout():
    """Post endpoint to logout."""
    session['logged_in'] = False
    return '', 204