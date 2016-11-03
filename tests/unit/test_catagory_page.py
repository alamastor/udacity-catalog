from app.views.catagory import catagory


def test_catagory_page_calls_render_with_Catagory(mock):
    mock_render_template = mock.patch('app.views.catagory.render_template')
    mock_Catagory = mock.patch('app.views.catagory.Catagory')
    catagory('soccer')
    mock_render_template.assert_called_once_with(
        'catagory.html',
        Catagory=mock_Catagory,
        catagory=mock.ANY,
        Item=mock.ANY
    )


def test_catagory_page_calls_render_with_catagory(mock):
    mock_render_template = mock.patch('app.views.catagory.render_template')
    catagory('soccer')
    mock_render_template.assert_called_once_with(
        'catagory.html', Catagory=mock.ANY, catagory='soccer', Item=mock.ANY
    )


def test_catagory_page_calls_render_with_Item(mock):
    mock_render_template = mock.patch('app.views.catagory.render_template')
    mock_Item = mock.patch('app.views.catagory.Item')
    catagory('soccer')
    mock_render_template.assert_called_once_with(
        'catagory.html', Catagory=mock.ANY, catagory=mock.ANY, Item=mock_Item
    )
