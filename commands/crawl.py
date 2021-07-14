import threading
import signal
import sys
from collections import OrderedDict
from time import sleep
from urllib import robotparser

import requests
import xmltodict
from flask import Blueprint

from crawler.html_tag_parser import HtmlTagParser
from crawler.link_finder import LinkFinder
from models.doc import Doc

from neomodel import db


bp = Blueprint('crawler', __name__, cli_group='crawler')


@bp.cli.command('crawl')
def crawl():
    # add_urls_by_sitemap()

    # Start scraping and exploring more urls
    create_threads(thread_function=crawl_webpages, n=8)

    while True:
        sleep(1)


def create_threads(thread_function, n):
    threads = list()
    for index in range(n):
        print("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, daemon=True)
        threads.append(x)
        x.start()
        sleep(1)

    return threads


def crawl_webpages():
    doc = Doc.nodes.order_by('?').first_or_none(title__isnull=True)

    while doc:
        if doc.url.startswith('https://stackoverflow.com/users/') or doc.url.startswith('https://stackoverflow.com/a/') or doc.url.startswith('https://stackoverflow.com/q/') or doc.url.startswith('https://stackoverflow.com/questions/tagged/'):
            print("deleted ", doc.url)
            doc.delete()
            doc = Doc.nodes.order_by('?').first_or_none(title__isnull=True)
            continue

        html_parser = parse_html(doc)

        if html_parser:
            with db.write_transaction:
                # Done: save data to Url model
                doc.title = html_parser.title
                doc.description = html_parser.description
                doc.save()

                for link in html_parser.links:
                    doc_ref = Doc.nodes.first_or_none(url=link)

                    if doc_ref is None:
                        continue
                        # doc_ref = Doc(url=link).save()

                    doc_ref.ref += 1
                    doc_ref.save()

                    # if doc_ref.id != doc.id and not doc_ref.ref_docs.is_connected(doc):
                    #     doc_ref.ref_docs.connect(doc)

                # Doc.get_or_create(*[{'url': link} for link in html_parser.links])
        else:
            doc.delete()

        doc = Doc.nodes.order_by('?').first_or_none(title__isnull=True)


def parse_html(doc):
    if doc.title:
        return None

    print('Crawling: ' + doc.url)

    try:
        response = requests.get(doc.url)

        links = LinkFinder(doc.url)
        links.feed(response.text)
    except:
        return None

    return HtmlTagParser(doc.url, response.text, links.page_links())


def add_urls_by_sitemap():
    domains = ['https://stackoverflow.com']
    for domain in domains:
        print('Crawling sitemap of ' + domain)
        rp = get_robot_parser(domain)
        print('Done parsing robots.txt of ' + domain)

        if rp.site_maps() is None:
            continue

        raw_urls = get_urls_from_sitemap(rp.site_maps()[0])
        queue_urls = [{'url': url['loc']} for url in raw_urls]
        # print(*queue_urls)
        Doc.get_or_create(*queue_urls)


def get_robot_parser(domain):
    rp = robotparser.RobotFileParser()
    rp.set_url(domain + "/robots.txt")
    rp.read()

    return rp


def get_urls_from_sitemap(main_sitemap_url):
    urls = []
    sitemap_xml_urls = xmltodict.parse(requests.get(main_sitemap_url).text)[
        'sitemapindex']['sitemap']

    for xml_url in sitemap_xml_urls:
        raw = xmltodict.parse(requests.get(xml_url['loc']).text)[
            'urlset']['url']
        print(raw)
        exit()
        urls = urls + (raw if isinstance(raw, list) else [raw])

    return urls
