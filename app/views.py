from flask import render_template
from flask import request
from app import app
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # выдуманный пользователь
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("search.html",
                           title='Home',
                           user=user,
                           posts=posts)

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
