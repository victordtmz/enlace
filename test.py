from globalElements.setup import load
load()
import sys
import os
from PyQt6.QtWidgets import (QApplication)
from PyQt6.QtCore import Qt
from globalElements.treeview import treeviewSearchBox
from globalElements.widgets import standardItem
from globalElements import constants
from localDB.states import estados
from enlace.traducciones01 import traduccionesCopyDB

# class main(treeviewSearchBox):
#     def __init__(self, fontSize=13, sortColumn=1, sortOrder=Qt.SortOrder.AscendingOrder):
#         super().__init__(fontSize, sortColumn, sortOrder)



 
if __name__ == '__main__':
    # db = main.main()
    # db.createDB()
    # app = QApplication(sys.argv)
    # mw = USCopy.DB()
    # mw.show()
    # sys.exit(app.exec())
    # app = cloneDb.Clone()
    # app.cloneDB() 
    #o! SQLITE TESTING
    traduccionesCopyDB.cloneDB()
    # db.C
    # db.selectEstados('México')
    # db.selectCiudades('México', 'Guanajuato')
    # db.createTable()
    # db.cloneDB()