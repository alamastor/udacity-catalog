import os
import binascii

from flask import session, request, abort

from .app import app


@app.before_request
def csrf_protect():
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = binascii.hexlify(os.urandom(32)).decode()
    return session['_csrf_token']


@app.context_processor
def inject_csrf_token():
    '''Inject CSRF token function into every template render.'''
    return {'csrf_token': generate_csrf_token}