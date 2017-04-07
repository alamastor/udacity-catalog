import json

import pytest
from flask import url_for


def test_api_base(test_app, dummy_items_json):
    res = test_app.get(url_for('api_base'))
    assert json.loads(res.data.decode()) == dummy_items_json


@pytest.fixture
def dummy_items_json(dummy_catagories, dummy_items):
    result = {'catagories': []}
    for i, catagory in enumerate(dummy_catagories):
        result['catagories'].append({
            'id': i + 1,
            'name': catagory,
            'items': []
        })
        for j, item in enumerate(dummy_items):
            if item.catagory == catagory:
                result['catagories'][i]['items'].append({
                    'id': j + 1,
                    'catagory_id': i + 1,
                    'name': item.name,
                    'description': item.description
                })
    return result