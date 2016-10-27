from flask import render_template
from flask import request
from app import app
import sqlite3
from elasticsearch import Elasticsearch
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
import re

tags = ['Prepositional_verb', 'Double_object', 'Quant_choice', 'Conditionals', 'Prepositional_adv', 'Often_confused', 'No_diff', 'Quantifiers', 'Agreement_errors', 'Modals_form', 'Attributes', 'Choice_of_ref', 'Animacy', 'Absence_comp_colloc', 'Det_form', 'Causation', 'Voice_form', 'Note_structure', 'Modals', 'Pronouns', 'Demonstrative', 'Modals_choice', 'Comparative_adv', 'Word_order', 'Relative_clause', 'Determiners', 'Incoherent_pron', 'Incoherent_conj', 'Det_choice', 'Diff', 'Person', 'Punctuation', 'Abs_comp_clause', 'Redundant', 'Discourse', 'Choice_synonyms', 'Interrogative', 'Superlative_adj', 'Personal', 'Standard', 'Derivation', 'Formational_affixes', 'Verb_prep_Gerund', 'Redundant_ref', 'Adverbs', 'Lack_of_ref_device', 'Conjunctions', 'that_clause', 'Seq_of_tenses', 'Numerical', 'Double_prep_phrasal', 'suggestion', 'Verb_Gerund', 'lex_part_choice', 'Vocabulary', 'Dangling_ref', 'Concession', 'Voice', 'Comparative_adj', 'Adjectives', 'Title_structure', 'Verb_pattern', 'Participial_constr', 'Verbs', 'Infinitive_constr', 'Coherence', 'Tense_choice', 'Incoherent_articles', 'Trans_phrasal', 'Spelling', 'Transitive', 'Presentation', 'And_syn', 'Word_choice', 'Category_confusion', 'Defining', 'Comparative_constr', 'Modifier', 'Tense_form', 'Verb_patterns', 'Grammar', 'Non_defining', 'Dative', 'Verb_Inf', 'Tense', 'Voice_choice', 'Noun_number', 'Form_in_cond', 'Attr_participial', 'Incoherent_in_cond', 'Trans_prep', 'Countable_uncountable', 'Number', 'Adjective_inf', 'Lack_of_connective', 'Prepositional_noun', 'Articles', 'lex_item_choice', 'Absence_explanation', 'Negation', 'Verb_object_inf', 'Incoherent_intro_unit', 'Redundant_comp', 'Incoherent_tenses', 'Suffix', 'Prepositions', 'Num_form', 'Contrast', 'Art_choice', 'Possessive', 'Art_form', 'Absence_comp_sent', 'Inappropriate_register', 'Quant_form', 'Tautology', 'Emphatic', 'Nouns', 'Lack_par_constr', 'Prepositional_adjective', 'Collective']

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
    text_results = False
    tags_results = False
    try:
        text = request.form['text_query']
    except:
        pass
    try:
        tag_value = request.form.getlist('tag_query')
    except:
        pass
    if text:
        c.execute('SELECT text_id FROM tokens WHERE token=?', (text,))
        results = set([i[0] for i in c.fetchall()])
        text_results = []
        for r in results:
            c.execute('SELECT text_name FROM texts WHERE text_id=?', (r,))
            t_results = [i[0].split('/')[-1].split('.')[0] for i in c.fetchall()]
            for t in t_results:
                with open('./anns_for_db/' + t + '.txt', 'r', encoding="utf-8") as f:
                    tex = f.read()
                    sents = re.split(r'(?:[.]\s*){3}|[.?!]', tex)
                    for sent in sents:
                        if re.search(text, sent) is not None:
                            text_results.append(sent)
    if tag_value:
        tags_results = {}
        for tag in tag_value[:-1]:
            c.execute('SELECT text FROM tags WHERE type=?', (tag,))
            t_results = list(set([i[0] for i in c.fetchall()]))
            tags_results[tag] = t_results
    base.close()
    return render_template("search.html", title='Search', text=text, results=text_results, tags=tags,
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

@app.route('/neo_search', methods=['GET', 'POST'])
def neo():
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="Sydney&witty3Unity")
    tag_value = False
    res = []
    try:
        tag_value = request.form.getlist('tag_query')
    except:
        pass
    if tag_value:
        res = []
        for tag in tag_value[:-1]:
            query = 'MATCH (t:Texts)-[r:contains]->(m:Mistake) WHERE m.name="%s" RETURN t, type(r), m' % tag
            results = db.query(query, returns=(client.Node, str, client.Node))
            for r in results:
                line = r[0]["name"] + ' ' + r[1] + ' ' + r[2]["name"]
                res.append(line)
    return render_template("neo.html", res=res, tags=tags)