from flask import url_for


class Page(object):

    def __init__(self, test_app, address):
        self.test_app = test_app
        self.address = address

    def visit(self):
        self.response = self.test_app.get(self.address)


class HomePage(Page):

    def __init__(self, test_app):
        super().__init__(test_app, url_for('home'))

    @property
    def catagories(self):
        eles = self.response.html.find_all('section')[0].ul.find_all('li')
        return [e.text for e in eles]