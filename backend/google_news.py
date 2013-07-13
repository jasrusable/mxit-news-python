from models import Topic, Article
import requests
import feedparser
import urlparse
from base64 import urlsafe_b64encode as b64encode

class GoogleNews(object):
    topics = {
            'w': Topic(name= 'World', id='w'),
            'n': Topic(name= 'National', id='n'),
            'b': Topic(name= 'Business', id='b'),
            'tc': Topic(name= 'Technology', id='tc'),
            'e': Topic(name= 'Entertainment', id='e'),
            's': Topic(name= 'Sports', id='s'),
            'snc': Topic(name= 'Science', id='snc'),
            'm': Topic(name= 'Health', id='m')
    }

    regions = [
            {'name': 'South Africa', 'tld': '.co.za', 'ned': 'en_ZA', 'hl': 'en'}
    ]

    def get_articles_by_topic(self, id, region=regions[0]):
        BASE_URL = 'http://news.google%s/news' % region['tld']
        params = {
                'pz': 1, # http/https
                'cf': 'all',  # ?
                'ned': region['ned'],
                'hl': region['hl'], # home lang
                'output': 'rss', # only supports rss
                'topic': id
                }

        response = requests.get(BASE_URL, params=params)
        feed = feedparser.parse(response.text)
        return [self.article_from_feed_entry(entry) for entry in feed.entries]

    def fetch_topic(self, id):
        topic = self.topics[id]
        topic.articles = self.get_articles_by_topic(id)
        return topic

    def article_from_feed_entry(self, entry):
        url_parts = urlparse.urlparse(entry.link)
        query_parts = urlparse.parse_qs(url_parts.query)
        url = query_parts['url'][0]
        url = b64encode(url)
        return Article(title=entry.title, url=url)

class GoogleNewsSearch(object):
    """Search for news using google.
    Warning - deprecated, will work till 2014
    """
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/news'

    def result_to_article(self, result):
        title = ('%s - %s') % (result['title'], result['publisher'])
        url = b64encode(result['url'])
        return Article(title, url)

    def search(self, query):
        params = {
                'v': '1.0',
                'q': query
                }
        raw_response = requests.get(self.BASE_URL, params=params)
        response = json.loads(raw_response.text)
        response_data  = response['responseData']
        results = response_data['results']
        return [self.result_to_article(result) for result in results]
