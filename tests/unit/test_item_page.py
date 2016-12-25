from app.views.item import read_item


def test_item_page_calls_render_with_Item(mock):
    mock_render = mock.patch('app.views.item.render_template')
    mock_Item = mock.patch('app.views.item.Item')
    mock_item = mock_Item.fetch_by_name_and_catagory_name.return_value
    item('soccer', 'ball')
    mock_render.assert_called_once_with('item.html', item=mock_item)
