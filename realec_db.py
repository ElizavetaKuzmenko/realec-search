# coding: utf-8
__author__ = 'liza'

import sqlite3
base = sqlite3.connect('realec_tags.db')
c = base.cursor()


def extract_mist():
    mistakes = []
    with open('table_mistakes.csv') as tab_m:
        table = tab_m.readlines()
        for line in table[1:]:
            # mistake_id, text_id, type, text, attr_weight_language, cause, correction, tokens_id
            mistakes.append(line.strip().split('\t'))
    return mistakes


def extract_tokens():
    tokens = []
    with open('table_tokens.csv') as tab_m:
        table = tab_m.readlines()
        for line in table[1:]:
            # text_id, token_id, token, POS	lemma, mistake_id
            tokens.append(line.strip().split('\t'))
    return tokens


def extract_texts():
    texts = []
    with open('table_texts.csv') as tab_m:
        table = tab_m.readlines()
        for line in table[1:]:
            # text_id, text_name
            texts.append(line.strip().split('\t'))
    return texts


def make_tags():
    tags = extract_mist()
    c.execute('''CREATE TABLE tags (mistake_id, text_id, type, text, attr_weight_language, cause, correction, tokens_id)''')
    for tag in tags:
        if len(tag) == 7:
            tag.append('NA')
        c.execute('INSERT INTO tags VALUES (?,?,?,?,?,?,?,?)', tag)


def make_tokens():
    tokens = extract_tokens()
    c.execute('''CREATE TABLE tokens (text_id, token_id, token, POS, lemma, mistake_id)''')
    for token in tokens:
        if len(token) == 4:
            token.append(token[2])
            token.append('NA')
        elif len(token) == 5:
            token.append('NA')
        c.execute('INSERT INTO tokens VALUES (?,?,?,?,?,?)', token)


def make_texts():
    texts = extract_texts()
    c.execute('''CREATE TABLE texts (text_id, text_name)''')
    for text in texts:
        c.execute('INSERT INTO texts VALUES (?,?)', text)

def queries():
    type = input('Which tag? ')
    c.execute('SELECT text_id FROM tags WHERE type=?', (type,))
    for i in c.fetchall():
        print(i)
    #print(c.fetchall())

if __name__ == '__main__':
    make_tags()
    make_tokens()
    make_texts()
    base.commit()
    base.close()
    #queries()
