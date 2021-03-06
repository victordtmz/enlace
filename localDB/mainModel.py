#!/usr/bin/python3
import imp
from localDB import sqliteDB
from abc import abstractmethod
import sys 
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from globalElements.treeview import treeviewSearchBox, filesTree
from globalElements.widgets import buttonWidget, labelWidget,  deleteWarningBox, tabWidget
import html2text
from globalElements import constants, functions as gf

from globalElements import modelMain

class main(modelMain.main):
    def __init__(self):
        super().__init__()
        pass
        
    @abstractmethod
    def setDBConnection(self):
        self.db = sqliteDB.avdtLocalDB()
        # self.

    def selectAll(self): 
        # sql = self.db.getSQL(self.selectSql)#make sure sql has no ending statement
        records, labels = self.db.selectRecordsAndLabels(self.selectSql)
        self.horizontalLabels = labels
        return records 
    
    def insertNewRecord(self, record):
        r = gf.insertNewRecord(record)
        # sql = self.db.getSQL(self.newRecordSql)
        sql = f"{self.newRecordSql} ({r});"
        idVar = self.db.insertNewRecord(sql)
        return idVar

             
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())