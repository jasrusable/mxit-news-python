from models import Article, Topic
from BeautifulSoup import BeautifulSoup
import re
import requests
from base64 import urlsafe_b64decode as b64decode

from backend.processor import Processors
processors = Processors()

class ArticleReader(object):
    """Extracts the title and body of a web page.
    """
    def get_article(self, url):
        """Fetch a webpage, extract it's title and body
        and return these in an Article object.
        """
        url = b64decode(url.encode('ascii'))
        # Fetch the article body
        html = self.fetch_url(url)

        # Encode the body as a utf-8 string.
        html = html.encode('utf-8', 'ignore')

        # Scrape the title of the article
        title = self.scrape_title(html)

        # Apply processor.
        processor = processors.get_processor(url)
        html = processor.process(html)

        # Scrape the text of the article.
        body = self.scrape_body(html)

        body = self.insert_paragraphs(body)

        return Article(url=url, title=title, text=body)

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
        return '<br/><br/>'.join(text)

    def scrape_body(self, html):
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
