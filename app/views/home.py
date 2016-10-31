from flask import render_template

from app import app
from ..models.catagory import Catagory


@app.route('/')
def home():
    return render_template('home.html', Catagory=Catagory)
