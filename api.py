import urllib.robotparser as robotparser
import requests
from bs4 import BeautifulSoup
import xmltodict
from neo4j import GraphDatabase


# db = GraphDatabase.driver(uri='bolt://localhost:7687', auth=('find_me', 'password')).session()


def crawl():
    domains = ['https://stackoverflow.com']
    for domain in domains:
        rp = get_robot_parser(domain)
        urls = [url['loc'] for url in get_urls_from_sitemap(rp.site_maps()[0])]
        print(urls)


def get_robot_parser(domain):
    rp = robotparser.RobotFileParser()
    rp.set_url(domain + "/robots.txt")
    rp.read()

    return rp


def get_urls_from_sitemap(main_sitemap_url):
    urls = []
    sitemap_xml_urls = xmltodict.parse(requests.get(main_sitemap_url).text)['sitemapindex']['sitemap']
    for xml_url in sitemap_xml_urls:
        raw = xmltodict.parse(requests.get(xml_url['loc']).text)['urlset']['url']
        urls = urls + raw
        break

    return urls


crawl()

# url = "https://stackoverflow.com"
# rp = robotparser.RobotFileParser()
# rp.set_url(url + "/robots.txt")
# rp.read()
#
# print(rp.can_fetch('*', "https://stackoverflow.com/questions/43085744/parsing-robots-txt-in-python"))
# print(rp.can_fetch('*', "https://stackoverflow.com/users/login"))
# xml = requests.get('https://stackoverflow.com/sitemap-questions-286.xml').text
# raw = xmltodict.parse(xml)['urlset']['url']
# sitemap_urls = xmltodict.parse(requests.get(rp.site_maps()[0]).text)['sitemapindex']['sitemap']
# print("a")
#
# print('a')
# print(rp.site_maps(), requests.get(rp.site_maps()[0]).text, xml.firstChild)
