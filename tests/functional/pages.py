from collections import namedtuple

from flask import url_for, session


class Page(object):

    def __init__(self, test_app, url):
        self.url = url
        self.test_app = test_app

    @property
    def html(self):
        return self.response.html

    def visit(self):
        response = self.test_app.get(self.url)
        status = response.status_code
        if status >= 400 and status < 500:
            raise RuntimeError('%s returned a %i error' % (self.url, status))
        self.response = response
        return self

    def submit_form(self, form, **kwargs):
        url = form.get('action', self.url)
        data = kwargs
        data['_csrf_token'] = self.html.find(
            'input', {'name': '_csrf_token'}
        ).attrs['value']
        response = self.test_app.post(
            url, headers={'referer': self.url}, data=data
        )
        status = response.status_code
        if status >= 400 and status < 500:
            raise RuntimeError('%s returned a %i error' % (self.url, status))
        self.response = response
        return self

    @property
    def is_logged_in(self):
        if self.html.find('button', id='logout-button'):
            return True
        else:
            return False

    def login(self):
        with self.test_app.session_transaction() as sess:
            sess['logged_in'] = True
        return self.visit()


Link = namedtuple('Link', ['text', 'url'])


class HomePage(Page):

    def __init__(self, test_app):
        super().__init__(test_app, url_for('home'))

    @property
    def catagories(self):
        links = self.html.find_all('section')[0].ul.find_all('a')
        return [Link(a.text, a['href']) for a in links]

    @property
    def items(self):
        eles = self.html.find_all('section')[1].ul.find_all('li')
        result = []
        for ele in eles:
            item = ele.text.split('-')[0].strip()
            catagory = ele.text.split('-')[1].strip()
            result.append((item, catagory))
        return result

    @property
    def item_links(self):
        links = self.html.find_all('section')[1].ul.find_all('a')
        return [Link(a.text, a['href']) for a in links]

    @property
    def add_item_link(self):
        link = self.html.find('a', class_='add-item-button')
        return Link(link.text, link['href'])


class CatagoryPage(Page):

    @property
    def catagories(self):
        links = self.html.find_all('section')[0].ul.find_all('a')
        return [Link(a.text, a['href']) for a in links]

    @property
    def items(self):
        links = self.html.find_all('section')[1].ul.find_all('a')
        return [Link(a.text, a['href']) for a in links]


class ItemPage(Page):

    @property
    def header(self):
        return self.html.h2.text

    @property
    def description(self):
        return self.html.p.text

    @property
    def edit_item_link(self):
        link = self.html.find('a', class_='edit-item')
        return Link(link.text, link['href'])

    @property
    def delete_item_link(self):
        link = self.html.find('a', class_='delete-item')
        return Link(link.text, link['href'])


class CreateItemPage(Page):

    @property
    def header(self):
        return self.html.find('h2')

    def add_item(self, **kwargs):
        form = self.html.find('form', class_='item-form')
        self.submit_form(form, **kwargs)


class EditItemPage(Page):

    @property
    def header(self):
        return self.html.find('h2')

    def edit_item(self, **kwargs):
        form = self.html.find('form', class_='item-form')
        self.submit_form(form, **kwargs)


class DeleteItemPage(Page):

    @property
    def header(self):
        return self.html.find('h2')

    def confirm_delete(self):
        form = self.html.find('form', class_='delete-item-form')
        self.submit_form(form)
