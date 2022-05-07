from globalElements import constants
from globalElements.accounts import main as accounts
from localDB import mainModel
from globalElements.widgets import (lineEditCopy, webWidget, dateWidget, 
    labelWidget,  textEdit, lineEdit, cboFilterGroup)
import pathlib
import os 
from localDB import sqliteDB
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
# from globalElements import DB as mysqlDb 

class main(accounts.main):
    def __init__(self):
        super().__init__()
        # self.dbFolder = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        
        self.configure_list()
        self.requery()

    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.db.dbFolder = f'{constants.rootAVDT}\Carriers'
        carrier = self.clientFiltros.getInfo()
        self.db.dbFolder = f'{self.db.dbFolder}\{carrier}\Accounts'
        # self.db.createSqliteConnection()
        try:
            records = self.selectAll()
        except:
            # sql = self.db.getSQL('createTable.sql')
            self.db.executeQuery(self.db.createTableSql)
            records = self.selectAll()

        if records:
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
        else:
            self.list.removeAllRows()
        self.configureColumns()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()
        
    def queryCarriers(self):
        if not constants.carriersItems:
            constants.queryCarriers()
        self.carriers = constants.carriersItems.copy()
        self.carriers.pop(0)

    def configure_list(self):
        self.listFontSize = 13
        self.queryCarriers()
        filterSize = 13
        self.clientFiltros = cboFilterGroup(self.fontSize,
            refreshable=False,
            items= self.carriers,
            requeryFunc= self.queryCarriers)

        self.list.layoutFilter.insertRow(0, labelWidget('Client:', filterSize), self.clientFiltros)
        self.clientFiltros.cbo.currentIndexChanged.connect(self.requery)
        

            
    # def configure_form(self): 
    #     self.formLayoutSideFilesTree()
    #     self.layoutFormBox.setMinimumWidth(450)
    #     self.layoutFormBox.setMaximumWidth(500)
    #     self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.account = lineEdit(self.fontSize)
        self.user = lineEditCopy(self.fontSize)
        self.pwd = lineEditCopy(self.fontSize)
        self.date_ = dateWidget(self.fontSize)
        self.portal = webWidget(10)
        self.notes = textEdit(self.fontSize)
        self.notes.setMinimumHeight(300)
        self.formItems = [self.id_, self.account, self.user,
            self.pwd, self.date_, self.portal, self.notes]

        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Account:', self.fontSize), self.account)
        self.layoutForm.addRow(labelWidget('User:', self.fontSize), self.user)
        self.layoutForm.addRow(labelWidget('Password:', self.fontSize), self.pwd)
        self.layoutForm.addRow(labelWidget('Date:', self.fontSize), self.date_)
        self.layoutForm.addRow(labelWidget('Portal:', self.fontSize), self.portal)
        self.layoutForm.addRow(labelWidget('Notes', 14,True, align="center"))
        self.layoutForm.addRow(self.notes)
        
    # def setConnections(self):
    #     self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
    #     # self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
    #     self.account.textChanged.connect(lambda: self.formDirty(1,self.account.getInfo()))
    #     self.user.lineEdit.textChanged.connect(lambda: self.formDirty(2,self.user.getInfo()))
    #     self.pwd.lineEdit.textChanged.connect(lambda: self.formDirty(3,self.pwd.getInfo()))
    #     self.date_.dateEdit.dateChanged.connect(lambda: self.formDirty(4,self.date_.getInfo()))
    #     self.portal.lineEdit.textChanged.connect(lambda: self.formDirty(5,self.portal.getInfo()))
    #     self.notes.textChanged.connect(lambda: self.formDirty(6,self.notes.getInfo()))

        # LIST CONNECTIONS
        

    def setFilesFolder(self):
        carrier = self.clientFiltros.cbo.currentText()
        account = self.account.text()
        if carrier and account:
            folderPath = f'{self.filesFolder.root}/{carrier}/Accounts/{account}'
            self.filesFolder.txtFilePath.setText(folderPath)
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
                self.filesFolder.txtFilePath.setText('folderPath')
                self.filesFolder.txtFilePath.setText(folderPath)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)

    


 #p! DO NOT DELETE - SAMPLE CODE FOR CLONING INTO DB
    # def cloneDB(self):
    #     dbLogin = constants.avdOld
    #     dataBase = mysqlDb.DB(dbLogin[0],dbLogin[1],dbLogin[2])
    #     sql = f'''
    #         SELECT 
    #             accountName,
    #             userName,
    #             pwd,
    #             date_,
    #             portal,
    #             notes
    #         FROM AVDT_Accounts
    #         WHERE idCarrier = 1;
    #     '''
    #     records = dataBase.get_records_clearNull(sql)
    #     # records = gf.recordToSQL(records)
    #     self.database = 'dnpfAct.db'
    #     sql = self.getSQL('createTable.sql')
    #     self.executeQuery(sql)
    #     missing = []
    #     missed = 0
    #     recorded = 0
    #     for i in records:
    #         # i = gf.recordToSQL(i)
    #         sql = f'''INSERT INTO {self.tableVar} 
    #             (account, user, pwd, date_, portal, notes)
    #         VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}","{i[4]}","{i[5]}")
    #     ''' 
    #         try:
    #             self.executeQueryCommit(sql)
    #             recorded += 1
    #         except:
    #             # print(sql)
    #             missing.append([i[0],i[1]])
    #             missed += 1
                
    #     for i in missing:
    #         print(i)
    #     print(missed)