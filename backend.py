from models import Article, Topic
import requests
import urlparse
import feedparser
import json
from BeautifulSoup import BeautifulSoup
import re

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
        return Article(title=entry.title, url=url)

class GoogleNewsSearch(object):
    """Search for news using google.
    Warning - deprecated, will work till 2014
    """
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/news'

    def result_to_article(self, result):
        title = ('%s - %s') % (result['title'], result['publisher'])
        url = result['url']
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

class ArticleReader(object):
    def fetch_article(self, url):
        # Fetch the article body
        html = self.fetch_url(url)
        # Encode the body as a utf-8 string.
        #html = html.encode('utf-8', 'ignore')

        # Scrape the text from the article.
        text = self.scrape_text(html)

        # Paragraph the text.
        text = self.insert_paragraphs(text)

        title = self.scrape_title(html)

        return Article(url=url, title=title, text=text)

    def fetch_url(self, url):
        return requests.get(url).text

    def extract_longest(self, seq, bad, max_bad):
        # start of current subsequnce
        head = 0
        # number of non bad items since head
        score = 0
        # best sequence so far
        best = []
        #current sequence
        current = []
        # number of consecutive bad chars so far
        bad_count = 0
        best_score = 0

        for i in range(len(seq)):
            s = self.unescape(seq[i])
            if s == bad:
                bad_count += 1
                if bad_count > max_bad:
                    score = 0
                    head = i
                    current = [] 
            else:
                bad_count = 0
                score += 1
                if len(s) > 32:
                    score += len(s)
        
            if score > 0:
                current.append(s)
                if score > best_score:
                    best_score = score
                    best = current
        return best

    def insert_paragraphs(self, text):
        text = [line for line in text if not line == '\n']
        text_block = '. '.join(text)
        text = text_block.split('. ')
        return '.<br/>'.join(text)

    def scrape_text(self, html):
        soup = BeautifulSoup(html)
        texts = soup.findAll(text=True)
        visible_texts = filter(self.visible, texts)
        text = self.extract_longest(visible_texts, u'\n', 2)
        return text

    def scrape_title(self, html):
        soup = BeautifulSoup(html)
        title = soup.title.text
        return title

    def unescape(self, text):
        out = text.replace('&nbsp;', ' ')
        return out

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True
