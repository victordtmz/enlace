import sys

def load():
    # ge = 'globalElements'
    paths = ['globalElements']
    for p in paths:
        if p not in sys.path:
            sys.path.insert(0,p)
    
    