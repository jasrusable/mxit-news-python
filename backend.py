# /bin/python2
import feedparser
from urlparse import urlparse, parse_qs

temp = [
{'name':'Tech','topic':'tc'},
{'name':'Sports', 'topic':'s'},
{'name':'Regional','topic':''}]

hl = 'en'
ned = 'en_za'
code = '.co.za'

#feed_url = 'https://news.google'+code+'/news/feeds?pz=1&topic='+topic+'&cf=all&ned='+ned+'&hl='+hl+'&output=rss'
#feed = feedparser.parse(feed_url)

#for item in feed['items']:
#	print parse_qs(urlparse(item['link']).query)['url'][0]


for item in temp:
	item['rss_url'] = ('https://news.google'+code+'/news/feeds?pz=1&topic='+item['topic']+'&cf=all&ned='+ned+'&hl='+hl+'&output=rss')
	item['topic_url'] = url_for('news_page') + item['name'].lower()
