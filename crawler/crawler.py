import requests
from link_finder import LinkFinder
from html_tag_parser import HtmlTagParser

# ONLY crawl url start with base url
BASE_URL = 'https://stackoverflow.com/questions'
# starting page
HOME_PAGE = 'https://stackoverflow.com/questions'


def grab_links(url, crawled):
    print('Fetching ' + url)
    try:
        response = requests.get(url)
        html_parser = HtmlTagParser(url, response.text)

        #TODO: save in temp var
        html_parser.description
        html_parser.title

        links = LinkFinder(BASE_URL, url)
        links.feed(response.text)
    except:
        return

    crawled.add(url)
    new_links = links.page_links().difference(crawled)

    for url in new_links:
        grab_links(url, crawled)


crawled = set()
grab_links(HOME_PAGE, crawled)
#TODO: save crawl data to csv
print(crawled)
print('YES' if '1' in crawled else 'No')
