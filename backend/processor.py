import urlparse
from StringIO import StringIO
from lxml import etree
from lxml import html as lxml_html

class Processor(object):
    def process(self, html):
        return html

class XPathProcessor(Processor):
    def __init__(self, xpath):
        self.parser = etree.XMLParser(recover=True)
        self.xpath = xpath

    def process(self, html):
        f = StringIO(html)
        doc = etree.parse(f, self.parser)
        element = doc.xpath(self.xpath)[0]
        text =  etree.tostring(element)
        return text

class Processors(object):
    processors = {
            'mg.co.za': XPathProcessor('//*[@id="body_content"]'),
            'www.supersport.com': XPathProcessor('//*[@id="articlecontent"]'),
            'www.kickoff.com': XPathProcessor('//*[@id="central-wrapper"]/section'),
            'www.guardian.co.uk': XPathProcessor('//*[@id="article-body-blocks"]'),
            'www.skysports.com': XPathProcessor('//*[@id="ss-content"]'),
            'www.iol.co.za': XPathProcessor('//*[@id="article_container"]'),
			'sport.iafrica.com' : XPathProcessor('//*[@id="articleBodyPrint"]'),
            'ewn.co.za': XPathProcessor('//*[@id="main"]'),
            'news.cnet.com': XPathProcessor('//*[@id="contentBody"]/div[2]/div'),
			'www.sport24.co.za': XPathProcessor('//*[@id="articleBodyContainer"]'),	
			'www.bbc.co.uk': XPathProcessor('//*[@id="storypage-container"]/div[1]/div[4]'),
			'sport.iafrica.com': XPathProcessor('//*[@id="articleBodyPrint"]'),
			'www.sport24.co.za': XPathProcessor('//*[@id="articleBodyContainer"]'),	
			'www.bbc.co.uk': XPathProcessor('//*[@id="storypage-container"]/div[1]/div[4]'),
			'www.smh.com.au': XPathProcessor('//*[@id="content"]/div[3]'),
			'www.telegraph.co.uk' : XPathProcessor('//*[@id="mainBodyArea"]'),
            }

    def get_site_id(self, url):
        url_parts = urlparse.urlparse(url)
        return url_parts.hostname

    def get_processor(self, url):
        site_id = self.get_site_id(url)
        if site_id in self.processors:
            return self.processors[site_id]
        else:
            return Processor()
