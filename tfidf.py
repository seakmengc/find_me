import math

def calc_score(q, d, all_d):
    score = 0
    for t in q:
        score += tf(t, d) * idf(t, all_d)

    return score


def tf(t, d):
    return float(d.count(t)) / len(d)


def idf(t, all_d):
    count_in_doc = 0
    
    for d in all_d:
        if t in d["content"]:
            count_in_doc += 1

    return 0 if count_in_doc == 0 else math.log(len(all_d) / float(count_in_doc), 2)


def calc_tfidf(query, docs):
    results = []

    for doc in docs: 
        score = calc_score(query, doc["content"], docs)

        if score > 0:
            results.append({**doc, "score": score})

    for res in results:
        del res["content"]
        
    return results