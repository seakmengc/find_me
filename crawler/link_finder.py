from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urlsplit(parse.urljoin(self.base_url, value))
                    clean_url = url.scheme + '://' + url.netloc + url.path
                    if self.base_url in clean_url:
                        self.links.add(clean_url)

    def page_links(self):
        return self.links