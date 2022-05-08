from globalElements import constants, functions as gf
from localDB import mainModel
from globalElements.widgets import labelWidget,  lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone
from distutils import ccompiler
import imp
from avdt import bookkeeping_
from avdt.bookkeeping_ import categories
from localDB import sqliteDB
from localDB.scheduleC import scheduleC
from globalElements.widgets import cbo
from PyQt6.QtWidgets import QCompleter,QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

# class scheduleCbo(cbo):
#     def __init__(self, fontSize =13):
#         super().__init__(fontSize)
#         self.db = DB()
#         self.db.selectListItems()
#         completer = QCompleter(self.db.list)
#         completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
#         self.setCompleter(completer)
#         self.addItems(self.db.list)
#         self.currentValues = []

#     def populateCurrentValues(self):
#         item = self.getInfo()
#         record = self.db.selectByItem(item)[0]
#         self.currentValues = record
#         # or i in record:
#         #     self.currentValues.append(i[0])

#     def getDbInfo(self):
#         v = self.getInfo()
#         sql = f'''
#             SELECT id from {self.db.tableVar}
#             WHERE item = '{v}' ORDER BY item
#         ''' 
#         info = self.db.selectRecords(sql)[0][0]
#         return info

class DB(sqliteDB.avdtLocalDB):
    def __init__(self):
        super().__init__()
        # self.configDB()
        #'id-0', 'carrier-1'
        self.dict = {}
        self.list = []
    
    def configDB(self):
        self.sqlFolder = 'localDB\\bAccounts'
        self.database = 'bAccounts.avd'
        self.tableVar = 'accounts'
        # self.idVar = 'id'

    # def selectListItems(self):
    #     sql = f'''
    #         SELECT item FROM {self.tableVar}
    #     '''
    #     records = self.selectRecords(sql)
    #     self.list.append('')
    #     for i in records:
    #         self.list.append(i[0])
    
    def selectDict(self):
        # self.dict[""] = ""
        self.list.append('')
        records = self.selectAll()
        for i in records:
            self.list.append(i[2])
            self.dict[i[2]] = i[1]

    # def selectByItem(self, txt):
    #     sql = f'''
    #         SELECT * FROM {self.tableVar}
    #         WHERE item = '{txt}'
    #     '''
    #     records = self.selectRecords(sql)
    #     return records

    def selectAll(self):
        sql = f'''
            SELECT * FROM {self.tableVar}
        '''
        records = self.selectRecords(sql)
        return records

    def createDB(self):
        sql = self.getSQL('createTable.sql')  
        self.executeQuery(sql) 

class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.setDBConnection()
        self.initUi()
        self.configure_form()
        self.setConnections()
        # self.setTotalsElements()
        self.requery()
        
        # self.getIdLoad()

    def setDBConnection(self):
        self.db = DB()
        self.tableVar = self.db.tableVar

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1" 
        self.idColumn = 'id' 
        self.listTableValuesIndexes = (0,1,2)
        # self.formToDBItems = 4
        self.titleText = "CARRIER BANK ACCOUNTS"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = ()
        self.listColumnWidth = ((0,80),(1,160))
        self.sortColumn = 1
        self.onNewFocusWidget = 0

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idCarrier = '{record[1]}',
                account = '{record[2]}'
                WHERE id =  {record[0]};'''
        self.db.executeQueryCommit(sql)

    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        records = self.selectAll()
        if records:
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
        else:
            self.list.removeAllRows()
        self.configureColumns()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()
        
        

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            carrier = self.carrier.getInfo()
            account = self.account.getInfo()
            text = f'''Eliminar el registro:
            id: {idVar} 
            Carrier: {carrier}
            Account.: {account}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        # self.idNew = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        if not constants.carriersList:
            constants.queryCarriers()
        self.carrier = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.carriersDict,
            requeryFunc=constants.queryCarriers)
        self.account = lineEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.carrier, self.account]
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Carrier:', self.fontSize), self.carrier)
        self.layoutForm.addRow(labelWidget('Account:', self.fontSize),self.account)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
        self.account.textChanged.connect(lambda: self.formDirty(2,self.account.getInfo()))

    # def save_record_toDb(self, newRecord):
    #     '''Redefined in this instance because id is not autogenerated'''
    #     record = self.getDBInfo()
    #     queryRecord = record.copy()
    #     queryRecord = gf.recordToSQL(queryRecord)

    #     if newRecord:
    #         id_ = self.idNew.getInfo()
    #         queryRecord[0] = id_
    #         idVar = self.insertNewRecord(queryRecord)
    #         # form item 0 should always hold the id value
    #         self.formItems[0].populate(str(idVar))
    #     else:
    #         self.updateRecord(queryRecord)

if __name__ == '__main__':
    db = DB()
    

    