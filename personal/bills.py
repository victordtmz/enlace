from localDB import mainModel
import sqlite3

from globalElements import constants, modelEmpty

from globalElements.treeview import treeviewSearchBox

from globalElements.widgets import (buttonWidget, dateEdit, dateWidget, lineEditCurrency, lineEditPhone, standardItem, 
    labelWidget,  textEdit, lineEdit, spinbox, cboFilterGroup, checkBox, webWidget)
from localDB import sqliteDB
from PyQt6.QtWidgets import (QApplication, QCompleter, QWidget, QFormLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QCursor, QCloseEvent
import pathlib
import os 
import csv
  
# class DB(sqliteDB.avdtLocalDB): 
#     def __init__(self): 
#         self.database = 'registros.avd'
#         self.tableVar = 'registros'
        
#         self.createTableSql = f'''
#         --sql
#         CREATE TABLE IF NOT EXISTS {self.tableVar} (
#             id INTEGER PRIMARY KEY,
#             date_ TEXT,
#             description_ TEXT,
#             file_ TEXT
#             );
#         --endsql '''

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
            cliente TEXT,
            expediente TEXT,
            fecha_ TEXT,
            honorarios_ REAL,
            telefono TEXT,
            domicilio TEXT,
            domicilio1 TEXT,
            ciudad TEXT,
            estado TEXT,
            cp TEXT,
            descripcion TEXT
            );
        '''
        
        
        self.selectSql = f'''
        --sql
        SELECT id, cliente, expediente, fecha_, honorarios_, telefono, domicilio, domicilio1,
            ciudad, estado, cp, descripcion
        FROM {self.tableVar};
        '''

        
    def insertNewSql(self):
        record = self.getInfo()
        record.pop(0)
        record = str(record)
        record = record[1:-1]
        sql = f'''
        --sql
        INSERT INTO {self.tableVar} (cliente, expediente, fecha_, honorarios_, telefono, domicilio, domicilio1,
            ciudad, estado, cp, descripcion) VALUES ({record});'''
            
            
        return sql

    def updateRecordSql(self): 
        record = self.getInfo()
        sql =f'''
        --sql
        UPDATE {self.tableVar} SET 
            cliente = '{record[1]}',
            expediente = '{record[2]}',
            fecha_ = '{record[3]}',
            honorarios_ = '{record[4]}',
            telefono = '{record[5]}',
            domicilio = '{record[6]}',
            domicilio1 = '{record[7]}',
            ciudad = '{record[8]}',
            estado = '{record[9]}',
            cp = '{record[10]}',
            descripcion = '{record[11]}'
            WHERE id = 1;'''
        return sql

    def configureForm(self):
        self.id_ = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        self.cliente = lineEdit(self.fontSize)
        self.expediente = lineEdit(self.fontSize)
        self.fecha = dateWidget(self.fontSize)
        self.honorarios = lineEditCurrency(self.fontSize)
        self.telefono = lineEditPhone(self.fontSize)
        self.domicilio = lineEdit(self.fontSize)
        self.domicilio1 = lineEdit(self.fontSize)
        self.ciudad = lineEdit(self.fontSize)
        self.estado = lineEdit(self.fontSize)
        self.cp = lineEdit(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.formItems = [self.id_, self.cliente, self.expediente, self.fecha, self.honorarios, 
            self.telefono, self.domicilio, self.domicilio1, self.ciudad, self.estado,
            self.cp, self.description]

        self.btnSave = buttonWidget('Guardar', 'h2_', constants.iconSave)

        self.layout_ = QFormLayout()
        self.layout_.addRow(labelWidget('Id:', self.fontSize) ,self.id_)
        self.layout_.addRow(labelWidget('Cliente:', self.fontSize) ,self.cliente)
        self.layout_.addRow(labelWidget('Expediente:', self.fontSize) ,self.expediente)
        self.layout_.addRow(labelWidget('Fecha de inicio:', self.fontSize) ,self.fecha)
        self.layout_.addRow(labelWidget('Honorarios:', self.fontSize) ,self.honorarios)
        self.layout_.addRow(labelWidget('Telefono:', self.fontSize) ,self.telefono)
        self.layout_.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio)
        self.layout_.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio1)
        self.layout_.addRow(labelWidget('Ciudad:', self.fontSize) ,self.ciudad)
        self.layout_.addRow(labelWidget('Estado:', self.fontSize) ,self.estado)
        self.layout_.addRow(labelWidget('Codigo postal:', self.fontSize) ,self.cp)
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
        self.configureWidth()
        
    def configureDetailsForm(self):
        self.detailsFormOpt = checkBox('Detalles del Tramite',fontSize=self.fontSize, size=self.mainSize)
        self.detailsFormOpt.setChecked(False)
        # = [self.mainFormOpt,self.listOpt, self.formOpt]
        self.titleLayout.insertWidget(4, self.detailsFormOpt)
        self.detailsFormOpt.toggled.connect(self.configureWidth)
        self.detailsForm = detailsForm()
        self.widgetsOptSizes.append(1)
        self.widgetsOpt.insert(3,self.detailsFormOpt)
        self.splitter.insertWidget(3,self.detailsForm)
        self.detailsForm.btnSave.pressed.connect(self.saveDetails)

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
        self.btnActivos = buttonWidget('Activos', 'h1', constants.iconFolderOpen)
        self.btnInactivos = buttonWidget('Inactivos', 'h1', constants.iconFolderOpen)
        self.titleLayout.insertWidget(5, self.btnCSV)
        self.titleLayout.insertWidget(5, self.btnInactivos)
        self.titleLayout.insertWidget(5, self.btnActivos)
        self.btnCSV.pressed.connect(self.recordsToCSV)
        self.btnActivos.pressed.connect(self.activosFolderOpen)
        self.btnInactivos.pressed.connect(self.inactivosFolderOpen)
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
        self.listTableValuesIndexes = (0,1,2,3,4)
        # self.formToDBItems = 4
        self.titleText = "JUICIOS Y TRAMITES"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1,1]
        self.listHiddenItems = (0,3,4)
        self.listColumnWidth = ((1,100),(2,120))
        self.sortColumn = 1
        self.sortOrder = Qt.SortOrder.DescendingOrder
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
        
        
            
    
    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        if self.mainList.treeview.selectionModel().hasSelection():
            expediente = self.mainList.treeview.selectedIndexes()
            tipo = expediente[0].data()
            # website = ''
            match tipo.lower():
                case "administrativo":
                    website = 'https://serviciosdigitales.tjagto.gob.mx/tribunalelectronicoweb/Secciones/Servicios/SeguridadServicios.aspx'
                case "civil":
                    website = 'https://poderjudicial-gto.gob.mx/modules.php?name=Servicios_virtuales&file=registro&func=login_suscriptor'
                case _:
                    website = 'enlacellc.com'
            self.webWidget.populate(website)

            
            # self.title.setText(expediente[1].data())
            fileFolder = f'{tipo}\{expediente[1].data()}'
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

    def insertNewRecord(self, record):
        sql = f'''INSERT INTO {self.tableVar} 
            (date_, title, description_, file_) VALUES 
            ('{record[1]}','{record[2]}','{record[3]}','{record[4]}')'''
        idVar = self.db.insertNewRecord(sql)
        return idVar
    
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

        #Web widget para informacion de la pagina del juzgado o donde se lleva el tramite
        self.webWidget = webWidget(self.fontSize)
        
        self.layoutForm.addRow(self.webWidget)
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
    
    # def closeEvent(self, a0: QCloseEvent):
    #     # self.save_record_main(False, False)#updateList, changedSelection
    #     return super().closeEvent(a0)

    # def listadoSelectionChanged(self):
    #     return super().listadoSelectionChanged()

    def activosFolderOpen(self):
        os.startfile(f'{constants.oneDrive}\enlace\Juicios')

    def inactivosFolderOpen(self):
        os.startfile(f'{constants.oneDrive}\enlace\Juicios_archivados')


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
        self.requery()
        # self.getFiles(self.rootFolder, self.rootNode)

    def createFilters(self):
        self.proxyTipo = QSortFilterProxyModel()
        self.filterTipo = cboFilterGroup(self.fontSize,refreshable=False)
        self.filterActivo = checkBox()
        self.filterActivo.toggled.connect(self.requery)
        self.layoutFilter.insertRow(0, labelWidget('Tipo:', self.fontSize), self.filterTipo)
        self.layoutFilter.insertRow(0, labelWidget('Inactivos:', self.fontSize), self.filterActivo)
        self.filterTipo.cbo.currentTextChanged.connect(self.applyFilterTipo)
    
    def configureTree(self):
        self.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        self.setColumnsWith(((0,110),(2,200)))
        self.rootFolder = f'{constants.oneDrive}\enlace'
        self.actRefresh.triggered.connect(self.requery)
        

    def requery(self):
        self.removeAllRows()
        tipoFolders = ['']
        if self.filterActivo.isChecked():
            self.rootFolder = f'{constants.oneDrive}\enlace\Juicios_archivados'
        else:
            self.rootFolder = f'{constants.oneDrive}\enlace\Juicios'

        for folder in os.scandir(self.rootFolder):
            if folder.is_dir():
                #add items for filter 
                tipoFolders.append(folder.name)
                for subFolder in os.scandir(folder):
                    record = (folder.name, subFolder.name)
                    record = list(map(self.createRecord, record))
                    self.rootNode.appendRow(record)
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