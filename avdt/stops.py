#!/usr/bin/python3

from globalElements import DB, constants, mainModel
from globalElements.widgets import dateWidget, dateEdit, labelWidget,  webWidget, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone
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
        # self.setTotalsElements()
        self.requery()
        
        # self.getIdLoad()

   

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'stops'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7,8,9,10)
        # self.formToDBItems = 4
        self.titleText = "WAREHOUSES"
        self.listWidth = 1 
        self.formWidth = 1
        self.listHiddenItems = (0,2,3,4,7,8,9,10)
        self.listColumnWidth = ((1,230),(5,120),(6,80))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
            SELECT 
            id,
            name_ AS "Warehouse",
            north AS "North",
            west AS "West",
            address_ AS "Address",
            city as "City",
            state_ AS "State",
            zip AS "Zip",
            phone AS "Phone",
            google AS "Google",
            notes AS "Notes"
            FROM stops
            ;'''
        self.newRecordSql = '''INSERT INTO stops (name_, north,
            west, address_, city, state_, zip, phone, google, notes) VALUES'''
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.carriersItems:
            constants.queryCarriers()

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                name_ = '{record[1]}',
                north = '{record[2]}',
                west = '{record[3]}',
                address_ = '{record[4]}',
                city = '{record[5]}',
                state_ = '{record[6]}',
                zip = '{record[7]}',
                phone = '{record[8]}',
                google = '{record[9]}',
                notes = '{record[10]}'
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
        self.formLayoutStraight()
        self.setFormElements()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.name_ = lineEdit(self.fontSize)
        self.north = lineEdit(self.fontSize)
        self.west = lineEdit(self.fontSize)
        self.address = lineEdit(self.fontSize)
        self.city = lineEdit(self.fontSize)
        self.state = lineEdit(self.fontSize)
        self.zip = lineEdit(self.fontSize)
        self.phone = lineEditPhone(self.fontSize)
        self.google  = webWidget(self.fontSize)
        self.notes = textEdit(self.fontSize)

        self.formItems = [
            self.id_, 
            self.name_,
            self.north, 
            self.west,
            self.address,
            self.city,
            self.state,
            self.zip,
            self.phone,
            self.google,
            self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Name:', self.fontSize), self.name_)
        self.layoutForm.addRow(labelWidget('North:', self.fontSize), self.north)
        self.layoutForm.addRow(labelWidget('West:', self.fontSize), self.west)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address)
        self.layoutForm.addRow(labelWidget('City:', self.fontSize), self.city)
        self.layoutForm.addRow(labelWidget('State:', self.fontSize), self.state)
        self.layoutForm.addRow(labelWidget('Zip:', self.fontSize), self.zip)
        self.layoutForm.addRow(labelWidget('Phone:', self.fontSize), self.phone)
        self.layoutForm.addRow(labelWidget('Google Maps:', self.fontSize), self.google)
        self.layoutForm.addRow(labelWidget("Notes", 16, fontColor="Blue", align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.name_.textChanged.connect(lambda: self.formDirty(1,self.name_.getInfo()))
        self.north.textChanged.connect(lambda: self.formDirty(2, self.north.getInfo))
        self.west.textChanged.connect(lambda: self.formDirty(3, self.west.getInfo))
        self.address.textChanged.connect(lambda: self.formDirty(4, self.address.getInfo))
        self.city.textChanged.connect(lambda: self.formDirty(5, self.city.getInfo))
        self.state.textChanged.connect(lambda: self.formDirty(6, self.state.getInfo))
        self.zip.textChanged.connect(lambda: self.formDirty(7, self.zip.getInfo))
        self.phone.textChanged.connect(lambda: self.formDirty(8, self.phone.getInfo))
        self.google.lineEdit.textChanged.connect(lambda: self.formDirty(9, self.google.getInfo))
        self.notes.textChanged.connect(lambda: self.formDirty(10, self.notes.getInfo))

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())