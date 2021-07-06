import math

def sigmoid(num):
    return math.exp(num) / (math.exp(num) + 1)


def cal_probab(query, docs):
    N = len(docs)
    for doc in docs:
        score = 0
        for word in query:
            try:
                ni = doc['freqs'][word]
                if ni > 0:
                    score += math.log2((N+0.5) / ni)
            except KeyError:
                continue
        
        # scores[doc['url']] = sigmoid(score)
        doc['scores']['probab'] = sigmoid(score)
        

def ranking(docs):
    docs = docs.copy()

    for doc in docs:
        doc['score'] = sigmoid((doc['scores']['tf_idf'] * 0.5 + doc['scores']['probab'] * 0.25 + doc['scores']['ref'] * 0.25) / 3)

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

            score += tf(doc['freqs'][search_keyword]) * idf(N, n_docs_appear_in=sum([1 if search_keyword in doc['freqs'] else 0 for doc in docs]))

        doc['scores']['tf_idf'] = sigmoid(score)
