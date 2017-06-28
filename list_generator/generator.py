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
#from unidecode import unidecode
import nltk
#nltk.download('all')
#nltk.word_tokenize("Tokenize me")

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

#logging.basicConfig(filename='example.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.info('Modulo de geração de lista invertida iniciado')

config = configparser.ConfigParser()
config.read('gli.cfg')
files_read = config.get('config', 'LEIA').split(",")
files_write = config.get('config', 'ESCREVA')
logging.info('Leitura do arquivo de configuração')

logging.info('Iniciando processo de leitura dos arquivos de dados')
for i in range(len(files_read)):
    xml = ET.parse(files_read[i])
    logging.info('Leitura do arquivo de dados '+str(files_read[i]))
    root = xml.getroot()
    
    abstracts = []
    recordnums = []
    total_time = 0
    total_records = 0
    
    for el in root.findall('RECORD'):
        total_records = total_records + 1
        start_time = time.time()
        # alguns nao tem abstract nem extract
        if el.find('ABSTRACT') is not None:
            #s = str(el.find('ABSTRACT').text).upper()
            #t=unidecode(s)
            #t.encode("ascii")
            abstracts.append(str(el.find('ABSTRACT').text).upper())
            recordnums.append(int(el.find('RECORDNUM').text))
        elif el.find('EXTRACT') is not None:
            abstracts.append(str(el.find('EXTRACT').text).upper())
            recordnums.append(int(el.find('RECORDNUM').text))
        else:
            logging.warning('Dado de recordnum '+str(int(el.find('RECORDNUM').text))+' nao possui abstract ou extract')
        total_time = total_time + time.time() - start_time
        
logging.info('Finalizado processo de leitura dos arquivos de dados')
logging.info('Tempo total de processamento: '+str(total_time)+' segundos')
logging.info('Processamento médio por documento(record): '+str(total_time/total_records)+' segundos')

words = []          
for abstract in abstracts:
    words.extend(nltk.word_tokenize(abstract))
    
result_dict = dict( [ (i, words.count(i)) for i in set(words) ] )
teste = set(words)