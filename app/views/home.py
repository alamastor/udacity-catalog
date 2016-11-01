from flask import render_template

from app import app
from ..models.catagory import Catagory
from ..models.item import Item


@app.route('/')
def home():
    return render_template('home.html', Catagory=Catagory, Item=Item)
