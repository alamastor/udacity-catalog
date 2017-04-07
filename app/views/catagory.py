from flask import render_template

from ..app import app
from ..models.catagory import Catagory
from ..models.item import Item


@app.route('/catalog/<catagory_name>/items')
def catagory(catagory_name):
    return render_template(
        'catagory.html',
        Catagory=Catagory,
        catagory=catagory_name,
        Item=Item
    )
