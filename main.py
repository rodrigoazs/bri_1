# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:28:29 2017

@author: Rodrigo Azevedo
"""

import logging
import gli

def main():
    logging.basicConfig(filename='module.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

if __name__ == "__main__":
    main()
