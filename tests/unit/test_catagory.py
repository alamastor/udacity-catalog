import pytest

from app.models.catagory import Catagory


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


def test_create_calls_add_and_commit(mock, mock_session):
    catagory = Catagory.create('a catagory')
    mock_session.add.assert_called_once_with(catagory)
    mock_session.commit.assert_called_once_with()


def test_fetch_all_calls_query(mock_session):
    Catagory.fetch_all()
    mock_session.query.assert_called_once_with(Catagory)


def test_fetch_all_returns_result(mock_session):
    assert Catagory.fetch_all() == mock_session.query.return_value
