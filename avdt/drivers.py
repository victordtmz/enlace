#!/usr/bin/python3

from globalElements import DB, constants, modelMain
from globalElements.widgets import dateWidget, dateEdit, labelWidget,  lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone
from globalElements.zipsWidget import mainUs as UsZipsWidget
import sys
import os
import pathlib
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 

locale.setlocale(locale.LC_ALL,"")
from decimal import *


class main(modelMain.main):
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
        self.tableVar = 'drivers'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
        # self.formToDBItems = 4
        self.titleText = "DRIVERS"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (0,3,4,5,6,7,8,9,10,11,12,13,14)#(4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((1,230),(2,220))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.newRecordSql = '''
            INSERT INTO drivers (idCarrier, name_, dob, phone, address, address1, city,
            state, zip, licNo, licIss, licExp, licState, notes)
            VALUES 
            '''
        self.selectSql = '''
        SELECT 
            drivers.id, 
            carriers.name_ AS "Carrier",
            drivers.name_ AS "Name",
            dob AS "Date of Birth",
            drivers.phone AS "Phone",
            drivers.address AS "Address",
            drivers.address1 AS "Address",
            drivers.city as "City",
            drivers.state AS "State",
            drivers.zip AS "Zip",
            licNo AS "No. Licencia", 
            licIss AS "Expedicion",
            licExp AS "Vencimiento",
            licState AS "Estado",
            drivers.notes AS "Notes"
            FROM drivers
            LEFT JOIN carriers ON carriers.id = drivers.idCarrier
            ORDER BY drivers.name_; 
        '''
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.carriersItems:
            constants.queryCarriers()

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idCarrier = '{record[1]}',
                name_ = '{record[2]}',
                dob = '{record[3]}',
                phone = '{record[4]}',
                address = '{record[5]}',
                address1 = '{record[6]}',
                city = '{record[7]}',
                state = '{record[8]}',
                zip = '{record[9]}',
                licNo = '{record[10]}',
                licIss = '{record[11]}',
                licExp = '{record[12]}',
                licState = '{record[13]}',
                notes = '{record[14]}'
                WHERE id =  {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()
        if records:
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
        else:
            self.list.removeAllRows()
        
        self.configureColumns()
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        
        

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            no = self.name.getInfo()
            

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
        self.name = lineEdit(self.fontSize)
        self.dob = dateEdit(self.fontSize)
        self.phone = lineEditPhone(self.fontSize)
        self.address = lineEdit(self.fontSize)
        self.address1 = lineEdit(self.fontSize)
        self.location = UsZipsWidget(self.fontSize)
        self.city = self.location.city
        self.state = self.location.state
        self.zip = self.location.zip
        self.licNo = lineEdit(self.fontSize)
        self.licIss = dateWidget(self.fontSize)
        self.licExp = dateWidget(self.fontSize)
        self.licState = cboFilterGroup(self.fontSize,
            items=self.location.states)
        self.notes = textEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.carrier, self.name, self.dob, self.phone, 
            self.address, self.address1, self.city, self.state , self.zip, self.licNo, 
            self.licIss, self.licExp, self.licState, self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Carrier:', self.fontSize), self.carrier)
        self.layoutForm.addRow(labelWidget('Name:', self.fontSize),self.name)
        self.layoutForm.addRow(labelWidget('DOB:', self.fontSize), self.dob)
        self.layoutForm.addRow(labelWidget('Phone:', self.fontSize), self.phone)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address1)
        self.layoutForm.addRow(labelWidget('Zip:', self.fontSize), self.zip)
        self.layoutForm.addRow(labelWidget('State:', self.fontSize), self.state)
        self.layoutForm.addRow(labelWidget('City:', self.fontSize), self.city)
        self.layoutForm.addRow(labelWidget('Licencia:', 14,True,align="center"))
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.licNo)
        self.layoutForm.addRow(labelWidget('Issued:', self.fontSize), self.licIss)
        self.layoutForm.addRow(labelWidget('Expires:', self.fontSize), self.licExp)
        self.layoutForm.addRow(labelWidget('State:', self.fontSize), self.licState)
        self.layoutForm.addRow(labelWidget('Notes:', 14,True,align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
        self.name.textChanged.connect(lambda: self.formDirty(2,self.name.getInfo()))
        self.dob.dateChanged.connect(lambda: self.formDirty(3,self.dob.getInfo()))
        self.phone.textChanged.connect(lambda: self.formDirty(4,self.phone.getInfo()))
        self.address.textChanged.connect(lambda: self.formDirty(5,self.address.getInfo()))
        self.address1.textChanged.connect(lambda: self.formDirty(6,self.address1.getInfo()))
        self.city.currentTextChanged.connect(lambda: self.formDirty(7,self.city.getInfo()))
        self.state.currentTextChanged.connect(lambda: self.formDirty(8,self.state.getInfo()))
        self.zip.textChanged.connect(lambda: self.formDirty(9,self.zip.getInfo()))
        self.licNo.textChanged.connect(lambda: self.formDirty(10,self.licNo.getInfo()))
        self.licIss.dateEdit.dateChanged.connect(lambda: self.formDirty(11,self.licIss.getInfo()))
        self.licExp.dateEdit.dateChanged.connect(lambda: self.formDirty(12,self.licExp.getInfo()))
        self.licState.cbo.currentTextChanged.connect(lambda: self.formDirty(13,self.licState.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(14,self.notes.getInfo()))

    def setFilesFolder(self):
        carrier = self.carrier.getInfo()
        driver = self.name.getInfo()
        if carrier and driver:
            folderPath = f'{self.filesFolder.root}\{carrier}\drivers\{driver}'
            self.filesFolder.txtFilePath.setText(folderPath)
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
                self.filesFolder.txtFilePath.setText('folderPath')
                self.filesFolder.txtFilePath.setText(folderPath)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())