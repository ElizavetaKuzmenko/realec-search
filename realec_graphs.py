from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
import json



texts = db.labels.create("Texts")
# Create some nodes with labels
identifiers = {'texts':{}, 'mistakes': {}}
with open('./elastic/texts.json', 'r', encoding='utf-8') as f:
    i = 0
    for line in f:
        print('texts', i)
        data = json.loads(line.strip())
        name = data['t_name']
        text = data['text']
        mark = data['essay_mark']
        year = data['year']
        fac = data['faculty']
        t_type = data['task_type']
        t = db.nodes.create(name=name, text=text, mark=mark, year=year, faculty=fac, type=t_type, t_id=i)
        texts.add(t)
        identifiers['texts'][i] = t.id
        i += 1

mistakes = {}
mist = db.labels.create("Mistake")
with open('./elastic/mistakes.json', 'r', encoding='utf-8') as f:
    i = 0
    for line in f:
        print('mistakes', i)
        data = json.loads(line.strip())
        name = data['m_type']
        if name not in mistakes:
            m = db.nodes.create(name=name, id=i)
            mist.add(m)
            mistakes[name] = m.id
        text = data['m_text']
        corr = data['correction']
        w_l = data['weight_language']
        cause = data['cause']
        t_id = int(data['t_id'])
        db.node[identifiers['texts'][t_id]].relationships.create("contains", db.node[mistakes[name]], text=text,
                                                                 correction=corr, weight_language=w_l, cause=cause)
        i += 1



#q = 'MATCH (u:Texts)-[r:contains]->(m:Mistakes) WHERE u.name="esl_0021" RETURN u, type(r), m'
# "db" as defined above
#results = db.query(q, returns=(client.Node, str, client.Node))
#for r in results:
#    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
