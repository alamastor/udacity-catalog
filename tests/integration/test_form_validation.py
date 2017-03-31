from app.views.item import form_errors
from app.models import Item


def test_valid_form(dummy_catagories):
    assert form_errors({
        'name': 'asdf',
        'catagory': dummy_catagories[0],
        'description': 'asdf'
    }) == {}


def test_no_name_error(dummy_catagories):
    assert form_errors({
        'name': '',
        'catagory': dummy_catagories[0],
        'description': 'asdf'
    }) == {'name': 'Please enter a name.'}


def test_long_name_error(dummy_catagories):
    max_name_length = Item.name.property.columns[0].type.length
    assert form_errors({
        'name': 'x' * (max_name_length + 1),
        'catagory': dummy_catagories[0],
        'description': 'asdf'
    }) == {'name': 'Name must be less than %s characters.' % max_name_length}


def test_invalid_catagory_error(dummy_catagories):
    assert form_errors({
        'name': 'asdf',
        'catagory': 'aasdf',
        'description': 'asdf'
    }) == {'catagory': 'Not a valid catagory.'}


def test_no_description_error(dummy_catagories):
    assert form_errors({
        'name': 'asdf',
        'catagory': dummy_catagories[0],
        'description': ''
    }) == {'description': 'Please enter a description.'}