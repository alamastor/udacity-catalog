from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('app_key.py')  # load instance/app_key.py
app.config.from_pyfile('google_auth.py')  # load instance/google_auth.py


@app.context_processor
def inject_google_id():
    '''Inject Google ID into every template render.'''
    return dict(google_id=app.config['GOOGLE_CLIENT_ID'])


from .views import home, catagory, item, login, logout
from .db import db
db.init_app(app)