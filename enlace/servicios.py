from cmath import exp
from localDB import mainModel
import sqlite3

from globalElements import constants, modelEmpty

from globalElements.treeview import treeviewSearchBox

from globalElements.widgets import (buttonWidget, dateEdit, dateWidget, lineEditCurrency, lineEditPhone, standardItem, 
    labelWidget,  textEdit, lineEdit, spinbox, cboFilterGroup, checkBox)
from localDB import sqliteDB
from PyQt6.QtWidgets import (QApplication, QCompleter, QWidget, QFormLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QCursor, QCloseEvent
import pathlib
import os 
import csv
  
class detailsForm(modelEmpty.main):
    def __init__(self):
        super().__init__()
        self.fontSize = 13
        self.configureForm()
        self.defVariables()
        
    
    def setGlobalVariables(self):
        self.titleText = "Detalles del Tramite"
        self.size_ = 'h2'



    def defVariables(self):
        # self.db = sqliteDB.avdtLocalDB()
        # self.db.dbFolder = ''
        # self.db.database = 'registros.avd'
        self.tableVar = 'detalles'
        
        self.createTableSql = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.tableVar} (
            id INTEGER PRIMARY KEY,
            fecha_ TEXT,
            honorarios REAL,
            honorariosEU REAL,
            descripcion TEXT
            );
        '''
        
        
        self.selectSql = f'''
        --sql
        SELECT * FROM {self.tableVar};
        '''

        
    def insertNewSql(self):
        record = self.getInfo()
        record.pop(0)
        record = str(record)
        record = record[1:-1]
        sql = f'''
        --sql
        INSERT INTO {self.tableVar} (fecha_, honorarios, honorariosEU, descripcion) VALUES ({record});'''
            
            
        return sql

    def updateRecordSql(self): 
        record = self.getInfo()
        sql =f'''
        --sql
        UPDATE {self.tableVar} SET 
            fecha_ = '{record[1]}',
            honorarios = '{record[2]}',
            honorariosEU = '{record[3]}',
            descripcion = '{record[4]}'
            WHERE id = 1;'''
        return sql

    def configureForm(self):
        self.id_ = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        self.fecha = dateWidget(self.fontSize)
        self.honorarios = lineEditCurrency(self.fontSize)
        self.honorariosEU = lineEditCurrency(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.formItems = [self.id_, self.fecha, self.honorarios,self.honorariosEU, self.description]

        self.btnSave = buttonWidget('Guardar', 'h2_', constants.iconSave)

        self.layout_ = QFormLayout()
        self.layout_.addRow(labelWidget('Id:', self.fontSize) ,self.id_)
        self.layout_.addRow(labelWidget('Actualizado:', self.fontSize) ,self.fecha)
        self.layout_.addRow(labelWidget('Pesos:', self.fontSize) ,self.honorarios)
        self.layout_.addRow(labelWidget('Dolares:', self.fontSize) ,self.honorariosEU)
        self.layout_.addRow(labelWidget("Descripcion", 14, True, fontColor="Black", align="center"))
        self.layout_.addRow(self.description)
        self.layout_.addRow(self.btnSave)

        self.layoutBox = QWidget()
        self.layoutBox.setMinimumWidth(460)
        self.layoutBox.setLayout(self.layout_)

        self.layoutmain.addWidget(self.layoutBox)
        self.layoutmain.setAlignment(self.layoutBox, Qt.AlignmentFlag.AlignHCenter)

    def populate(self, record):
        c = 0
        if record:
            for i in self.formItems:
                i.populate(str(record[c]))
                c += 1

    def getInfo(self):
        infoList = []
        for i in self.formItems:
            infoList.append(i.getInfo())
        return infoList

    def clearForm(self):
        for i in self.formItems:
            i.reSet()
           


class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.listFontSize = 11
        self.rowHeight = 72
        self.configure_form()
        self.setConnections()
        self.configure_mainList()
        self.configureDetailsForm()
        
    
    def createDetailsForm(self):
        
        if hasattr(self, 'detailsForm'):
            self.detailsForm.deleteLater()
            delattr(self, 'detailsForm')
            self.listOpt.setChecked(True)
            self.formOpt.setChecked(True)
            self.configureWidth()
        else:
            self.detailsForm = detailsForm()
            self.listOpt.setChecked(False)
            self.formOpt.setChecked(False)
            self.splitter.insertWidget(1,self.detailsForm)
            self.configureWidth()
            try:
                records = self.db.selectOne(self.detailsForm.selectSql)
                self.detailsForm.populate(records)
            except:
                self.detailsForm.clearForm()
            self.detailsForm.btnSave.pressed.connect(self.saveDetails)

    def configureDetailsForm(self):
        self.detailsFormOpt = checkBox('Detalles del Tramite',fontSize=self.fontSize, size=self.mainSize)
        self.detailsFormOpt.setChecked(False)
        self.widgetsOpt.insert(1,self.detailsFormOpt)# = [self.mainFormOpt,self.listOpt, self.formOpt]
        self.titleLayout.insertWidget(2, self.detailsFormOpt)
        self.detailsFormOpt.toggled.connect(self.createDetailsForm)

    def configure_mainList(self):
        self.mainList = mainTree()
        self.splitter.insertWidget(0,self.mainList)
        self.mainFormOpt = checkBox('Expedientes',fontSize=self.fontSize, size=self.mainSize)
        self.mainFormOpt.setChecked(True)
        self.widgetsOpt.insert(0,self.mainFormOpt)# = [self.mainFormOpt,self.listOpt, self.formOpt]
        self.titleLayout.insertWidget(1, self.mainFormOpt)
        self.mainFormOpt.toggled.connect(self.configureWidth)
        
        self.filesFolder.root = self.mainList.rootFolder
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.mainList.treeview.selectionModel().selectionChanged.connect(self.requery)

        self.btnCSV = buttonWidget('Excel', 'h1', constants.iconExcel)
        self.titleLayout.insertWidget(5, self.btnCSV)
        self.btnCSV.pressed.connect(self.recordsToCSV)
        #o! CONNECT 

    def setDBConnection(self):
        self.db = DB()
        self.tableVar = self.db.tableVar
        self.db.dbFolder = ''


    def setGlobalVariables(self):
        # DB INFO
        # self.idLoad = 0
        self.setDBConnection()
        self.evaluateSaveIndex = (2,)
        self.loadFolder = ''
        self.size_ = "h1" 
        self.idColumn = 'id' 
        self.listTableValuesIndexes = (0,1,2,3)
        # self.formToDBItems = 4
        self.titleText = "SERVICIOS DEL DESPACHO"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1,1,1]
        self.listHiddenItems = (0,3)
        self.listColumnWidth = ((1,120),(2,120))
        self.sortColumn = 1
        self.onNewFocusWidget = 0
        self.selectSql = f'''
        --sql
        SELECT
            id,
            date_ AS "Fecha",
            title AS "Titulo", 
            description_ AS "Descripcion",
            file_ AS "Archivo"
        FROM {self.tableVar};
        '''
        
        self.newRecordSql = f'''INSERT INTO {self.tableVar} (date_, title, description_, file_) VALUES '''
            
    
    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        if self.mainList.treeview.selectionModel().hasSelection():
            expediente = self.mainList.treeview.selectedIndexes()
            self.title.setText(expediente[1].data())
            fileFolder = f'{expediente[0].data()}\{expediente[1].data()}'
            self.db.dbFolder = f'{self.mainList.rootFolder}\{fileFolder}'
            self.filesFolder.txtFilePath.setText(self.db.dbFolder)
            self.db.dbFolder = f'{self.db.dbFolder}\desgloce'

            #populate list of items
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

            #populate details
            if hasattr(self, 'detailsForm'):
                # records = self.db.selectOne(self.detailsForm.selectSql)
                # self.detailsForm.populate(records)
                try:
                    records = self.db.selectOne(self.detailsForm.selectSql)
                    self.detailsForm.populate(records)
                except:
                    self.detailsForm.clearForm()

        else:
            self.list.removeAllRows()
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()


    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                date_ = '{record[1]}',
                title = '{record[2]}',
                description_ = '{record[3]}',
                file_ = '{record[4]}'
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
        self.title_ = lineEdit(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.anexoBox = self.filesFolder.layoutLineEditFileBox
        self.anexo = self.filesFolder.lineEditItems.txt 


        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.date, self.title_, self.description, self.anexo]
        
        self.layoutForm.addRow(self.anexoBox)
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Fecha:', self.fontSize), self.date)
        self.layoutForm.addRow(labelWidget('Titulo:', self.fontSize), self.title_)
        self.layoutForm.addRow(labelWidget("Descripcion", 14, True, fontColor="Black", align="center"))
        self.layoutForm.addRow(self.description)
    
    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            date_ = self.date.getInfo()
            title = self.title_.getInfo()
            desc = self.description.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            Fecha: {date_}
            Titulo: {title}
            Item: {desc}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        # self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.title_.textChanged.connect(lambda: self.formDirty(1, self.title_.getInfo()))
        self.date.dateEdit.dateChanged.connect(lambda: self.formDirty(2, self.date.getInfo))
        self.description.textChanged.connect(lambda: self.formDirty(3, self.description.getInfo))
        self.anexo.textChanged.connect(lambda: self.formDirty(4, self.anexo.getInfo))


    def recordsToCSV(self):
        if self.db.dbFolder:
            try:
                fileHeader = ['Id', 'Fecha', 'Titulo', 'Descripcion', 'Archivo']#'Id, Fecha, Descripcion, Archivo'
                csvFile = f'{self.db.dbFolder}\\registros.csv'
                records = self.selectAll()
                with open(csvFile,'w', newline="") as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(fileHeader)

                    for row in records:
                        writer.writerow(row)
            except PermissionError: print('Cerrar archivo e intentar nuevamente')

    def saveDetails(self):
        if self.db.dbFolder:
            if self.detailsForm.id_.text(): sql = self.detailsForm.updateRecordSql()
            else: sql = self.detailsForm.insertNewSql()
            try:
                self.db.executeQueryCommit(sql)
            except sqlite3.OperationalError:
                self.db.executeQuery(self.detailsForm.createTableSql)
                self.db.executeQueryCommit(sql)
            
        
    
class mainTree(treeviewSearchBox):
    def __init__(self, fontSize=11, sortColumn=1, sortOrder=Qt.SortOrder.AscendingOrder):
        super().__init__(fontSize, sortColumn, sortOrder)
        self.fontSize = fontSize
        self.configureTree()
        self.createFilters()
        self.getFiles(self.rootFolder, self.rootNode)

    def requery(self):
        self.getFiles(self.rootFolder, self.rootNode)
        
    def createFilters(self):
        self.proxyTipo = QSortFilterProxyModel()
        self.filterTipo = cboFilterGroup(self.fontSize,
        refreshable=False)
        self.layoutFilter.insertRow(0, labelWidget('Tipo:', self.fontSize), self.filterTipo)
        self.filterTipo.cbo.currentTextChanged.connect(self.applyFilterTipo)
    
    def configureTree(self):
        self.standardModel.setHorizontalHeaderLabels(['Tipo', 'Servicio'])
        self.setColumnsWith(((0,110),(2,200)))
        self.rootFolder = f'{constants.oneDrive}\Despacho\Enlace_servicios\Servicios'

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
            title TEXT,
            description_ TEXT,
            file_ TEXT
            );
        --endsql '''
        # self.dbFolder = f'{constants.rootAVDT}\Carriers'




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