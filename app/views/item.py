from flask import render_template

from app import app
from app.models.item import Item


@app.route('/catalog/<catagory_name>/<item_name>')
def item(item_name, catagory_name):
    item = Item.fetch_by_name_and_catagory_name(item_name, catagory_name)
    return render_template('item.html', item=item)
