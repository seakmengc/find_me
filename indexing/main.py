from pathlib import Path
import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re

stemmer = PorterStemmer()
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
stop_words = set(stopwords.words("english"))

crawled_csv_path = Path(__file__).parent / "../data/crawled.csv"
stemmed_csv_path = Path(__file__).parent / "../data/stemmed.csv"

URL_LABEL = "https://stackoverflow.com/questions"
TITLE_LABEL = "newest questions"
DESC_LABEL = "stack overflow | the world’s largest online community for developers"


# stemming
def get_keywords(text):
    # remove symbols n stuff
    text = re.sub(r"[\W+-_]", " ", text)

    words = word_tokenize(text.lower())
    keywords = []
    for w in words:
        keyword = stemmer.stem(w)

        if w in stop_words or keyword in punctuation:
            continue

        keywords.append(keyword)

    # remove duplicates and sort by word frequency
    return sorted(set(keywords), key=lambda w: keywords.count(w), reverse=True)


def get_keywords_dict_from_csv():
    keywords = {}
    with crawled_csv_path.open() as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            url, title, desc = [row[URL_LABEL], row[TITLE_LABEL], row[DESC_LABEL]]
            keywords[url] = get_keywords(title + desc)

    return keywords


def write_csv(keywords_dict):
    with stemmed_csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "keywords"])
        writer.writeheader()

        for url in keywords_dict:
            writer.writerow({ "url": url, "keywords": keywords_dict[url] })


def init():
    keywords_dict = get_keywords_dict_from_csv()
    write_csv(keywords_dict)

    pass


# store data
def boot_graph_db():
    # TODO: read from stemmed csv

    # TODO: create data

    pass


init()
