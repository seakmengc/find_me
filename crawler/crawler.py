import requests
from link_finder import LinkFinder
from html_tag_parser import HtmlTagParser
from urllib import parse
from bs4 import BeautifulSoup

# ONLY crawl url start with base url
BASE_URL = 'https://stackoverflow.com/questions'
# starting page
HOME_PAGE = 'https://stackoverflow.com/questions'
HOME_PAGE ='https://stackoverflow.com/questions/3392354/append-values-to-a-set-in-python/3392370'


def grab_links(url, crawled):
    print('Fetching ' + url)
    content = {}
    try:
        response = requests.get(url)
        html_parser = HtmlTagParser(url, response.text)

        print(html_parser.description, 2)
        exit()
        links = LinkFinder(BASE_URL, url)
        print(response.headers)
        exit()
        links.feed(response.text)
    except:
        return

    crawled.add(url)
    new_links = links.page_links().difference(crawled)
    # print(new_links)
    # print(links.page_links())
    # print(crawled)

    for url in new_links:
        grab_links(url, crawled)


def get_search_tags(html_text):
    pass


crawled = set()
grab_links(HOME_PAGE, crawled)
print(crawled)
print('YES' if '1' in crawled else 'No')
