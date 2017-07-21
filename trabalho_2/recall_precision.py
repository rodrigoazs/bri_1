# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:57:19 2017

@author: 317005
"""
import time
import logging
import configparser
import xml.etree.ElementTree as ET
import re
import csv
import ast
import math
import numpy as np
import matplotlib.pyplot as plt

files_read = '../results_porter/esperados.csv'
#esperados = []
relevants = {}
retrieveds = {'porter' : {}, 'no_porter': {}}

with open(files_read, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if len(row):
            #esperados.append({'QueryNumber': row[0], 'DocNumber': row[1], 'DocVotes': row[2]})
            try:
                if int(row[0]) in relevants:
                    relevants[int(row[0])].append(int(row[1]))
                else:
                    relevants[int(row[0])] = [int(row[1])]
            except:
                pass
        
for tp in ['porter', 'no_porter']:
    files_read = '../results_'+ tp +'/busca_result.csv'
    with open(files_read, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row):
                try:
                    rec = []
                    row1 = ast.literal_eval(row[1])
                    for r in row1:
                        rec.append(r[1]) # returns all of them
                    retrieveds[tp][int(row[0])] = rec
                except:
                    pass
                
n_queries = len(relevants)
n_documents = len(retrieveds['porter'][1])

precisions = {'porter' : np.zeros((n_queries, n_documents)), 'no_porter': np.zeros((n_queries, n_documents))}
recalls = {'porter' : np.zeros((n_queries, n_documents)), 'no_porter': np.zeros((n_queries, n_documents))} 
                
for tp in ['porter', 'no_porter']:
    m = 0
    for key, value in retrieveds[tp].items():
        if(m < 5):
            print(key)
        rel = len(relevants[key])
        rel_retrieved = 0
        for k in range(len(value)):
            if value[k] in relevants[key]:
                rel_retrieved += 1
            precisions[m][k] = rel_retrieved / (1.0*(k + 1))
            recalls[m][k] = rel_retrieved / (1.0*rel)
        m += 1
                