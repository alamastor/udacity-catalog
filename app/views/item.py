from flask import render_template, request, redirect, url_for

from app import app
from app.models import Item, Catagory
from app.auth import login_required


@app.route('/catalog/<catagory_name>/<item_name>')
def read_item(item_name, catagory_name):
    item = Item.fetch_by_name_and_catagory_name(item_name, catagory_name)
    return render_template('item.html', item=item)


@app.route('/catalog/create_item')
@login_required
def create_item_page():
    catagories = [c.name for c in Catagory.fetch_all()]
    return render_template('add_item.html', catagories=catagories, values={})


@app.route('/catalog/create_item', methods=['POST'])
@login_required
def create_item():
    name = request.form['name']
    catagory = request.form['catagory']
    description = request.form['description']

    max_name_length = Item.name.property.columns[0].type.length
    if len(name) > max_name_length:
        catagories = [c.name for c in Catagory.fetch_all()]
        errors = {'name': (
            'Name must be no more than %i '
            'characters long.' % max_name_length
        )}
        values = {
            'name': name, 'catagory': catagory, 'description': description
        }
        return render_template(
            'add_item.html',
            catagories=catagories,
            values=values,
            errors=errors
        )
    Item.create(name, catagory_name=catagory, description=description)
    return redirect(url_for(
        'read_item', catagory_name=catagory, item_name=name
    ))
