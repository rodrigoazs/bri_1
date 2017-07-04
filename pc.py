# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:18:04 2017

@author: Rodrigo Azevedo

Modulo de processador de consultas
"""

import time
import logging
import configparser
import xml.etree.ElementTree as ET
import csv
import re
from unidecode import unidecode

def run():
    logging.info('Modulo de indexação iniciado')
    
    config = configparser.ConfigParser()
    config.read('pc.cfg')
    files_read = config.get('config', 'LEIA')
    file_query = config.get('config', 'CONSULTAS')
    file_expect = config.get('config', 'ESPERADOS')
    logging.info('Leitura do arquivo de configuração')
    
    logging.info('Iniciando processo de consultas')
    
    xml = ET.parse(files_read)
    logging.info('Leitura do arquivo de consultas '+str(files_read))
    root = xml.getroot()
    
    total_time = 0
    total_query = 0
    to_save_query = []
    to_save_expect = []
    to_save_query.append(['QueryNumber', 'QueryText'])
    to_save_expect.append(['QueryNumber', 'DocNumber', 'DocVotes'])
    
    for el in root.findall('QUERY'):
        start_time = time.time()
        total_query = total_query + 1
        num = int(el.find('QueryNumber').text)
        text = str(el.find('QueryText').text).upper()
        text = unidecode(text)
        text = re.sub(';', '', text)
        text = text.split()
        text = ' '.join(text)
        to_save_query.append([num, text])
        for rec in el.find('Records').findall('Item'):
            doc_num = int(rec.text)
            votes = 0
            score = rec.get('score')
            for i in range(len(score)):
                if int(score[i]) > 0:
                    votes = votes + 1
            to_save_expect.append([num, doc_num, votes])
        total_time = total_time + time.time() - start_time
                                           
    logging.info('Finalizado processo')
    logging.info('Tempo total de processamento: '+str(total_time)+' segundos')
    logging.info('Processamento médio por consulta: '+str(total_time/total_query)+' segundos')
                                    
    logging.info('Salvando arquivo de consultas do processador de consultas')
    with open(file_query, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(to_save_query)
    logging.info('Arquivo salvo')
    
    logging.info('Salvando arquivo de esperado do processador de consultas')
    with open(file_expect, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(to_save_expect)
    logging.info('Arquivo salvo')