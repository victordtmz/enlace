from localDB import mainModel
from globalElements import constants
from globalElements.treeview import treeviewSearchBox

from globalElements.widgets import (dateEdit, dateWidget, lineEditCurrency, standardItem, 
    labelWidget,  textEdit, lineEdit, spinbox, cboFilterGroup, checkBox)
from localDB import sqliteDB
from PyQt6.QtWidgets import QApplication, QCompleter
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QCursor, QCloseEvent
import pathlib
import os 
import csv
  
# tableVar = 'accounts'
class mainTree(treeviewSearchBox):
    def __init__(self, fontSize=11, sortColumn=1, sortOrder=Qt.SortOrder.AscendingOrder):
        super().__init__(fontSize, sortColumn, sortOrder)
        self.fontSize = fontSize
        self.configureTree()
        self.createFilters()
        self.getFiles(self.rootFolder, self.rootNode)

    def createFilters(self):
        self.proxyTipo = QSortFilterProxyModel()
        self.filterTipo = cboFilterGroup(self.fontSize,
        refreshable=False)
        self.layoutFilter.insertRow(0, labelWidget('Tipo:', self.fontSize), self.filterTipo)
        self.filterTipo.cbo.currentTextChanged.connect(self.applyFilterTipo)
    
    def configureTree(self):
        # self.getFiles(self.rootFolder, self.rootNode)
        # self.treeview.setRootIsDecorated(True)
        # self.treeview.setAllColumnsShowFocus(True)
        self.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        self.setColumnsWith(((0,110),(2,200)))
        self.rootFolder = f'{constants.oneDrive}\Despacho\Enlace_servicios'

    def getFiles(self, path, node):
        tipoFolders = ['']
        for folder in os.scandir(path):
            if folder.is_dir():
                #add items for filter 
                tipoFolders.append(folder.name)
                for subFolder in os.scandir(folder):
                    record = (folder.name, subFolder.name)
                    record = list(map(self.createRecord, record))
                    node.appendRow(record)
        #config filter
        tipoFolders.sort()
        self.filterTipo.cbo.addItems(tipoFolders)
        completer = QCompleter(tipoFolders)
        self.filterTipo.cbo.setCompleter(completer)

    def createRecord(self, text, rowHeight=42, colorVar='#000000'):
        record = standardItem(text, self.fontSize, rowHeight,colorVar)
        return record

    def applyFilterTipo(self):
        filterText = self.filterTipo.getDbInfo()
        self.proxyTipo.setSourceModel(self.standardModel)
        self.proxyTipo.setFilterFixedString(filterText)
        self.proxyTipo.setFilterKeyColumn(0)

        self.proxyModel.setSourceModel(self.proxyTipo)
        self.search_afterUpdate(1)

class DB(sqliteDB.avdtLocalDB): 
    def __init__(self): 
        self.database = 'registros.avd'
        self.tableVar = 'registros'
        
        self.createTableSql = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.tableVar} (
            id INTEGER PRIMARY KEY,
            date_ TEXT,
            description_ TEXT,
            file_ TEXT
            )
            --endsql'''
        # self.dbFolder = f'{constants.rootAVDT}\Carriers'

class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.listFontSize = 11
        self.rowHeight = 72
        self.configure_form()
        self.setConnections()
        self.configure_mainList()
        
    def configure_mainList(self):
        self.mainList = mainTree()
        self.splitter.insertWidget(0,self.mainList)
        self.mainFormOpt = checkBox('Expedientes',fontSize=self.fontSize, size=self.mainSize)
        self.mainFormOpt.setChecked(True)
        self.widgetsOpt.insert(0,self.mainFormOpt)# = [self.mainFormOpt,self.listOpt, self.formOpt]
        self.titleLayout.insertWidget(1, self.mainFormOpt)
        self.mainFormOpt.toggled.connect(self.configureWidth)
        
        self.filesFolder.root = self.mainList.rootFolder
        self.mainList.treeview.selectionModel().selectionChanged.connect(self.requery)
        

    def setDBConnection(self):
        self.db = DB()
        self.tableVar = self.db.tableVar
        self.db.dbFolder = ''


    def setGlobalVariables(self):
        # DB INFO
        self.idLoad = 0
        self.setDBConnection()
        self.evaluateSaveIndex = (2,)
        self.loadFolder = ''
        self.size_ = "h1" 
        self.idColumn = 'id' 
        self.listTableValuesIndexes = (0,1,2,3)
        # self.formToDBItems = 4
        self.titleText = "JUICIOS Y TRAMITES"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1,1]
        self.listHiddenItems = (0,3)
        self.listColumnWidth = ((1,120),(2,120))
        self.sortColumn = 1
        self.onNewFocusWidget = 0
        self.selectSql = f'''
        --sql
        SELECT
            id,
            date_ AS "No.",
            description_ AS "Descripcion",
            file_ AS "Archivo"
        FROM {self.tableVar};
        '''
        
        self.newRecordSql = f'''INSERT INTO {self.tableVar} (date_, description_, file_) VALUES '''
            
    
    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        if self.mainList.treeview.selectionModel().hasSelection():
            expediente = self.mainList.treeview.selectedIndexes()
            fileFolder = f'{expediente[0].data()}\{expediente[1].data()}'
            self.db.dbFolder = f'{self.mainList.rootFolder}\{fileFolder}'
            self.filesFolder.txtFilePath.setText(self.db.dbFolder)
            self.db.dbFolder = f'{self.db.dbFolder}\desgloce'

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
                self.configureColumns()
            else:
                self.list.removeAllRows()
        else:
            self.list.removeAllRows()
        
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()


    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                date_ = '{record[1]}',
                description_ = '{record[2]}',
                file_ = '{record[3]}'
                WHERE id =  {record[0]};'''
        self.db.executeQueryCommit(sql)
    
    def configure_form(self): 
        self.formLayoutSideFilesTree()
        self.filesFolder.setLineEditFileBox(self.fontSize)
        
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        # self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        # self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.date = dateWidget(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.anexoBox = self.filesFolder.layoutLineEditFileBox
        self.anexo = self.filesFolder.lineEditItems.txt 


        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.date, self.description, self.anexo]
        
        self.layoutForm.addRow(self.anexoBox)
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.date)
        self.layoutForm.addRow(labelWidget("Notes", 14, fontColor="Blue", align="center"))
        self.layoutForm.addRow(self.description)
    
    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            date_ = self.date.getInfo()
            desc = self.description.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {date_}
            Item: {desc}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        # self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.date.dateEdit.dateChanged.connect(lambda: self.formDirty(1, self.date.getInfo))
        self.description.textChanged.connect(lambda: self.formDirty(2, self.description.getInfo))
        self.anexo.textChanged.connect(lambda: self.formDirty(3, self.anexo.getInfo))

    
    def closeEvent(self, a0: QCloseEvent):
        # self.save_record_main(False, False)#updateList, changedSelection
        return super().closeEvent(a0)

    def listadoSelectionChanged(self):
        return super().listadoSelectionChanged()
        
    

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