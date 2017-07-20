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
relevantes = [[] for i in range(101)]
recuperados = {'porter' : [[] for i in range(101)], 'no_porter': [[] for i in range(101)]}
precision = {'porter' : [None for i in range(101)], 'no_porter': [None for i in range(101)]}
recall = {'porter' : [None for i in range(101)], 'no_porter': [None for i in range(101)]}

with open(files_read, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if len(row):
            #esperados.append({'QueryNumber': row[0], 'DocNumber': row[1], 'DocVotes': row[2]})
            try:
                relevantes[int(row[0])].append(int(row[1]))
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
                        if r[2] > 0.1: # documents with cos_sim greater than 0.1 are considered relevant
                            rec.append(r[1])
                        #rec.append(r[1]) # returns always 100 documents
                    recuperados[tp][int(row[0])] = rec
                except:
                    pass
                
for tp in ['porter', 'no_porter']:
    for i in range(1, 101):
        rel = set(relevantes[i])
        rec = set(recuperados[tp][i])
        rel_rec = len(rel.intersection(rec))
        total_rel = len(rel)
        total_rec = len(rec)
        try:
            precision[tp][i] = rel_rec / (1.0*total_rec)
            recall[tp][i] = rel_rec / (1.0*total_rel)
        except:
            # query number 93 does not exist
            pass

#s = 0.0
#for i in precision['no_porter']:
#    if i is not None:
#        s += i       
#print(s/100.0)
X = []
y = []
for i in recall['no_porter']:
    if i is not None:
        X.append(i)
for i in precision['no_porter']:
    if i is not None:
        y.append(i)

X = sorted(X)
y = sorted(y, reverse=True)
# Plot Precision-Recall curve
plt.clf()
plt.plot(X, y, lw=2, color='navy', label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
#plt.title('Precision-Recall example: AUC={0:0.2f}'.format(average_precision[0]))
plt.legend(loc="lower left")
plt.show()