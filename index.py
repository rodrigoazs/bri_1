# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:47:05 2017

@author: Rodrigo Azevedo

Modulo de indexação
"""

import time
import logging
import configparser
import re
import csv
import ast
import math

def run():
    logging.info('Modulo de indexação iniciado')
    
    config = configparser.ConfigParser()
    config.read('index.cfg')
    files_read = config.get('config', 'LEIA')
    file_write = config.get('config', 'ESCREVA')
    logging.info('Leitura do arquivo de configuração')
    
    logging.info('Iniciando processo de indexação dos dados')
    
    words_dict = {}
    words_count = 0
    new_dict = {}
    
    total_time = 0
    total_documents = 0
    
    with open(files_read, 'r') as csvfile:
        logging.info('Leitura do arquivo de dados '+str(files_read))
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # remover caracteres que nao sao do alfabeto
            if len(row):
                start_time = time.time()
                #print(ast.literal_eval(row[1]))
                word = re.sub('[^A-Z]', '', row[0])
                if len(word) > 1:
                    # passa as novas palavras para dicionario
                    # se existe agrupa os valores
                    row1 = ast.literal_eval(row[1])
                    if word in new_dict:
                        new_dict[word].extend(row1)
                    else:
                        new_dict[word] = row1
                    if word not in words_dict:
                        words_dict[word] = words_count
                        words_count = words_count + 1
                    for key in new_dict[word]:
                        total_documents = int(max(total_documents, int(key)))
                total_time = total_time + time.time() - start_time
                          
    total_words = len(words_dict)
    
    logging.info('Finalizado processo de leitura dos arquivos de dados')
    logging.info('Tempo total de processamento: '+str(total_time)+' segundos')
    logging.info('Número total de tokens unicos: '+str(total_words))
    logging.info('Processamento médio por tokens: '+str(total_time/total_words)+' segundos')
    
    # conta numero de termos em cada documento
    #tot = []
    #for key, value in new_dict.items():
    #    tot.extend(value)
    #tdf = dict([(i, tot.count(i)) for i in set(tot)])
    
    # cria a matrix do modelo vetorial termos x documentos
    #matrix = [[0 for x in range(total_documents)] for x in range(total_words)]
    # matriz ocupando muita memoria
    #matrix = [{} for x in range(total_documents)]
    dict_doc_word = {}
    
    logging.info('Atribuindo pesos tfidf a matriz')
    # preenche a matrix com tf/idf
    for key, value in new_dict.items():
        tf_dict = dict([(i, value.count(i)) for i in set(value)])
        nd = total_documents
        df = len(tf_dict)*1.0
        idf = math.log((1.0+nd)/(1.0+df)) + 1 # calculo do idf
        word_id = words_dict[key]
        for i, tf in tf_dict.items():
            document_id = i
            if document_id not in dict_doc_word:
                dict_doc_word[document_id] = {}
            dict_doc_word[document_id][word_id] = tf * idf # calculo de tf idf
            
    # l2-normalization
    for doc_id, words_value in dict_doc_word.items():
        s = 0
        for word_id, value in dict_doc_word[doc_id].items():
            s = s + value**2
        s = math.sqrt(s)
        for word_id, value in dict_doc_word[doc_id].items():
            dict_doc_word[doc_id][word_id] = value / (s * 1.0)
    
    logging.info('Atribuição de pesos finalizado')
                  
    logging.info('Salvando arquivo de resultado de indexação')
    # salvando dict de tokens, dict de documents e matriz em arquivo
    to_save = []
    with open(file_write, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        to_save.append(['TOKENS', str(words_dict)])
        to_save.append(['MODEL', str(dict_doc_word)])
        to_save.append(['REVERSE', str(new_dict)])
        writer.writerows(to_save)
    logging.info('Arquivo de indexação salvo')