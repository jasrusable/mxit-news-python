#! /bin/python2
import feedparser
import re
from urlparse import urlparse, parse_qs
import urllib
import requests
import nltk
from flask import Markup
from base64 import urlsafe_b64encode as b64encode
from BeautifulSoup import BeautifulSoup

def fetch_url(url):
    return requests.get(url).text

def extract_longest(seq, bad, max_bad):
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
        s = unescape(seq[i])
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
    return ''.join(best)

def insert_paragraphs(text):
    return text


def scrape_text(html):
    soup = BeautifulSoup(html)
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    text = extract_longest(visible_texts, u'\n', 2)
    return text

def scrape_title(html):
    soup = BeautifulSoup(html)
    title = soup.title.text
    return title

def unescape(text):
    """Resolves &#xxx; HTML entities (and some others)."""
    out = text.replace('&nbsp;', ' ')
    return out

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def fetch_article(url):
    html = fetch_url(url)
    html = html.encode('utf-8', 'ignore')
    text = scrape_text(html)
    text = insert_paragraphs(text)
    text = text.replace('\n', '<br/>')

    title = scrape_title(html)
    return title, Markup(text)

class GoogleNews(object):
    regions = [
            {'name': 'South Africa', 'tld': '.co.za', 'ned': 'en_ZA', 'hl': 'en'}
            ]
    topics = { 
            'w': {'name': 'World'},
            'n': {'name': 'National'},
            'b': {'name': 'Business'},
            'tc': {'name': 'Technology'},
            'e': {'name': 'Entertainment'},
            's': {'name': 'Sports'},
            'snc': {'name': 'Science'},
            'm': {'name': 'Health'}
            }
    def extract_image_url(self, html):
        soup = BeautifulSoup(html)
        imgs = soup.findAll("img",{"alt":True, "src":True})
        for img in imgs:
                img_url = img["src"]
                return img_url

    def get_articles(self, topic_id):
        url, params = self.build_request(topic_id, self.regions[0])
        response = requests.get(url, params=params)
        feed = feedparser.parse(response.text)

        articles = []
        for entry in feed.entries:
            b64url = b64encode(entry['link'])
            image_url = self.extract_image_url(entry['summary'])
            articles.append({'title': entry.title, 'url': b64url, 'image_url': image_url})

        return articles
            

    def build_request(self, topic_id, region):
        base_url = 'https://news.google%s/news' % region['tld']
        params = {
                'pz': 1, # seams to change between http and https
                'cf': 'all', # not sure,
                'ned': region['ned'], # locale stuff
                'hl': region['hl'],
                'output': 'rss', # doesn't support anything else?
                'topic': topic_id
                }
        return base_url, params

    def add_url(self, topic):
        topic['url'] = self.build_url(topic['topic_id'], region=self.regions[0])
        return topic

    def get_topics(self):
        return self.topics