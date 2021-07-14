import json
from models.doc import Doc
from process import ranking, sigmoid, cal_probab, cal_tfidf
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import time as time_

from commands.crawl import bp as crawl_bp
from commands.stem import bp as stem_bp

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from commands.stem import get_keywords
from models.keyword import Keyword
from neomodel import Q, config, db
from neo4j import GraphDatabase

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(crawl_bp)
app.register_blueprint(stem_bp)

NEO_URL = "bolt://{username}:{password}@{uri}".format(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    uri=os.getenv("DB_URI"),
)

db.set_connection(NEO_URL)
config.AUTO_INSTALL_LABELS = True

config.DATABASE_URL = NEO_URL

db = GraphDatabase.driver(os.getenv("URI"), auth=(
    os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD")))

lemmatizer = WordNetLemmatizer()


def get_time_ms():
    return int(round(time_.time() * 1000))


# function to convert nltk tag to wordnet tag
def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith("J"):
        return wordnet.ADJ
    elif nltk_tag.startswith("V"):
        return wordnet.VERB
    elif nltk_tag.startswith("N"):
        return wordnet.NOUN
    elif nltk_tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


def find_synonyms(keyword):
    synonyms = []
    for synset in wordnet.synsets(keyword):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())

    return str(synonyms)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/search")
@cross_origin()
def search():
    query = request.args.get("query")
    start = get_time_ms()

    # word tokenize
    # filter stopwords
    # stemming
    search_keywords = list(get_keywords(query).keys())
    print(search_keywords)

    # keywords = Keyword.nodes.has(docs=True).filter(
    #     keyword__in=search_keywords)
    # # end = get_time_ms()

    response = dict()
    query = ""
    for keyword in search_keywords:
        query += "MATCH (d: Doc) < -[ in :IN]-(k: Keyword {keyword: '" + keyword + \
            "'}) RETURN {d: properties(d), freq: COALESCE(in.freq, 0), keyword: k.keyword} as result UNION ALL "

    # graph_response = db.cypher_query(query.rstrip(" UNION ALL "))[0]

    query = query.rstrip(" UNION ALL ")
    with db.session() as session:
        # graph_response = session.read_transaction(lambda tx: tx.run(query))
        graph_response = session.run(query).data()
        # print([record.data() for record in graph_response])
    # print(graph_response)
    print(query)

    for record in graph_response:
        each = record['result']
        if not each['d']['url'] in response:
            response[each['d']['url']] = {
                "url": each['d']['url'],
                "title": each['d']['title'],
                "description": each['d']['description'],
                'freqs': {each['keyword']: each['freq']},
                'scores': {
                    'ref': each['d']['ref'],
                }
            }
        else:
            response[each['d']['url']]['freqs'][each['keyword']] = each['freq']
            response[each['d']['url']
                     ]['scores']['ref'] += each['d']['ref']

    docs = list(response.values())

    cal_probab(search_keywords, docs)

    # calc_tfidf(search_keywords, docs)
    cal_tfidf(search_keywords, docs)

    sorted_results = ranking(docs)

    end = get_time_ms()

    print(start, end, str(end-start))
    return {
        "time_to_search_in_milliseconds": str(end - start) + " ms",
        "results": sorted_results,
    }

    # lemmatize
    # synonyms


if __name__ == "__main__":
    app.run(debug=True)
