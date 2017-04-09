"""CSRF protection code, based on http://flask.pocoo.org/snippets/3/."""
import os
import binascii

from flask import session, request, abort

from .app import app


@app.before_request
def csrf_protect():
    """Before every post request check for and compare CSRF token with token in
    session, then delete token in session so a new one is generate on the next
    page.
    """
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    """Add new CSRF token to session if required, and return it for use in
    HTML form.
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = binascii.hexlify(os.urandom(32)).decode()
    return session['_csrf_token']


@app.context_processor
def inject_csrf_token():
    ""Inject CSRF token function into every template render."""
    return {'csrf_token': generate_csrf_token}