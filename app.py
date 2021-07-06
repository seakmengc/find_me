from process import ranking, sigmoid, cal_probab, cal_tfidf
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
from neomodel import db
import time as time_

from commands.crawl import bp as crawl_bp
from commands.stem import bp as stem_bp

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from commands.stem import get_keywords
from models.keyword import Keyword
from neomodel import Q, config

from tfidf import calc_tfidf


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

config.DATABASE_URL = NEO_URL

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


def lemmatize_sentence(sentence):
    # tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    # tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (
        x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


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

    keywords = Keyword.nodes.has(docs=True).filter(keyword__in=search_keywords)

    response = {}
    for keyword in list(keywords):
        for r in list(keyword.docs.all()):
            if not r.url in response:
                response[r.url] = {
                    "url": r.url,
                    "title": r.title,
                    "description": r.description,
                    # "content": (r.title + " " + r.description).lower().split(),
                    "content": [keyword.keyword],
                    'freqs': {keyword.keyword: keyword.docs.relationship(r).freq},
                    'scores': {
                        'ref': sigmoid(len(r.ref_docs)),
                    }
                }
            else:
                response[r.url]['content'].append(keyword.keyword)
                response[r.url]['freqs'][keyword.keyword] = keyword.docs.relationship(r).freq


    docs = list(response.values())

    cal_probab(search_keywords, docs)

    # calc_tfidf(search_keywords, docs)
    cal_tfidf(search_keywords, docs)

    sorted_results = ranking(docs)

    end = get_time_ms()

    print(start, end)

    return {
        "time_to_search_in_milliseconds": str(end - start) + "ms",
        "results": sorted_results,
    }

    # lemmatize
    # synonyms


if __name__ == "__main__":
    app.run(debug=True)
