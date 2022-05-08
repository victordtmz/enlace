#!/usr/bin/python3

from globalElements import DB, constants, modelMain
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
        self.tableVar = 'carriers'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7,8,10,11,9,12)
        # self.formToDBItems = 4
        self.titleText = "CARRIERS"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((0,60),(1,280),(2,130),(3,130))
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
            SELECT 
                id, 
                name_ AS "Name",
                mc AS "MC",
                usdot AS "USDOT",
                ein AS "EIN",
                agent AS "Agent",
                phone AS "Phone",
                address AS "Address",
                address1 AS "Address",
                zip AS "Zip",
                city as "City",
                state AS "State",
                notes AS "Notes"
                FROM carriers
                ORDER BY 
                name_
                ;
                        '''
        self.newRecordSql = '''
            INSERT INTO carriers (
                name_,
                mc,
                usdot,
                ein,
                agent,
                phone,
                address,
                address1,
                city,
                state,
                zip,
                notes
            )
            VALUES 
                    '''
        
    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                name_ = '{record[1]}',
                mc = '{record[2]}',
                usdot = '{record[3]}',
                ein = '{record[4]}',
                agent = '{record[5]}',
                phone = '{record[6]}',
                address = '{record[7]}',
                address1 = '{record[8]}',
                city = '{record[9]}',
                state = '{record[10]}',
                zip = '{record[11]}',
                notes = '{record[12]}'
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
            Carrier: {name}
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
        self.name = lineEdit(self.fontSize)
        self.mc = lineEdit(self.fontSize, True)
        self.usdot = lineEdit(self.fontSize)
        self.ein = lineEdit(self.fontSize)
        self.agent = lineEdit(self.fontSize)
        self.phone = lineEditPhone(self.fontSize)
        self.address = lineEdit(self.fontSize)
        self.address1 = lineEdit(self.fontSize)
        self.location = UsZipsWidget(self.fontSize)
        self.city = self.location.city
        self.state = self.location.state
        self.zip = self.location.zip
        self.notes = textEdit(self.fontSize)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_,self.name, self.mc, self.usdot, self.ein, self.agent, self.phone, 
            self.address, self.address1, self.city, self.state , self.zip,  self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Name:', self.fontSize), self.name)
        self.layoutForm.addRow(labelWidget('MC:', self.fontSize),self.mc)
        self.layoutForm.addRow(labelWidget('USDOT:', self.fontSize), self.usdot)
        self.layoutForm.addRow(labelWidget('EIN:', self.fontSize), self.ein)
        self.layoutForm.addRow(labelWidget('Agent:', self.fontSize), self.agent)
        self.layoutForm.addRow(labelWidget('Phone:', self.fontSize), self.phone)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address)
        self.layoutForm.addRow(labelWidget('Address:', self.fontSize), self.address1)
        self.layoutForm.addRow(labelWidget('Zip:', self.fontSize), self.zip)
        self.layoutForm.addRow(labelWidget('State:', self.fontSize), self.state)
        self.layoutForm.addRow(labelWidget('City:', self.fontSize), self.city)
        self.layoutForm.addRow(labelWidget('Notes:', 14,True,align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.name.textChanged.connect(lambda: self.formDirty(1,self.name.getInfo()))
        self.mc.textChanged.connect(lambda: self.formDirty(2,self.mc.getInfo()))
        self.usdot.textChanged.connect(lambda: self.formDirty(3,self.usdot.getInfo()))
        self.ein.textChanged.connect(lambda: self.formDirty(4,self.ein.getInfo()))
        self.agent.textChanged.connect(lambda: self.formDirty(5,self.agent.getInfo()))
        self.phone.textChanged.connect(lambda: self.formDirty(6,self.phone.getInfo()))
        self.address.textChanged.connect(lambda: self.formDirty(7,self.address.getInfo()))
        self.address1.textChanged.connect(lambda: self.formDirty(8,self.address1.getInfo()))
        self.city.currentTextChanged.connect(lambda: self.formDirty(9,self.city.getInfo()))
        self.state.currentTextChanged.connect(lambda: self.formDirty(10,self.state.getInfo()))
        self.zip.textChanged.connect(lambda: self.formDirty(11,self.zip.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(12,self.notes.getInfo()))

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