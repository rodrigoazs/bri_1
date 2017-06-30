# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:34:55 2017

@author: Rodrigo Azevedo

Modulo de buscador
"""

#import time
import logging
import configparser
import xml.etree.ElementTree as ET
import re
import csv
import ast
#import math
from unidecode import unidecode
import nltk
from sklearn.metrics.pairwise import cosine_similarity

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

xml = ET.parse(file_query)
logging.info('Leitura do arquivo de consultas '+str(file_query))
root = xml.getroot()

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

for el in root.findall('QUERY'):
    num = int(el.find('QueryNumber').text)
    print('para consulta' + str(num))
    text = str(el.find('QueryText').text).upper()
    abstract = unidecode(text)
    tokenized = nltk.word_tokenize(abstract)
    tokens = {}
    print(tokenized)
    # obtem tokens da query
    for token in tokenized:
        word = re.sub('[^A-Z]', '', token)
        if len(word) > 1:
            tokens[word] = 1
    # cria o vetor da query
    query_vec = [0 for x in range(total_words)]
    # atribui pesos no vetor
    for key in tokens:
        # palavras na consulta podem nao ter sido indexadas
        if key in words_dict:
            query_vec[words_dict[key]] = 1
    results = []
    for doc_id, value in dict_doc_word.items():
        doc = doc_id
        # cria o vetor do documento
        doc_vec = [0 for x in range(total_words)]
        for word_key, word_f in dict_doc_word[doc].items():
            doc_vec[word_key] = word_f
        sim = cosine_similarity([query_vec], [doc_vec])
        #print(key + ' ' + str(sim)) #if sim > 0.7071:
        results.append([doc_id, sim[0][0]])
    results.sort(key=lambda x: x[1], reverse=True)
    print(results[:100])
    break
            