#!/bin/bash
from flask import Flask, url_for, render_template, redirect, request
import feedparser
from urlparse import urlparse, parse_qs
from base64 import urlsafe_b64decode as b64decode

from backend import GoogleNews, ArticleParser, GoogleNewsSearch

google_news = GoogleNews()
google_news_search = GoogleNewsSearch()
article_parser = ArticleParser()

app = Flask(__name__)

def search(query):
    """Respond with a list of search results.
    """

    results = news_searcher.search(query)
    return render_template('search_results.html', results=results, query=query)



@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage, list news topics or respond with search results if
    X-Mxit-User-Input is present.
    """
    query = request.form.get('X-Mxit-User-Input')
    if query:
        # The user has submitted a search query.
        return search(query)
    else:
        # The user is requesting the home page.
        topics = news_browser.get_topics()
        return render_template('index.html',
                topics=topics,
                debug=True)

@app.route('/topic/')
def topic():
    topic_id = request.args.get('id')
    topic = news_browser.fetch_topic(topic_id)

    return render_template('topic.html', topic=topic)


@app.route('/article/')
def article():
    b64_url = request.args.get('b64_url')
    url = b64decode(b64_url.encode('ascii'))
    article = article_reader.fetch_article(url)

    return render_template('article.html',article=article)

if __name__ == '__main__':
	app.run(debug=True)
