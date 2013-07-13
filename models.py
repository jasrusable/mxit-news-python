from flask import url_for, Markup

class Topic(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.articles = []

    def get_url(self):
        base_url = url_for('topic')
        return ('%s?id=%s') % (base_url, self.id)


class Article(object):
    def __init__(self, title, url, text=None):
        self.title = Markup(title)
        self.url = url
        self.text = Markup(text)

    def get_display_url(self):
        return '/article/?url=' + self.url
