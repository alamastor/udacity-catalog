from flask import render_template

from app import app
from ..models.catagory import Catagory
from ..models.item import Item


@app.route('/catalog/<catagory>/items')
def catagory(catagory):
    return render_template(
        'catagory.html',
        Catagory=Catagory,
        catagory=catagory,
        Item=Item
    )
