from flask import render_template
from flask import request
from app import app
import sqlite3
from elasticsearch import Elasticsearch
import re
from collections import defaultdict, OrderedDict

@app.route('/')
@app.route('/index')
def index():
    return render_template("search.html")

@app.route('/sql_search', methods=['GET', 'POST'])
def sql_search():
    base = sqlite3.connect('realec_tags.db')
    c = base.cursor()
    text = False
    tag_value = False
    results = False
    tags_results = False
    tags = ['Articles', 'Lex_item_choice', 'Prepositions']
    try:
        text = request.form['text_query']
    except:
        pass
    try:
        tag_value = request.form.getlist('tag_query')
    except:
        pass
    if text:
        c.execute('SELECT POS FROM tokens WHERE token=?', (text,))
        results = set([i[0] for i in c.fetchall()])
    if tag_value:
        tags_results = []
        for tag in tag_value:
            #print(tag)
            c.execute('SELECT text FROM tags WHERE type=?', (tag,))
            tags_results += list(set([i[0] for i in c.fetchall()]))
    base.close()
    return render_template("search.html", title='Search', text=text, results=results, tags=tags,
                           tags_results=tags_results)

@app.route('/elastic', methods=['GET', 'POST'])
def elastic_search():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    text = False
    texts = False
    try:
        text = request.form['text_query']
    except:
        pass
    if text:
        query = es.search(index="corpus", body={"query": {"match": {'text': text}}})
        results = query['hits']['hits']
        texts = []
        for r in results:
            res = r['_source']['text']
            #res = defaultdict(OrderedDict)
            #q = r['_source']['text'].replace(text, '<em>' + text + '<em>')
            #parts = q.split('<em>')
            #for part in parts:
            #    if part == text:
            #        res[part] = 'yes'
            #    else:
            #        res[part] = 'no'
            texts.append(res)
    return render_template("elastic.html", texts=texts)

def neo('/neo_search', methods=['GET', 'POST']):
    return render_template("neo.html")