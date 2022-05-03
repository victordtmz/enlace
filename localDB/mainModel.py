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

from globalElements import mainModel

class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.setDBConnection()
        
    @abstractmethod
    def setDBConnection(self):
        self.db = sqliteDB.avdtLocalDB()

    def selectAll(self):
        sql = self.db.getSQL(self.selectFile)#make sure sql has no ending statement
        records, labels = self.db.selectRecordsAndLabels(sql)
        self.horizontalLabels = labels
        return records 
    
    def insertNewRecord(self, record):
        r = gf.insertNewRecord(record)
        sql = self.db.getSQL(self.newRecordSql)
        sql = f"{sql} ({r});"
        idVar = self.db.insertNewRecord(sql)
        return idVar

             
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())