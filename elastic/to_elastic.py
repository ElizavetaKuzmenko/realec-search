# coding: utf-8

import json, requests, os, csv
from elasticsearch import Elasticsearch
PATH = '/home/lizaku/PycharmProjects/REALEC/anns_for_db'
PATH_mistakes = '/home/lizaku/PycharmProjects/REALEC/table_mistakes.csv'



def make_json(doc):
    js = {}
    js['t_name'] = doc.split('/')[-1][:-4]
    js['text'] = open(doc, encoding='utf-8').read()
    js['year'] = 2016
    js['faculty'] = ''
    js['essay_mark'] = 0
    js['task_type'] = 'essay'
    return json.dumps(js, ensure_ascii=False)


def read_corpus(path):
    jsons = set()
    for f in os.listdir(path):
        if f.endswith('.txt'):
            js = make_json(path + os.sep + f)
            jsons.add(js)
    return jsons


def extract_mistakes(path):
    jsons = set()
    with open(path, encoding='utf-8') as f:
        table = csv.reader(f, delimiter='\t')
        next(table, None)  # skip header
        for row in table:
            print(row)
            js = {}
            mistake_id, text_id, m_type, m_text, attr_weight, cause, correction, tokens_id = row
            js['m_type'] = m_type
            js['m_text'] = m_text
            js['correction'] = correction
            js['t_id'] = text_id
            js['weight_language'] = attr_weight
            js['cause'] = cause
            jsons.add(json.dumps(js, ensure_ascii=False))
    return jsons


def to_elastic():
    jsons = read_corpus(PATH)
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    i = 1
    for j in jsons:
        print(i)
        doc = json.loads(j)
        r = requests.get('http://localhost:9200')
        if r.status_code != 200:
            print(i)
        es.index(index='corpus', doc_type='document', id=i, body=doc)
        i += 1
    jsons = extract_mistakes(PATH_mistakes)
    i = 1
    for j in jsons:
        print(i)
        doc = json.loads(j)
        r = requests.get('http://localhost:9200')
        if r.status_code != 200:
            print(i)
        es.index(index='corpus', doc_type='mistake', id=i, body=doc)
        i += 1
    #while r.status_code == 200: ?


if __name__ == '__main__':
    to_elastic()

