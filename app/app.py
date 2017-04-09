"""Set up app."""

from flask import Flask, session
import warnings

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config') # load config.py
try:
    app.config.from_pyfile('app_key.py')  # load instance/app_key.py
except FileNotFoundError:
    warnings.warn(
        'Running without a secret key, create one with manage.py generate_key.'
    )
try:
    app.config.from_pyfile('google_auth.py')  # load instance/google_auth.py
except FileNotFoundError:
    warnings.warn(
        'Running without Google auth keys. Add GOOGLE_CLIENT_ID and '
        'GOOGLE_SECRET to instance/google_auth.py.'
    )


@app.context_processor
def inject_google_id():
    '''Inject Google ID into every template render.'''
    return {'google_id': app.config['GOOGLE_CLIENT_ID']}


from .views import home, catagory, item, auth, api
from .db import db
db.init_app(app)
from . import csrf