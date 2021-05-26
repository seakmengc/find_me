from collections import Counter

from flask import Blueprint

import re
from string import punctuation
import nltk
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords

from models.keyword import Keyword
from models.doc import Doc
from neomodel import db

bp = Blueprint('stemmer', __name__, cli_group='stemmer')


@bp.cli.command('stem')
def stem():
    stemmer = SnowballStemmer(language="english")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    stop_words = set(stopwords.words("english"))

    # Start stemming
    doc = Doc.nodes.first_or_none(stemmed__exact=False, title__isnull=False, description__isnull=False)
    while doc:
        keys = get_keywords(doc, stemmer=stemmer, stop_words=stop_words)
        # print(keywords.items())
        # return

        with db.transaction:
            # print(*[{'keyword': keyword} for keyword in keys])
            keywords = Keyword.get_or_create(*[{'keyword': keyword} for keyword in keys])
            for keyword in keywords:
                if not keyword.docs.is_connected(doc):
                    keyword.docs.connect(doc, {'freq': keys[keyword.keyword]})

            doc.stemmed = True
            doc.save()

        doc = Doc.nodes.first_or_none(stemmed__exact=False, title__isnull=False, description__isnull=False)

    print('Done stemming')


def get_keywords(page, stemmer, stop_words):
    keywords = []

    texts = [page.title, page.description]
    for text in texts:
        # remove symbols n stuff
        text = re.sub(r"[\W+-_]", " ", text)

        words = word_tokenize(text.lower())
        for w in words:
            keyword = stemmer.stem(w)

            if w in stop_words or keyword in punctuation:
                continue

            keywords.append(keyword)

    # remove duplicates and sort by word frequency
    return Counter(keywords)
    return set(sorted(keywords, key=lambda w: keywords.count(w), reverse=True))
