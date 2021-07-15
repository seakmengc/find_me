import math


def sigmoid(num):
    return math.exp(num) / (math.exp(num) + 1)


def minmax_norm(num, min, max):
    div = (max - min)
    return 0 if div == 0 else (num - min) / div


def find_minmax(dict, key):
    return [min(dict, key=lambda doc: doc['scores'][key])['scores'][key], max(dict, key=lambda doc: doc['scores'][key])['scores'][key]]


def cal_probab(query, docs):
    N = len(docs)
    for doc in docs:
        score = 0
        for word in query:
            if not word in doc['freqs']:
                continue

            ni = doc['freqs'][word]
            if ni <= 0:
                continue

            score += math.log2((N+0.5) / (ni + 0.5))

        # scores[doc['url']] = sigmoid(score)
        doc['scores']['probab'] = sigmoid(score)


def ranking(docs):
    docs = docs.copy()

    [min_ref, max_ref] = find_minmax(docs, 'ref')
    # print(find_minmax(docs, 'tf_idf'))
    # print(find_minmax(docs, 'probab'))
    for doc in docs:
        doc['scores']['ref'] = minmax_norm(
            doc['scores']['ref'], min=min_ref, max=max_ref)

        doc['score'] = doc['scores']['tf_idf'] * 0.6 + \
            doc['scores']['ref'] * 0.25 + \
            doc['scores']['probab'] * 0.15
    # print(find_minmax(docs, 'ref'))

    return sorted(
        docs, key=lambda doc: doc["score"], reverse=True)


def tf(ni):
    return 0 if ni <= 0 else 1 + math.log2(ni)


def idf(N, n_docs_appear_in):
    return 0 if n_docs_appear_in <= 0 else math.log2(N / n_docs_appear_in)


def cal_tfidf(search_keywords, docs):
    N = len(docs)
    for doc in docs:
        score = 0
        for search_keyword in search_keywords:
            if not search_keyword in doc['freqs']:
                continue

            score += tf(doc['freqs'][search_keyword]) * idf(N, n_docs_appear_in=sum(
                [1 if search_keyword in doc['freqs'] and doc['freqs'][search_keyword] > 0 else 0 for doc in docs]))

        doc['scores']['tf_idf'] = sigmoid(score)
