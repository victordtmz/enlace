#!/usr/bin/python3
import sys, os, pathlib
from globalElements.widgets import labelWidget, textEdit, lineEdit, cboFilterGroup
from globalElements import constants, mainModel, DB
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import  QCursor


class main(mainModel.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configure_form()
        self.setConnections()
        # self.setTotalsElements()
        self.requery()
        
        # self.getIdLoad()

   

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'trucks'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7)
        # self.formToDBItems = 4
        self.titleText = "TRUCKS"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (0,3,4,5,6,7)#(4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((1,260),(2,120))
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        sqlFiles = 'avdt\\trucks'
        self.selectFile = f'{sqlFiles}\selectAll.sql'
        self.selectSql = '''
        SELECT 
            trucks.id, 
            carriers.name_ AS "Carrier",
            no_ AS "No",
            vin AS "VIN",
            year_ AS "Year",
            make AS "Make",
            model AS "Model",
            trucks.notes AS "Notes"
            FROM trucks
            LEFT JOIN carriers ON carriers.id = trucks.idCarrier
            ORDER BY no_
            ;
        '''
        self.newRecordSql = '''
        INSERT INTO trucks (
            idCarrier,
            no_,
            vin,
            year_,
            make,
            model,
            notes
            )
            VALUES
        '''
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.carriersItems:
            constants.queryCarriers()

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idCarrier = '{record[1]}',
                no_ = '{record[2]}',
                vin = '{record[3]}',
                year_ = '{record[4]}',
                make = '{record[5]}',
                model = '{record[6]}',
                notes = '{record[7]}'
                WHERE id =  {record[0]};'''
        self.db.run_sql_commit(sql)

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
            no = self.no.getInfo()
            

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutSideFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)

        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.carrier = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.carriersDict,
            requeryFunc=constants.queryCarriers) #lineEdit(self.fontSize)
        self.no = lineEdit(self.fontSize)
        self.vin = lineEdit(self.fontSize)
        self.year = lineEdit(self.fontSize)
        self.make = lineEdit(self.fontSize)
        self.model = lineEdit(self.fontSize)
        self.notes = textEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_,self.carrier, self.no, self.vin, self.year, self.make, self.model, self.notes]
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdCarrier:', self.fontSize), self.carrier)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize),self.no)
        self.layoutForm.addRow(labelWidget('VIN:', self.fontSize), self.vin)
        self.layoutForm.addRow(labelWidget('Year:', self.fontSize), self.year)
        self.layoutForm.addRow(labelWidget('Make:', self.fontSize), self.make)
        self.layoutForm.addRow(labelWidget('Model:', self.fontSize), self.model)
        self.layoutForm.addRow(labelWidget('Notes:', 14,True,align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
        self.no.textChanged.connect(lambda: self.formDirty(2,self.no.getInfo()))
        self.vin.textChanged.connect(lambda: self.formDirty(3,self.vin.getInfo()))
        self.year.textChanged.connect(lambda: self.formDirty(4,self.year.getInfo()))
        self.make.textChanged.connect(lambda: self.formDirty(5,self.make.getInfo()))
        self.model.textChanged.connect(lambda: self.formDirty(6,self.model.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(7,self.notes.getInfo()))

    def setFilesFolder(self):
        carrier = self.carrier.getInfo()
        truck = self.no.getInfo()
        if carrier and truck:
            folderPath = f'{self.filesFolder.root}\{carrier}\Trucks\{truck}'
            self.filesFolder.txtFilePath.setText(folderPath)
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
                self.filesFolder.txtFilePath.setText('folderPath')
                self.filesFolder.txtFilePath.setText(folderPath)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())