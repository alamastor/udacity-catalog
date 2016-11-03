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
    Item.create('an item', catagory=mock_catagory)
    mock_init.assert_called_once_with(name='an item', catagory=mock_catagory)


def test_create_returns_instance(mock_session, mock_catagory):
    assert isinstance(Item.create('an item', catagory=mock_catagory), Item)


def test_create_calls_add_and_commit(mock, mock_session, mock_catagory):
    item = Item.create('an item')
    mock_session.add.assert_called_once_with(item)
    mock_session.commit.assert_called_once_with()


def test_create_uses_catagory_name_arg_when_passed(mock, mock_session):
    mock_init = mock.patch(
        'app.models.item.Item.__init__', return_value=None
    )
    Item.create('an item', catagory_name='a catagory')
    mock_init.assert_called_once_with(
        name='an item', catagory_name='a catagory'
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


def test_fetch_catagory_calls_filter(mock, mock_session):
    Item.fetch_catagory('soccer')
    mock_filter = mock_session.query.return_value.filter
    mock_filter.assert_called_once_with(mock.ANY)
