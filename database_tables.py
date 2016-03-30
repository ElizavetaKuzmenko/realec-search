# coding: utf-8
__author__ = 'liza'

import os, re

PATH = './anns_for_db'
table1 = open('table_tokens.csv', 'w', encoding='utf8')
table1.write('text_id\ttoken_id\ttoken\tPOS\tlemma\tmistake_id\n')
table2 = open('table_mistakes.csv', 'w', encoding='utf8')
table2.write('mistake_id\ttext_id\ttype\ttext\tattr_weight_language\tcause\tcorrection\ttokens_id\n')
table3 = open('table_texts.csv', 'w', encoding='utf8')
table3.write('text_id\ttext_name\n')

def write_table(f, text_id, mistake_id):
    token_id = 1
    lines = open(f, 'r', encoding='utf8').readlines()
    tokens = []
    table3.write(str(text_id) + '\t' + f + '\n')
    for line in range(len(lines)):
        if 'pos_' in lines[line]:
            proc_line = lines[line].strip().split('\t')
            pos, span1, span2 = proc_line[1].split(' ')
            pos = pos.replace('pos_', '')
            T = proc_line[0]
            try:
                token = proc_line[2]
            except IndexError:
                token = 'NA'
            lemma = 'NA'
            if 'AnnotatorNotes ' + T in lines[line + 1]:
                proc_line = lines[line + 1].strip().split('\t')
                lemma = proc_line[2].replace('lemma = ', '').replace('\'', '')
            tokens.append([text_id, token_id, token, pos, lemma, [], int(span1), int(span2)])
            token_id += 1

    mistakes = []
    for line in range(len(lines)):
        if re.search('^T', lines[line]) is not None and 'pos_' not in lines[line]:
            proc_line = lines[line].strip().split('\t')
            error_type, span1, span2 = proc_line[1].split(' ')
            T = proc_line[0]
            try:
                error_text = proc_line[2]
            except IndexError:
                error_text = 'NA'
            w_lang = 'NA'
            cause = 'NA'
            correction = 'NA'
            if 'AnnotatorNotes ' + T in lines[line + 1]:
                proc_line = lines[line + 1].strip().split('\t')
                correction = proc_line[2]
            elif 'AnnotatorNotes ' + T in lines[line + 2]:
                proc_line = lines[line + 2].strip().split('\t')
                correction = proc_line[2]
            elif 'AnnotatorNotes ' + T in lines[line + 3]:
                proc_line = lines[line + 3].strip().split('\t')
                correction = proc_line[2]
            elif 'AnnotatorNotes ' + T in lines[line + 4]:
                proc_line = lines[line + 4].strip().split('\t')
                correction = proc_line[2]

            if 'Cause ' + T in lines[line + 1]:
                proc_line = lines[line + 1].strip().split(' ')
                cause = proc_line[2]
            elif 'Cause ' + T in lines[line + 2]:
                proc_line = lines[line + 2].strip().split(' ')
                cause = proc_line[2]
            elif 'Cause ' + T in lines[line + 3]:
                proc_line = lines[line + 3].strip().split(' ')
                cause = proc_line[2]
            elif 'Cause ' + T in lines[line + 4]:
                proc_line = lines[line + 4].strip().split(' ')
                cause = proc_line[2]

            if 'Weight-language ' + T in lines[line + 1]:
                proc_line = lines[line + 1].strip().split(' ')
                w_lang = proc_line[2]
            elif 'Weight-language ' + T in lines[line + 2]:
                proc_line = lines[line + 2].strip().split(' ')
                w_lang = proc_line[2]
            elif 'Weight-language ' + T in lines[line + 3]:
                proc_line = lines[line + 3].strip().split(' ')
                w_lang = proc_line[2]
            elif 'Weight-language ' + T in lines[line + 4]:
                proc_line = lines[line + 4].strip().split(' ')
                w_lang = proc_line[2]
            mistakes.append([mistake_id, text_id, error_type, error_text, w_lang, cause, correction, [], int(span1), int(span2)])
            mistake_id += 1
    for token in tokens:
        token_id = token[1]
        span1, span2 = token[-2:]
        for mistake in mistakes:
            mistake_id = mistake[0]
            mspan1, mspan2 = mistake[-2:]
            if span1 >= mspan1 and span2 <= mspan2:
                token[-3].append(mistake_id)
                mistake[-3].append(token_id)
    for token in tokens:
        #errors = ','.join([str(x) for x in token[-3]])
        errors = [str(x) for x in token[-3]]
        if len(errors) == 0:
            table1.write('\t'.join([str(x) for x in token[:-3]]) + '\tNA\n')
        else:
            for error in errors:
                table1.write('\t'.join([str(x) for x in token[:-3]]) + '\t' + error + '\n')
    for mistake in mistakes:
        #toks = ','.join([str(x) for x in mistake[-3]])
        toks = [str(x) for x in mistake[-3]]
        if len(toks) == 0:
            table2.write('\t'.join([str(x) for x in mistake[:-3]]) + '\tNA\n')
        else:
            for tok in toks:
                table2.write('\t'.join([str(x) for x in mistake[:-3]]) + '\t' + tok + '\n')
    return mistake_id

if __name__ == '__main__':
    files = os.listdir(PATH)
    text_id = 1
    mistake_id = 1
    for f in files:
        if f.endswith('.ann'):
            print('***', f, '***')
            f = PATH + os.sep + f
            try:
                mistake_id = write_table(f, text_id, mistake_id)
            except:
                continue
            text_id += 1
    table1.close()
    table2.close()