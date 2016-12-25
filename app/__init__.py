from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('app_key.py')  # load instance/app_key.py

from .views import home, catagory, item, login, logout
from .db import db
db.init_app(app)
