from collections import OrderedDict
from urllib import robotparser

import requests
import xmltodict
from flask import Blueprint

from crawler.html_tag_parser import HtmlTagParser
from crawler.link_finder import LinkFinder
from models.doc import Doc

bp = Blueprint('crawler', __name__, cli_group='crawler')


@bp.cli.command('crawl')
def crawl():
    add_urls_by_sitemap()

    # Start scraping and exploring more urls
    doc = Doc.nodes.first_or_none(title__isnull=True)
    while doc:
        html_parser = parse_html(doc)

        if html_parser:
            # Done: save data to Url model
            doc.title = html_parser.title
            doc.description = html_parser.description
            doc.save()

            for link in html_parser.links:
                doc_ref = Doc.nodes.first_or_none(url=link)

                if doc_ref is None:
                    doc_ref = Doc(url=link).save()

                if not doc_ref.ref_docs.is_connected(doc):
                    doc_ref.ref_docs.connect(doc)

            # Doc.get_or_create(*[{'url': link} for link in html_parser.links])

        doc = Doc.nodes.first_or_none(title__isnull=True)


def parse_html(doc):
    if doc.title:
        return

    print('Crawling: ' + doc.url)

    try:
        response = requests.get(doc.url)

        links = LinkFinder(doc.url)
        links.feed(response.text)
    except:
        return

    return HtmlTagParser(doc.url, response.text, links.page_links())


def add_urls_by_sitemap():
    domains = ['https://stackoverflow.com']
    for domain in domains:
        print('Crawling sitemap of ' + domain)
        rp = get_robot_parser(domain)
        print('Done parsing robots.txt of ' + domain)

        raw_urls = get_urls_from_sitemap(rp.site_maps()[0])
        queue_urls = [{'url': url['loc']} for url in raw_urls]
        print(*queue_urls)
        Doc.get_or_create(*queue_urls)


def get_robot_parser(domain):
    rp = robotparser.RobotFileParser()
    rp.set_url(domain + "/robots.txt")
    rp.read()

    return rp


def get_urls_from_sitemap(main_sitemap_url):
    urls = []
    sitemap_xml_urls = xmltodict.parse(requests.get(main_sitemap_url).text)[
        'sitemapindex']['sitemap'][::-1]
    for xml_url in sitemap_xml_urls:
        raw = xmltodict.parse(requests.get(xml_url['loc']).text)['urlset']['url']
        urls = urls + raw
        break

    return urls
