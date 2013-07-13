#!/bin/bash
from flask import Flask, url_for, render_template, redirect, request
from base64 import urlsafe_b64decode as b64decode

from backend import GoogleNewsSearch, GoogleNews, ArticleReader
from util import cached_call, get_with_back

news_searcher = GoogleNewsSearch()
news_browser = GoogleNews()
article_reader = ArticleReader()

app = Flask(__name__)

def search(query):
    """Respond with a list of search results.
    """
    results = cached_call(news_searcher.search, query=query)
    return render_template('search_results.html', results=results, query=query,
            with_back=get_with_back(request),
            back_url=request.args.get('back_url'))


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
        topics = news_browser.topics
        return render_template('index.html',
                topics=topics,
                debug=True,
                with_back=get_with_back(request),
                back_url=request.args.get('back_url'))

@app.route('/topic/')
def topic():
    topic_id = request.args.get('id')
    print(request.args)
    topic = cached_call(news_browser.fetch_topic, topic_id)
    return render_template('topic.html', topic=topic, with_back=get_with_back(request),
            back_url=request.args.get('back_url'))


@app.route('/article/')
def article():
    print(request.args)
    url = request.args.get('url')
    article = cached_call(article_reader.fetch_article, url)
    return render_template('article.html',
            article=article,
            with_back=get_with_back(request),
            back_url=request.args.get('back_url'))

if __name__ == '__main__':
	app.run(debug=True)
