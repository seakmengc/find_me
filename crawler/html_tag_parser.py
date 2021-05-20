from bs4 import BeautifulSoup


class HtmlTagParser:

    def __init__(self, url, html_text):
        self.soup = BeautifulSoup(html_text, 'html.parser')

        self.url = url
        self.title = self.get_title()
        self.description = self.get_description()

    def get_title(self):
        title = self.soup.find('meta', {'name': 'title'})

        if title is None:
            title = self.soup.find('meta', {'itemprop': 'name'})

        return str(title.get('content')).lower()

    def get_description(self):
        title = self.soup.find('meta', {'name': 'description'})

        if title is None:
            title = self.soup.find('meta', {'itemprop': 'description'})

        return str(title.get('content')).lower()
