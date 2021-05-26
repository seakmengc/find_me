from collections import OrderedDict
from urllib import robotparser

import requests
import xmltodict
from flask import Blueprint

from crawler.html_tag_parser import HtmlTagParser
from crawler.link_finder import LinkFinder
from models.page import Page

bp = Blueprint('crawler', __name__, cli_group='crawler')


@bp.cli.command('crawl')
def crawl():
    add_urls_by_sitemap()

    # Start crawling
    page = Page.nodes.first_or_none(title__isnull=True)
    while page:
        html_parser = parse_html(page)

        if html_parser:
            # Done: save data to Url model
            page.title = html_parser.title
            page.description = html_parser.description
            page.save()
            print(page)

            Page.get_or_create(*[{'url': link} for link in html_parser.links])

        page = Page.nodes.first_or_none(title__isnull=True)


def parse_html(page):
    if page.title:
        return

    print('Crawling: ' + page.url)

    try:
        response = requests.get(page.url)

        links = LinkFinder(page.url)
        links.feed(response.text)
    except:
        return

    return HtmlTagParser(page.url, response.text, links.page_links())


def add_urls_by_sitemap():
    domains = ['https://stackoverflow.com']
    for domain in domains:
        print('Crawling sitemap of ' + domain)
        rp = get_robot_parser(domain)
        print('Done parsing robots.txt of ' + domain)

        raw_urls = get_urls_from_sitemap(rp.site_maps()[0])[:10]
        queue_urls = [{'url': url['loc']} for url in raw_urls]
        print(*queue_urls)
        Page.get_or_create(*queue_urls)


def get_robot_parser(domain):
    rp = robotparser.RobotFileParser()
    rp.set_url(domain + "/robots.txt")
    rp.read()

    return rp


def get_urls_from_sitemap(main_sitemap_url):
    # return [OrderedDict({'loc': 'https://stackoverflow.com/questions/10855/linq-query-on-a-datatable'})]
    urls = []
    sitemap_xml_urls = xmltodict.parse(requests.get(main_sitemap_url).text)['sitemapindex']['sitemap']
    for xml_url in sitemap_xml_urls:
        raw = xmltodict.parse(requests.get(xml_url['loc']).text)['urlset']['url']
        urls = urls + raw
        break

    return urls