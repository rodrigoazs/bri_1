# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:50:55 2017

@author: Rodrigo Azevedo

Modulo de geração de lista inversa
"""

import time
import logging
import configparser
import xml.etree.ElementTree as ET
#import re
import csv
from unidecode import unidecode
import nltk
#nltk.download('all')

#logging.basicConfig(filename='module.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
#logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.info('Modulo de geração de lista invertida iniciado')

config = configparser.ConfigParser()
config.read('gli.cfg')
files_read = config.get('config', 'LEIA').split(",")
file_write = config.get('config', 'ESCREVA')
logging.info('Leitura do arquivo de configuração')

logging.info('Iniciando processo de leitura e tokenizacao dos arquivos de dados')

total_time = 0
total_records = 0
tokens = {}

for i in range(len(files_read)):
    xml = ET.parse(files_read[i])
    logging.info('Leitura do arquivo de dados '+str(files_read[i]))
    root = xml.getroot()
    
    #abstracts = []
    #abstracts_tokenized = []
    #recordnums = []

    for el in root.findall('RECORD'):
        total_records = total_records + 1
        start_time = time.time()
        # alguns nao tem abstract nem extract
        if el.find('ABSTRACT') is not None or el.find('EXTRACT') is not None:
            num = int(el.find('RECORDNUM').text)
            #recordnums.append(num)
            abstract = str(el.find('ABSTRACT').text).upper() if el.find('ABSTRACT') is not None else str(el.find('EXTRACT').text).upper()
            # remove ; para evitar conflito com delimitador
            #abstract = re.sub(';', ' ', unidecode(abstract)) # unidecode remove acentos
            abstract = unidecode(abstract)
            #abstracts.append(abstract)
            tokenized = nltk.word_tokenize(abstract)
            #abstracts_tokenized.append(tokenized)
            for i in range(len(tokenized)):
                if tokenized[i] in tokens:
                    tokens[str(tokenized[i])].append(num)
                else:
                    tokens[str(tokenized[i])] = [num]            
        else:
            logging.warning('Dado de recordnum '+str(int(el.find('RECORDNUM').text))+' nao possui abstract ou extract')
        total_time = total_time + time.time() - start_time
        
logging.info('Finalizado processo de leitura e tokenizacao dos arquivos de dados')
logging.info('Tempo total de processamento: '+str(total_time)+' segundos')
logging.info('Número total de documentos (record): '+str(total_records))
logging.info('Processamento médio por documento (record): '+str(total_time/total_records)+' segundos')


#words = []          
#for abstract in abstracts:
#    words.extend(nltk.word_tokenize(abstract))
    
#result_dict = dict( [ (i, words.count(i)) for i in set(words) ] )
#unique_words = set(words)

logging.info('Total de '+str(len(tokens))+' tokens')

logging.info('Salvando arquivo de resultado de tokens')
# salvando tokens em arquivo
to_save = []
with open(file_write, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    for key, value in tokens.items():
        to_save.append([key, value])
    writer.writerows(to_save)
    
logging.info('Arquivo de tokens salvo')