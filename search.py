from elasticsearch import Elasticsearch, helpers
import sys, json
import os
from PyDictionary import PyDictionary

def load_json(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(filename,'r') as open_file:
                files.append(json.load(open_file))
    return files


if __name__ == '__main__':
    dictionary = PyDictionary()

    es = Elasticsearch(HOST="http://localhost", PORT=9200)
    es = Elasticsearch()
    a=load_json(r'C:\Users\LERA\PycharmProjects\search2')
    for i in range(len(a)):
        es.index(index="index", doc_type="doc", id=i, body=a[i])
    print('Запрос по дате? y-да, n-нет')
    f = str(input())
    if (f == 'n'):
        q = input('query ')
        body = {
            "_source": [
                "ref"
            ],
            "query": {
                "match": {
                    "content": q
                }
            }
        }
        ans = []
        res = es.search(index="index", body=body)
        ans.append(res)
        for i in ans:
            a = i['hits']
            b = a['hits']
            for el in b:
                s = el['_score']
                source = el['_source']
                r = source['ref']
                print(r, s)
        try:
            synonyms = dictionary.synonym(q)
            for s in synonyms:
                body = {
                    "_source": [
                        "ref"
                    ],
                    "query": {
                        "match": {
                            "content": s
                        }
                    }
                }
                res = es.search(index="index", body=body)
                ans.append(res)
        except:
            pass
        print('\n')
        print("Поиск по синонимам \n")
        j=0
        for i in ans:
            a = i['hits']
            b = a['hits']
            try:
                print(synonyms[j])
            except:
                pass
            if b ==[]:
                print('no results')
            j+=1
            for el in b:
                s = el['_score']
                source = el['_source']
                r = source['ref']
                print(r, s)
    else:
        f = input('от ')
        t = input('до ')
        body = {
            "_source": [
                "ref"
            ],
            "query": {
                "range": {
                    "date": {
         "gt": f,
         "lte": t
       }
                }
            }
        }
        res = es.search(index="index", body=body)
        ans = []
        ans.append(res)
        for i in ans:
            a = i['hits']
            b = a['hits']
            for el in b:
                s = el['_score']
                source = el['_source']
                r = source['ref']
                print(r, s)

