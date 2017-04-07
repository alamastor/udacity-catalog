import pytest

from app.models.catagory import Catagory
from app.models.item import Item


@pytest.fixture
def mock_session(mock):
    return mock.patch('app.models.catagory.db.session')


@pytest.fixture
def mock_catagory(mock):
    return mock.Mock()


def test_create_calls_Item(mock, mock_session, mock_catagory):
    mock_init = mock.patch(
        'app.models.item.Item.__init__', return_value=None
    )
    Item.create(
        'an item', catagory=mock_catagory, description='a description'
    )
    mock_init.assert_called_once_with(
        name='an item', catagory=mock_catagory, description='a description'
    )


def test_create_calls_add_and_commit(mock, mock_session, mock_catagory):
    item = Item.create('an item')
    mock_session.add.assert_called_once_with(item)
    mock_session.commit.assert_called_once_with()


def test_create_uses_catagory_name_arg_when_passed(mock, mock_session):
    mock_init = mock.patch(
        'app.models.item.Item.__init__', return_value=None
    )
    Item.create(
        'an item', catagory_name='a catagory', description='description'
    )
    mock_init.assert_called_once_with(
        name='an item', catagory=mock.ANY, description='description'
    )


def test_create_raises_when_called_with_catagory_and_catagory_name(
    mock_session, mock_catagory):
    with pytest.raises(TypeError):
        Item.create(
            'an item', catagory=mock_catagory, catagory_name='a catagory'
        )


def test_fetch_all_calls_query(mock_session):
    Item.fetch_all()
    mock_session.query.assert_called_once_with(Item)


def test_fetch_all_returns_all(mock_session):
    mock_all = mock_session.query.return_value.all
    assert Item.fetch_all() == mock_all.return_value


def test_fetch_by_name_and_catagory_name_returns_one(mock, mock_session):
    mock_filter = mock_session.query.return_value.filter
    mock_one = mock_filter.return_value.one.return_value
    assert Item.fetch_by_name_and_catagory_name('ball', 'soccer') == mock_one


def test_update_item_with_name_updates_name(mock_session):
    item = Item()
    item.name = 'a'
    item.update(name = 'b')
    assert item.name == 'b'


def test_update_item_with_description_updates_description(mock_session):
    item = Item()
    item.description = 'x'
    item.update(description = 'y')
    assert item.description == 'y'


def test_update_calls_commit(mock_session):
    Item().update()
    mock_session.commit.assert_called_once_with()


def test_dict(mock_session):
    item = Item()
    item.name = 'x'
    item.catagory_id = 2
    item.description = 'z'
    assert item.dict == {
        'id': None,
        'catagory_id': 2,
        'name': 'x',
        'description': 'z'
    }