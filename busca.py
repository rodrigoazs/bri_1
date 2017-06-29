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
            elif row[0] == 'DOCUMENTS':
                documents_dict = ast.literal_eval(row[1])
            elif row[0] == 'MODEL':
                matrix = ast.literal_eval(row[1])

xml = ET.parse(file_query)
logging.info('Leitura do arquivo de consultas '+str(file_query))
root = xml.getroot()

total_words = len(words_dict)

# transpoe a matrix em documentos x termos
t_matrix = [list(i) for i in zip(*matrix)]

for el in root.findall('QUERY'):
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
    query_vec = [0 for x in range(total_words)]
    # atribui pesos no vetor
    for key in tokens:
        # palavras na consulta podem nao ter sido indexadas
        if key in words_dict:
            query_vec[words_dict[key]] = 1
    results = []
    for key, value in documents_dict.items():
        doc_vec = t_matrix[value]
        sim = cosine_similarity([query_vec], [doc_vec])
        print(key + ' ' + str(sim))#if sim > 0.7071:
            #print(sim)
    break
            