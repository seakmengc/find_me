from flask import Flask
from flask import request
import os
from neomodel import db
from commands.crawl import bp as crawl_bp
from commands.stem import bp as stem_bp

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from commands.stem import get_keywords
from models.keyword import Keyword


app = Flask(__name__)

app.register_blueprint(crawl_bp)
app.register_blueprint(stem_bp)

db.set_connection(
    "bolt://{username}:{password}@{uri}".format(
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        uri=os.getenv("DB_URI"),
    )
)

lemmatizer = WordNetLemmatizer()

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
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
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
def search():
    query = request.args.get("query")

    # word tokenize
    # filter stopwords
    keywords = list(get_keywords(query).keys())

    # lemmatize
    # synonyms
    # stemming

    res = Keyword.nodes.filter(keyword__in=keywords)

    for r in res:
        print(r)
        
    return res


if __name__ == "__main__":
    app.run(debug=True)
