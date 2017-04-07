import pytest

from app.models.catagory import Catagory
from app.models.item import Item


@pytest.fixture
def mock_session(mock):
    return mock.patch('app.models.catagory.db.session')

def test_create_calls_Catagory(mock, mock_session):
    mock_init = mock.patch(
        'app.models.catagory.Catagory.__init__', return_value=None
    )
    Catagory.create('a catagory')
    mock_init.assert_called_once_with(name='a catagory')


def test_create_returns_instance(mock_session):
    assert isinstance(Catagory.create('a catagory'), Catagory)


def test_create_calls_add_and_commit(mock_session):
    catagory = Catagory.create('a catagory')
    mock_session.add.assert_called_once_with(catagory)
    mock_session.commit.assert_called_once_with()


def test_fetch_all_calls_query(mock_session):
    Catagory.fetch_all()
    mock_session.query.assert_called_once_with(Catagory)


def test_fetch_all_returns_all(mock_session):
    mock_all = mock_session.query.return_value.all
    assert Catagory.fetch_all() == mock_all.return_value


def test_exists_calls_query_twice(mock, mock_session):
    Catagory.exists('a catagory')
    mock_filter = mock_session.query.return_value.filter
    mock_exists_call = mock_filter.return_value.exists.return_value
    calls = [mock.call(Catagory), mock.call(mock_exists_call)]
    assert mock_session.query.call_args_list == calls


def test_exists_calls_filter(mock, mock_session):
    Catagory.exists('a catagory')
    mock_filter = mock_session.query.return_value.filter
    mock_filter.assert_called_once_with(mock.ANY)


def test_exists_return_one(mock_session):
    mock_one = mock_session.query.return_value.one
    assert Catagory.exists('a catagory') == mock_one.return_value[0]


def test_dict(mock_session):
    catagory = Catagory(name='cat')
    item = Item(name='x', catagory_id=catagory.id, description='z')
    catagory.items = [item]
    assert catagory.dict == {
        'id': None,
        'name': 'cat',
        'items': [
            item.dict
        ]
    }