# /bin/bash
from flask import Flask, url_for, render_template, redirect
import feedparser
from urlparse import urlparse, parse_qs

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', news_url=url_for('news_page'), page_title='Home')

@app.route('/news/')
def news_page():
	return render_template('news.html',back_url=url_for('index'), temp=temp, page_title='Home/News')

@app.route('/news/<topic>/')
def news_topic(topic):
	for d in temp:
		if d['topic_url'] == url_for('news_topic', topic=topic.lower()):
			feed = feedparser.parse(d['rss_url'])
			feeed = []
			for item in feed['items']:
				diccc = {}
				diccc['title'] = item['title']
				diccc['url'] = parse_qs(urlparse(item['link']).query)['url'][0]
				feeed.append(diccc)
			return render_template('topic.html', back_url=(url_for('news_page')), ff=feeed,  page_title='Home/News/'+d['name'])
	return 'mmm'

temp = [
{'name':'Tech','topic_id':'tc'},
{'name':'Sports', 'topic_id':'s'},
{'name':'Regional','topic_id':''}]

hl = 'en'
ned = 'en_za'
code = '.co.za'

#feed_url = 'https://news.google'+code+'/news/feeds?pz=1&topic='+topic+'&cf=all&ned='+ned+'&hl='+hl+'&output=rss'
#feed = feedparser.parse(feed_url)

#for item in feed['items']:
#       print parse_qs(urlparse(item['link']).query)['url'][0]

with app.test_request_context():
        for item in temp:
                item['rss_url'] = ('https://news.google'+code+'/news/feeds?pz=1&topic='+item['topic_id']+'&cf=all&ned='+ned+'&hl='+hl+'&output=rss')
                item['topic_url'] = url_for('news_topic', topic=item['name'].lower())

if __name__ == '__main__':
	app.run(debug=True)
