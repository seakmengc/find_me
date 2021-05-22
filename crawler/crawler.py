import requests
from link_finder import LinkFinder
from html_tag_parser import HtmlTagParser

# ONLY crawl url start with base url
BASE_URL = 'https://stackoverflow.com/questions'


def grab_links(url, crawled):
    print('Fetching ' + url)
    try:
        response = requests.get(url)
        html_parser = HtmlTagParser(url, response.text)

        # TODO: append url to crawled.txt

        # TODO: append crawl data to csv

        html_parser.description
        html_parser.title

        links = LinkFinder(BASE_URL, url)
        links.feed(response.text)
    except:
        return

    crawled.add(url)
    new_links = links.page_links().difference(crawled)

    # TODO: append urls to to_crawl_urls


crawled = set()

# TODO: run until out of urls in to_crawl_urls
# TODO: read from to_crawl_urls and clear file
# TODO: loop to each url
grab_links(HOME_PAGE, crawled)

print(crawled)
print('YES' if '1' in crawled else 'No')
