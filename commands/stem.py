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
stemmer = SnowballStemmer(language="english")
stop_words = set(stopwords.words("english"))


@bp.cli.command('stem')
def stem():
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")

    # Start stemming
    doc = Doc.get_havent_stemmed()
    while doc:
        text = doc.title + ' ' + doc.description
        keys = get_keywords(text=text)
        # print(keywords.items())
        # return

        with db.transaction:
            # print(*[{'keyword': keyword} for keyword in keys])
            keywords = Keyword.get_or_create(
                *[{'keyword': keyword} for keyword in keys])
            for keyword in keywords:
                if not keyword.docs.is_connected(doc):
                    keyword.docs.connect(doc, {'freq': keys[keyword.keyword]})

            doc.stemmed = True
            doc.save()

        doc = Doc.get_havent_stemmed()

    print('Done stemming')


def get_keywords(text):
    keywords = []

    # remove symbols n stuff
    text = re.sub(r"[\W+-_]", " ", text)

    words = word_tokenize(text.lower())
    for w in words:
        keyword = stemmer.stem(w)

        if w in stop_words or keyword in punctuation:
            continue

        keywords.append(keyword)

        # keywords.append(extract_ne(words))
    return Counter(keywords)


# Experiment
def extract_ne(text):
    words = word_tokenize(text)
    tags = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tags, binary=True)

    ne = []
    for ent in tree:
        if hasattr(ent, 'label') and ent.label() == 'NE':
            print(i for i in ent)
            ne.append(" ".join(i[0] for i in ent))

    return ne
