from flask import Flask

app = Flask(__name__)

from .views import home
from .db import db
db.init_app(app)
