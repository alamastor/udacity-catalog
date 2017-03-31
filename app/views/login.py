from flask import session, request
from oauth2client import client, crypt

from ..app import app


@app.route('/login', methods=['POST'])
def login():
    token = request.form.get('idtoken')
    if verify_token(token):
        session['logged_in'] = True
        return '', 204
    else:
        return '', 401


def verify_token(token):
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