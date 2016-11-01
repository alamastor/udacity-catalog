from app.views.home import home


def test_home_page_calls_render_template_with_Catagory(mock):
    mock_render_template = mock.patch('app.views.home.render_template')
    mock_Catagory = mock.patch('app.views.home.Catagory')
    home()
    mock_render_template.assert_called_once_with(
        'home.html', Catagory=mock_Catagory, Item=mock.ANY
    )
def test_home_page_calls_render_template_with_Item(mock):
    mock_render_template = mock.patch('app.views.home.render_template')
    mock_Item = mock.patch('app.views.home.Item')
    home()
    mock_render_template.assert_called_once_with(
        'home.html', Catagory=mock.ANY, Item=mock_Item
    )
