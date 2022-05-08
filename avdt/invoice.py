from localDB import mainModel
from globalElements import constants
from globalElements.widgets import (lineEditCurrency, webWidget, 
    dateWidget, labelWidget,  textEdit, lineEdit, spinbox, cboFilterGroup)
from localDB import sqliteDB
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
import pathlib
import os
  
# tableVar = 'accounts'
class DB(sqliteDB.avdtLocalDB): 
    def __init__(self): 
        # self.dict = {}
        # self.list = []
        self.createTableSql = f'''
        CREATE TABLE IF NOT EXISTS {self.tableVar} (
            id INTEGER PRIMARY KEY,
            no_ TEXT,
            item TEXT,
            amount REAL,
            notes TEXT
            )
        '''
        # self.sqlFolder = 'globalElements\\accounts'
        self.database = 'invoice.avd'
        self.tableVar = 'invoice'
        # self.dbFolder = f'{constants.rootAVDT}\Carriers'

class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.configure_form()
        self.setConnections()
        self.setDBConnection()

    def setDBConnection(self):
        self.db = DB()
        self.tableVar = self.db.tableVar

    def setGlobalVariables(self):
        # DB INFO
        self.loadFolder = ''
        self.size_ = "h1" 
        self.idColumn = 'id' 
        self.listTableValuesIndexes = (0,1,2,3,4,5,6)
        # self.formToDBItems = 4
        self.titleText = "ACCOUNTS"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (0,3,4,5,6)
        self.listColumnWidth = ((1,320),(2,250))
        self.sortColumn = 1
        self.onNewFocusWidget = 0
        self.selectSql = f'''
        SELECT
            id,
            no_ AS "No.",
            item AS "Item",
            amount AS "Amount",
            notes AS "Notes"
        FROM {self.tableVar};'''
        self.newRecordSql = '''
            INSERT INTO accounts (no_, item, amount, notes) VALUES 
        '''
    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.db.dbFolder = f'{self.loadFolder}\invoice'
        try:
            records = self.selectAll()
        except:
            folder = pathlib.Path(self.db.dbFolder)
            if not folder.exists():
                os.mkdir(self.db.dbFolder)
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


    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                no_ = '{record[1]}',
                item = '{record[2]}',
                amount = '{record[3]}',
                notes = '{record[4]}'
                WHERE id =  {record[0]};'''
        self.db.executeQueryCommit(sql)
    
    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            no_ = self.no_.getInfo()
            item = self.item.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no_}
            Item: {item}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        # self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        # self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        self.idLoad_ = lineEdit(self.fontSize)
        self.idLoad_.setReadOnly(True)
 
        self.no_ = spinbox(self.fontSize)
        self.no_.setMinimum(1)

        self.item = cboFilterGroup(
            self.fontSize, 
            refreshable=False, 
            items= ["", "Line haul", "Detention", "Layover", "Lumper"],
            clearFilter=False
        )

        self.amount = lineEditCurrency(self.fontSize)
        self.notes = textEdit(self.fontSize)


        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [
            self.id_, 
            self.idLoad_,
            self.no_,
            self.item, 
            self.amount,
            self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdLoad:', self.fontSize), self.idLoad_)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.no_)
        self.layoutForm.addRow(labelWidget('Item:', self.fontSize), self.item)
        self.layoutForm.addRow(labelWidget('Amount:', self.fontSize), self.amount)
        self.layoutForm.addRow(labelWidget("Notes", 14, fontColor="Blue", align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.no_.textChanged.connect(lambda: self.formDirty(2, self.no_.getInfo))
        self.item.cbo.currentTextChanged.connect(lambda: self.formDirty(3, self.item.getInfo))
        self.amount.textChanged.connect(lambda: self.formDirty(4, self.amount.getInfo))
        self.notes.textChanged.connect(lambda: self.formDirty(5, self.notes.getInfo()))
        self.btnNew.pressed.connect(self.createNewRecord)

    def createNewRecord(self):
        if self.idLoad:
            self.idLoad_.setText(str(self.idLoad))

if __name__ == '__main__':
    db = DB()
    

    


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