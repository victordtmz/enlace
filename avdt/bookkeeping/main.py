#!/usr/bin/python3

from globalElements import DB, constants, mainModel
from globalElements.widgets import labelWidget,  lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone
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


class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.configure_form()
        self.setConnections()
        self.requery()
        
    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'clients'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7,8,9,10,11,12)
        # self.formToDBItems = 4
        self.titleText = "CLIENTS"
        self.listWidth = 1
        self.formWidth = 1
        self.listHiddenItems = ()#(4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((0,60),(1,280),(2,130),(3,130))
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        sqlFiles = 'avdt\clients'
        self.selectFile = f'{sqlFiles}\selectAll.sql'
        self.newRecordSql = f'{sqlFiles}\insertNewRecord.sql'
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                name_ = '{record[1]}',
                mc = '{record[2]}',
                usdot = '{record[3]}',
                phone = '{record[4]}',
                address = '{record[5]}',
                address1 = '{record[6]}',
                city = '{record[7]}',
                state = '{record[8]}',
                zip = '{record[9]}',
                notes = '{record[10]}',
                invoiceEmail = '{record[11]}',
                invoiceNotes = '{record[12]}'
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
            name = self.name.getInfo()
            

            text = f'''Eliminar el registro:
            id: {idVar} 
            Cliente: {name}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutSideFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.root = f'{constants.rootAVDT}\Clients'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)

        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.name = lineEdit(self.fontSize)
        self.mc = lineEdit(self.fontSize)
        self.usdot = lineEdit(self.fontSize)
        self.phone = lineEditPhone(self.fontSize)
        self.address = lineEdit(self.fontSize)
        self.address1 = lineEdit(self.fontSize)
        self.location = UsZipsWidget(self.fontSize)
        self.city = self.location.city
        self.state = self.location.state
        self.zip = self.location.zip
        self.notes = textEdit(self.fontSize)
        self.invoiceEmail = lineEdit(self.fontSize)
        self.invoiceNotes = textEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_,self.name, self.mc, self.usdot, self.phone, 
            self.address, self.address1, self.city, self.state , self.zip,  
            self.notes, self.invoiceEmail, self.invoiceNotes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Name:', self.fontSize), self.name)
        self.layoutForm.addRow(labelWidget('MC:', self.fontSize),self.mc)
        self.layoutForm.addRow(labelWidget('USDOT:', self.fontSize), self.usdot)
        self.layoutForm.addRow(labelWidget('Phone:', self.fontSize), self.phone)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address1)
        self.layoutForm.addRow(labelWidget('Zip:', self.fontSize), self.zip)
        self.layoutForm.addRow(labelWidget('State:', self.fontSize), self.state)
        self.layoutForm.addRow(labelWidget('City:', self.fontSize), self.city)
        self.layoutForm.addRow(labelWidget('Notes', 14,True, align="center"))
        self.layoutForm.addRow(self.notes)
        self.layoutForm.addRow(labelWidget('INVOICE  DETAILS', 20,False, "white", "center", '#0053a7'))
        self.layoutForm.addRow(labelWidget('Email:', self.fontSize), self.invoiceEmail)
        self.layoutForm.addRow(labelWidget('Notes', 14,True, "Black", "center"))
        self.layoutForm.addRow(self.invoiceNotes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.name.textChanged.connect(lambda: self.formDirty(1,self.name.getInfo()))
        self.mc.textChanged.connect(lambda: self.formDirty(2,self.mc.getInfo()))
        self.usdot.textChanged.connect(lambda: self.formDirty(3,self.usdot.getInfo()))
        self.phone.textChanged.connect(lambda: self.formDirty(4,self.phone.getInfo()))
        self.address.textChanged.connect(lambda: self.formDirty(5,self.address.getInfo()))
        self.address1.textChanged.connect(lambda: self.formDirty(6,self.address1.getInfo()))
        self.city.currentTextChanged.connect(lambda: self.formDirty(7,self.city.getInfo()))
        self.state.currentTextChanged.connect(lambda: self.formDirty(8,self.state.getInfo()))
        self.zip.textChanged.connect(lambda: self.formDirty(9,self.zip.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(10,self.notes.getInfo()))
        self.invoiceEmail.textChanged.connect(lambda: self.formDirty(11,self.notes.getInfo()))
        self.invoiceEmail.textChanged.connect(lambda: self.formDirty(12,self.notes.getInfo()))

    def setFilesFolder(self):
        if self.name.text():
            folderPath = f'{self.filesFolder.root}\{self.name.text()}'
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