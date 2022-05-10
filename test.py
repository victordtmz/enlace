from globalElements.setup import load
load()
import sys
import os
from PyQt6.QtWidgets import (QApplication)
from PyQt6.QtCore import Qt
from globalElements.treeview import treeviewSearchBox
from globalElements.widgets import standardItem
from globalElements import constants

class main(treeviewSearchBox):
    def __init__(self, fontSize=13, sortColumn=1, sortOrder=Qt.SortOrder.AscendingOrder):
        super().__init__(fontSize, sortColumn, sortOrder)
        self.rootFolder = f'{constants.oneDrive}\Despacho\Enlace_servicios'
        # self.rootFolder = f'{constants.oneDrive}\Despacho\Traducciones\Traducciones'

        self.getFiles(self.rootFolder, self.rootNode)
        self.treeview.setRootIsDecorated(True)
        # self.treeview.header().hide()
        self.treeview.setAllColumnsShowFocus(True)
    
    def getFiles(self, path, node):
        # mainFolder = self.rootNode
        
        for folder in os.scandir(path):
            if folder.is_dir():
                for subFolder in os.scandir(folder):
                    record = (folder.name, subFolder.name)
                    record = list(map(self.createRecord, record))
                    node.appendRow(record)


            # type_ = entry.name
            # record = []
            # if entry.is_dir():
            #     record.append(type_)
            #     for entry in os.scandir(entry):
            #         if entry.is_dir():
            #             record.append(entry.name)
            #             record = list(map(self.createRecord, record))
            #             node.appendRow(record)

            #     # record = self.createRecord(name)
            #     # node.appendRow(record)
            # else:
            #     record = self.createRecord(name)
            #     node.appendRow(record)
            #     # mainFolder = record
            #     self.getFiles(entry, record)

        # for dirpath,dirnames,files in  os.walk(self.rootFolder):
        #     pass

    def addRecords(self, records, fontSize=13, rowHeight=42, colorVar='#000000'):
        if records:
            for r in records:
                stdItemItem = list(map(lambda x: standardItem(str(x),fontSize,rowHeight,colorVar),r))
                self.rootNode.insertRow(0, stdItemItem)
    
    def createRecord(self, text, fontSize=13, rowHeight=42, colorVar='#000000'):
        record = standardItem(text, fontSize, rowHeight,colorVar)
        return record


    def requery(self, records, sizeVar=13, rowHeight=42, colorVar='#000000'):
                 
        return super().requery(records, sizeVar, rowHeight, colorVar)


 
if __name__ == '__main__':
    # db = main.main()
    # db.createDB()
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())
    # app = cloneDb.Clone()
    # app.cloneDB() 
    #o! SQLITE TESTING
    db = main.DB()
    # db.cloneDB()