from collections import namedtuple

from flask import url_for


class Page(object):

    def __init__(self, test_app, url):
        self.test_app = test_app
        self.url = url

    def visit(self):
        response = self.test_app.get(self.url)
        status = response.status_code
        if status >= 400 and status < 500:
            raise RuntimeError('%s returned a %i error' % (self.url, status))
        self.response = response
        return self

    @property
    def html(self):
        return self.response.html


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
        return [tuple(e.text.split(' - ')) for e in eles]


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
    def description(self):
        return self.html.p.text
