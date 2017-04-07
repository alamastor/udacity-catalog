from flask import render_template

from ..app import app
from ..models import Catagory
from ..models import Item


@app.route('/')
def home():
    return render_template('home.html', Catagory=Catagory, Item=Item)
