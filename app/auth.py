from functools import wraps

from flask import session, abort

def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not session.get('logged_in', False):
            abort(401)
        return func(*args, **kwargs)
    return wrapped
