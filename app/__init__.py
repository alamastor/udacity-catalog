from flask import Flask

app = Flask(__name__)

from .views import home
from .views import catagory
from .db import db
db.init_app(app)
