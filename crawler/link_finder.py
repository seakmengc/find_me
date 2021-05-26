from html.parser import HTMLParser
from urllib import parse, robotparser


class LinkFinder(HTMLParser):

    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url

        url = parse.urlsplit(page_url)
        self.base_url = url.scheme + '://' + url.netloc
        self.robot_parser = get_robot_parser(self.base_url)

        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urlsplit(parse.urljoin(self.base_url, value))
                    clean_url = url.scheme + '://' + url.netloc + url.path
                    if self.robot_parser.can_fetch('*', clean_url) and clean_url.startswith(self.base_url):
                        self.links.add(clean_url)

    def page_links(self):
        return self.links


def get_robot_parser(domain):
    rp = robotparser.RobotFileParser()
    rp.set_url(domain + "/robots.txt")
    rp.read()

    return rp