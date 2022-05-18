#!/usr/bin/python3
import sys
import logging
def load():
    # ge = 'globalElements'
    paths = ['globalElements']
    for p in paths:
        if p not in sys.path:
            sys.path.insert(0,p)
load()

# class():
class logger(): 
    def __init__(self):  
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        datestr = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s Line:%(lineno)d Msg:%(message)s')
        formatter.datefmt = datestr
        file_handler = logging.FileHandler('enlace.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    
    