import nltk
from nltk import word_tokenize


def extract_ne(text):
    words = word_tokenize(text)
    tags = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tags, binary=True)

    ne = set()
    for ent in tree:
        if hasattr(ent, 'label') and ent.label() == 'NE':
            ne.add(" ".join(i[0] for i in ent))

    return ne


doc = extract_ne('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices.'
                 ' Information Retrieval has.')
print(doc)