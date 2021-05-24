import requests
from link_finder import LinkFinder
from html_tag_parser import HtmlTagParser
from csv_writer import CSVWriter
from csv_writer import TxtWrite
from csv_writer import TxtRead

# ONLY crawl url start with base url
BASE_URL = 'https://stackoverflow.com/questions'


def grab_links(url, crawled):
    if (url in crawled): 
        return
    
    print('Fetching ' + url)
    try:
        response = requests.get(url)
        html_parser = HtmlTagParser(url, response.text)

        # Done: append url to crawled.txt
        TxtWrite('data/crawled_urls.txt', html_parser.url)

        # Done: append crawl data to csv
        CSVWriter(html_parser.url, html_parser.title, html_parser.description)

        links = LinkFinder(BASE_URL, url)
        links.feed(response.text)
    except:
        return

    crawled.add(url)
    new_links = links.page_links().difference(crawled)

    # Done: append urls to to_crawl_urls
    TxtWrite('data/to_crawl_urls.txt', new_links)


crawled = set()

# Done: run until out of urls in to_crawl_urls
# Done: read from to_crawl_urls and clear file
# Done: loop to each url

grab_links(BASE_URL, crawled)
for x in range(500):
    nextUrl = TxtRead('data/to_crawl_urls.txt').readStr()
    if nextUrl != None:
        grab_links(nextUrl, crawled)

print(crawled)
print('YES' if '1' in crawled else 'No')
