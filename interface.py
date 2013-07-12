#!/bin/bash
from flask import Flask, url_for, render_template, redirect, request
import feedparser
from urlparse import urlparse, parse_qs
from backend import GoogleNews
from base64 import urlsafe_b64decode as b64decode
import backend

google_news = GoogleNews()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """News homepage, list news topics and link to search.
    """
    query = request.form.get('X-Mxit-User-Input')
    if query:
        results = ['oua']
        return render_template('search_results.html', results=results, query=query)

    topics = google_news.get_topics()
    return render_template('index.html',
            topics=topics,
            debug=True)

@app.route('/news/topic/<topic_id>')
def topic(topic_id):
    articles = google_news.get_articles(topic_id)
    topic_name = google_news.topics[topic_id]['name']
    return render_template('topic.html',
            back_url=url_for('index'),
            articles=articles,
            topic_id=topic_id,
            topic_name=topic_name)

@app.route('/news/<topic_id>/article/<article_url>')
def article(article_url, topic_id):
    url = b64decode(article_url.encode('utf-8'))
    title, text = backend.fetch_article(url)
    return render_template('article.html',
            text=text,
            title=title,
            back_url=url_for('topic', topic_id=topic_id))

if __name__ == '__main__':
	app.run(debug=True)
