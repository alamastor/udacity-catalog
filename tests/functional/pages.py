from collections import namedtuple

from flask import url_for


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
        response = self.test_app.post(
            url, headers={'referer': self.url}, data=kwargs
        )
        status = response.status_code
        if status >= 400 and status < 500:
            raise RuntimeError('%s returned a %i error' % (self.url, status))
        self.response = response
        return self

    @property
    def login_form(self):
        return self.html.find('form', class_='login-form')

    @property
    def is_logged_in(self):
        if self.html.find('form', class_='logout-form'):
            return True
        else:
            return False

    def login(self):
        return self.submit_form(self.login_form)


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
        link = self.html.find('a', class_='add-item')
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


class AddItemPage(Page):

    @property
    def header(self):
        return self.html.find('h2')

    def add_item(self, **kwargs):
        form = self.html.find('form', class_='add-item-form')
        self.submit_form(form, **kwargs)
