# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:28:29 2017

@author: Rodrigo Azevedo
"""

import logging
import gli
import index
import busca
import pc
    
def main():
    logging.basicConfig(filename='module.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    gli.run(EnablePorterStemmer = True)
    index.run()
    busca.run(EnablePorterStemmer = True)
    pc.run()

if __name__ == "__main__":
    main()

