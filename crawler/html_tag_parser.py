from bs4 import BeautifulSoup


class HtmlTagParser:

    def __init__(self, url, html_text, links):
        self.soup = BeautifulSoup(html_text, 'html.parser')

        self.url = url
        self.title = self.get_title()
        self.description = self.get_description()
        self.links = links

    def get_title(self):
        title = self.soup.find('meta', {'name': 'title'})

        if title is None:
            title = self.soup.find('meta', {'itemprop': 'name'})

        return str(title.get('content')).lower().strip("\n. ") if title else ''

    def get_description(self):
        description = self.soup.find('meta', {'name': 'description'})

        if description is None:
            description = self.soup.find('meta', {'itemprop': 'description'})

        return str(description.get('content')).lower().strip("\n. ") if description else ''
