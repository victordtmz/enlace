#!/usr/bin/python3
from setup import load
load() 
import sys
from globalElements.treeview import treeviewSearchBox
from PyQt6.QtWidgets import QApplication

class main(treeviewSearchBox):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())