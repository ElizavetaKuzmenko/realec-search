from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase


# Create some nodes with labels
text = db.labels.create("Texts")
t1 = db.nodes.create(name="esl_0021")
text.add(t1)
t2 = db.nodes.create(name="esl_0022")
text.add(t2)

mist = db.labels.create("Mistakes")
m1 = db.nodes.create(name="Articles")
m2 = db.nodes.create(name="lex_item_choice")
# You can associate a label with many nodes in one go
mist.add(m1, m2)

t1.relationships.create("contains", m1, text="a")
t1.relationships.create("contains", m2, text="amount")
t2.relationships.create("contains", m1, text="the")



#q = 'MATCH (u:Texts)-[r:contains]->(m:Mistakes) WHERE u.name="esl_0021" RETURN u, type(r), m'
# "db" as defined above
#results = db.query(q, returns=(client.Node, str, client.Node))
#for r in results:
#    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
