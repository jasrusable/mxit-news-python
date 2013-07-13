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
            'www.news24.com': XPathProcessor('//*[@id="article_special"]'),
            'mg.co.za': XPathProcessor('//*[@id="body_content"]'),
            'www.supersport.com': XPathProcessor('//*[@id="articlecontent"]'),
            'www.kickoff.com': XPathProcessor('//*[@id="central-wrapper"]/section'),
            'www.guardian.co.uk': XPathProcessor('//*[@id="article-body-blocks"]'),
            'www.skysports.com': XPathProcessor('//*[@id="ss-content"]'),
			'sport.iafrica.com' : XPathProcessor('//*[@id="articleBodyPrint"]'),
			'www.sport24.co.za':XPathProcessor('//*[@id="articleBodyContainer"]'),	

            }

    def get_site_id(self, url):
        url_parts = urlparse.urlparse(url)
        return url_parts.hostname

    def get_processor(self, url):
        site_id = self.get_site_id(url)
        if site_id in self.processors:
            return self.processors[site_id]
        else:
            print()
            print(url)
            print(site_id)
            print()
            return Processor()
