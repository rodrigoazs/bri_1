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
models = ['porter', 'no_porter']
#esperados = []
relevants = {}
retrieveds = {'porter' : {}, 'no_porter': {}}

# obtem os itens relevantes de cada consulta
with open(files_read, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if len(row):
            try:
                if int(row[0]) in relevants:
                    relevants[int(row[0])].append(int(row[1]))
                else:
                    relevants[int(row[0])] = [int(row[1])]
            except:
                pass

# obtem os itens retornados em ordem de cada consulta       
for model in models:
    files_read = '../results_'+ model +'/busca_result.csv'
    with open(files_read, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row):
                try:
                    rec = []
                    row1 = ast.literal_eval(row[1])
                    for r in row1:
                        rec.append(r[1]) # returns all of them
                    retrieveds[model][int(row[0])] = rec
                except:
                    pass
                
n_queries = len(relevants)
n_documents = len(retrieveds['porter'][1])

# calcula precision e recall para cada query      
precisions = {'porter' : np.zeros((n_queries, n_documents)), 'no_porter': np.zeros((n_queries, n_documents))}
recalls = {'porter' : np.zeros((n_queries, n_documents)), 'no_porter': np.zeros((n_queries, n_documents))} 
     
for model in models:
    m = 0
    for key, value in retrieveds[model].items():
        rel = len(relevants[key])
        rel_retrieved = 0
        for k in range(len(value)):
            if value[k] in relevants[key]:
                rel_retrieved += 1
            precisions[model][m][k] = rel_retrieved / (1.0*(k + 1))
            recalls[model][m][k] = rel_retrieved / (1.0*rel)
        m += 1

# calculado o maximo a direita nos precisions
for model in models:
    for i in range(len(precisions[model])):
        for j in range(len(precisions[model][i])-1, 0, -1):
            if precisions[model][i][j] > precisions[model][i][j-1]:
                precisions[model][i][j-1] = precisions[model][i][j]

# calculos interpolado nos 11 pontos  
interpolated_prec_recs_each =  {'porter' : np.zeros((n_queries, 11)), 'no_porter': np.zeros((n_queries, 11))}
interpolated_prec_recs =  {'porter' : np.zeros(11), 'no_porter': np.zeros(11)}

for model in models:
    for q in range(n_queries):
        prec = precisions[model][q]
        rec = recalls[model][q]
        for recall_in_level in range(0, 11):
            prec_at = 0
            for k in range(n_documents):
                if recall_in_level <= rec[k] * 10:
                    prec_at = max(prec_at, prec[k])
            interpolated_prec_recs_each[model][q][recall_in_level] = prec_at
    interpolated_prec_recs[model] = np.mean(interpolated_prec_recs_each[model], axis = 0)
    
    
# calculos interpolado nos 11 pontos (medias antes)          
#interpolated_prec_recs = {'porter' : None, 'no_porter': None}
#for model in models:
#    prec = precisions[model]
#    rec = recalls[model]
#    mean_precisions = np.mean(prec, axis = 0)
#    mean_recalls = np.mean(rec, axis = 0)
#    
#    interpolated_precision_recall = np.zeros(11)
#    
#    for recall_in_level in range(0, 11):
#        precision_at_k = 0
#        for k in range(len(mean_recalls)):
#            if recall_in_level <= mean_recalls[k] * 10:
#                precision_at_k = max(precision_at_k, mean_precisions[k])
#        interpolated_precision_recall[recall_in_level] = precision_at_k
#    interpolated_prec_recs[model] = interpolated_precision_recall

# plot 11 interpolated precision recall curve
rec_x = np.arange(0, 1.1, 0.1) # the x locations for the groups

for model in models:
    label = 'Com Porter Stemming' if model == 'porter' else 'Sem Porter Stemming'
    plt.plot(rec_x, interpolated_prec_recs[model], label=label)

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title("Curva de Precision-Recall interpolado em 11 níveis")
plt.legend(loc='upper right')

plt.subplots_adjust(bottom=0.2)
plt.show()