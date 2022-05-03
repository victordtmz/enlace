from globalElements import constants, functions as gf
from localDB import mainModel
from globalElements.widgets import labelWidget,  lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone
from distutils import ccompiler
import imp
from avdt import bookkeeping
from avdt.bookkeeping import categories
from localDB import sqliteDB
from localDB.scheduleC import scheduleC
from globalElements.widgets import cbo
from PyQt6.QtWidgets import QCompleter,QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class scheduleCbo(cbo):
    def __init__(self, fontSize =13):
        super().__init__(fontSize)
        self.db = DB()
        self.db.selectListItems()
        completer = QCompleter(self.db.list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompleter(completer)
        self.addItems(self.db.list)
        self.currentValues = []

    def populateCurrentValues(self):
        item = self.getInfo()
        record = self.db.selectByItem(item)[0]
        self.currentValues = record
        # or i in record:
        #     self.currentValues.append(i[0])

    def getDbInfo(self):
        v = self.getInfo()
        sql = f'''
            SELECT id from {self.db.tableVar}
            WHERE item = '{v}' ORDER BY item
        ''' 
        info = self.db.selectRecords(sql)[0][0]
        return info

class DB(sqliteDB.avdtLocalDB):
    def __init__(self):
        super().__init__()
        # self.configDB()
        #'id-0', 'item-1', 'itemEs-2', 'itemDesc-3'
        
        # self.sqlFolder = 'sqlite\scheduleC'
        # self.database = 'scheduleC.avd'
        
        self.dict = {}
        self.dictCbo = {}
        self.list = []
    
    def configDB(self):
        self.sqlFolder = 'localDB\scheduleC'
        self.database = 'avdt.db'
        self.tableVar = 'scheduleC'
        self.idVar = 'id'

    def selectListItems(self):
        sql = f'''
            SELECT item FROM {self.tableVar}
        '''
        records = self.selectRecords(sql)
        self.list.append('')
        for i in records:
            self.list.append(i[0])
    
    def selectDict(self):
        self.dict[""] = ""
        self.dictCbo[""] = ""
        records = self.selectAll()
        for i in records:
            self.dict[i[0]] = [i[1],i[3],i[2]]
            self.dictCbo[i[0]] = i[1]

    def selectByItem(self, txt):
        sql = f'''
            SELECT * FROM {self.tableVar}
            WHERE item = '{txt}'
        '''
        records = self.selectRecords(sql)
        return records

    def selectAll(self):
        sql = f'''
            SELECT * FROM {self.tableVar}
        '''
        records = self.selectRecords(sql)
        return records

    def createDB(self):
        records = []
        for k,v in scheduleC.scheduleC.items():
            record = [k]
            for i in v:
                record.append(i)
            records.append(record)
        sql = self.getSQL('createTable.sql')  
        self.executeQuery(sql) 
        for i in records:
            sql = f'''INSERT INTO scheduleC 
                (id, item, itemEs, itemDesc)
            VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}")
        '''
            self.executeQueryCommit(sql)


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
        self.listTableValuesIndexes = (0,1,2,3)
        # self.formToDBItems = 4
        self.titleText = "SCHEDULE C ITEMS - LOCAL DB"
        self.listWidth = 1
        self.formWidth = 1
        self.listHiddenItems = ()
        self.listColumnWidth = ((1,260),(2,120))
        self.sortColumn = 1
        self.onNewFocusWidget = 0

        
        
        # self.selectFile = f'{self.db.sqlFiles}\selectAll.sql'
        # self.
        # self.newRecordSql = f'{self.db.sqlFolder}\insertNewRecord.sql'

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                item = '{record[1]}',
                itemEs = '{record[2]}',
                itemDesc = '{record[3]}',
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
            no = self.item.getInfo()
            

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no}
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
        self.idNew = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        self.item = textEdit(self.fontSize)
        self.item.setMaximumHeight(3)
        self.itemEs = textEdit(self.fontSize)
        self.itemEs.setMaximumHeight(30)
        self.itemDesc = textEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.item, self.itemEs, self.itemDesc]
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Id New:', self.fontSize), self.idNew)

        self.layoutForm.addRow(labelWidget('Item:', self.fontSize),self.item)
        self.layoutForm.addRow(labelWidget('Español:', self.fontSize), self.itemEs)
        self.layoutForm.addRow(labelWidget('Descripcion:', 14,True,align="center"))
        self.layoutForm.addRow(self.itemDesc)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))

        self.item.textChanged.connect(lambda: self.formDirty(1,self.item.getInfo()))
        self.itemEs.textChanged.connect(lambda: self.formDirty(2,self.itemEs.getInfo()))
        self.itemDesc.textChanged.connect(lambda: self.formDirty(3,self.itemDesc.getInfo()))

    def save_record_toDb(self, newRecord):
        '''Redefined in this instance because id is not autogenerated'''
        record = self.getDBInfo()
        queryRecord = record.copy()
        queryRecord = gf.recordToSQL(queryRecord)

        if newRecord:
            id_ = self.idNew.getInfo()
            queryRecord[0] = id_
            idVar = self.insertNewRecord(queryRecord)
            # form item 0 should always hold the id value
            self.formItems[0].populate(str(idVar))
        else:
            self.updateRecord(queryRecord)

if __name__ == '__main__':
    db = DB()
    

    