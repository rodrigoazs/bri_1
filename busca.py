# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:34:55 2017

@author: Rodrigo Azevedo

Modulo de buscador
"""

import time
import logging
import configparser
import xml.etree.ElementTree as ET
import re
import csv
import ast
import math
from unidecode import unidecode
import nltk
from sklearn.metrics.pairwise import cosine_similarity

# função para calcular cosine similarity
def cos_sim(A, B):
    num = 0
    A_den = 0
    B_den = 0
    for word_id, value in A.items():
        if word_id in B:
            num = num + value * B[word_id]
        A_den = A_den + value**2
    for word_id, value in B.items():
        B_den = B_den + value**2
    return (1.0*num)/(math.sqrt(A_den)*math.sqrt(B_den))

logging.info('Modulo de busca iniciado')

config = configparser.ConfigParser()
config.read('busca.cfg')
file_model = config.get('config', 'MODELO')
file_query = config.get('config', 'CONSULTAS')
file_result = config.get('config', 'RESULTADOS')
logging.info('Leitura do arquivo de configuração')

csv.field_size_limit(500 * 1024 * 1024) # problema com 'field larger than field limit (131072)'
with open(file_model, 'r') as csvfile:
    logging.info('Leitura do arquivo de modelo de indexação '+str(file_model))
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if len(row):
            if row[0] == 'TOKENS':
                words_dict = ast.literal_eval(row[1])
            elif row[0] == 'MODEL':
                matrix_word_doc = ast.literal_eval(row[1])

total_words = len(words_dict)
#total_documents = 0

# matrix esparca doc word
dict_doc_word = {}
for word_id in range(len(matrix_word_doc)):
    for document_id, f in matrix_word_doc[word_id].items():
        if document_id not in dict_doc_word:
            dict_doc_word[document_id] = {}
        dict_doc_word[document_id][word_id] = f
        #total_documents = int(max(total_documents, document_id))

# matrix esparca doc word
#for i in range(len(matrix_word_doc)):
#    for key, value in matrix_word_doc[i].items():
#        matrix_doc_word[key][i] = value
                       
# obter word pelo key
#words_key = ['' for x in range(total_words)]
#for key, value in words_dict.items():
#    words_key[value] = key

# transpoe a matrix em documentos x termos
#t_matrix = [list(i) for i in zip(*matrix)]

xml = ET.parse(file_query)
logging.info('Leitura do arquivo de consultas '+str(file_query))
root = xml.getroot()

total_time = 0
total_query = 0
to_save = []
for el in root.findall('QUERY'):
    start_time = time.time()
    total_query = total_query + 1
    num = int(el.find('QueryNumber').text)
    text = str(el.find('QueryText').text).upper()
    abstract = unidecode(text)
    tokenized = nltk.word_tokenize(abstract)
    tokens = {}
    # obtem tokens da query
    for token in tokenized:
        word = re.sub('[^A-Z]', '', token)
        if len(word) > 1:
            tokens[word] = 1
    # cria o vetor da query
    #query_vec = [0 for x in range(total_words)]
    query_vec = {}
    # atribui pesos no vetor
    for key in tokens:
        # palavras na consulta podem nao ter sido indexadas
        if key in words_dict:
            query_vec[words_dict[key]] = 1
    results = []
    for doc_id, value in dict_doc_word.items():
        doc = doc_id
        # cria o vetor do documento
        #doc_vec = [0 for x in range(total_words)]
        #for word_key, word_f in dict_doc_word[doc].items():
        #    doc_vec[word_key] = word_f
        doc_vec = dict_doc_word[doc]
        #sim = cosine_similarity([query_vec], [doc_vec])
        sim = cos_sim(query_vec, doc_vec)
        #print(key + ' ' + str(sim)) #if sim > 0.7071:
        #results.append([doc_id, sim[0][0]])
        results.append([doc_id, sim])
    results.sort(key=lambda x: x[1], reverse=True)
    results = results[:100]
    to_res = []
    for i in range(len(results)):
        res = [(i+1)]
        res.extend(results[i])
        to_res.append(res)
    to_save.append([num, to_res])
    total_time = total_time + time.time() - start_time

logging.info('Finalizado processo de busca')
logging.info('Tempo total de processamento: '+str(total_time)+' segundos')
logging.info('Processamento médio por consulta: '+str(total_time/total_query)+' segundos')

logging.info('Salvando arquivo de resultado de busca')
# salvando dict de tokens, dict de documents e matriz em arquivo
with open(file_result, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerows(to_save)
logging.info('Arquivo de busca salvo')