#!/usr/bin/python3

from globalElements import DB, constants, mainModel
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
        self.tableVar = 'clients_agents'
        self.listTableValuesIndexes = (0,1,2,3,4,5,6)
        # self.formToDBItems = 4
        self.titleText = "CLIENTS CONTACTS"
        self.listExpand = 1
        self.formExpand = 1
        self.listHiddenItems = (0,3,4,5,6)#(4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((1,230),(2,220))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectFile = '''
            SELECT 
                agents.id, 
                clients.name_ AS "Client",
                agents.name_ AS "Agent",
                agents.phone AS "Phone",
                agents.ext AS "Extention",
                agents.email AS "Email",
                agents.notes AS "Notes"
                FROM clients_agents agents
                LEFT JOIN clients ON clients.id = agents.idClient
                ORDER BY agents.name_
                ;
                        '''
        self.newRecordSql = ''' INSERT INTO clients_agents 
            (idClient, name_, phone, ext, email, notes) VALUES '''
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.clientsList:
            constants.queryClients()

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idClient = '{record[1]}',
                name_ = '{record[2]}',
                phone = '{record[3]}',
                ext = '{record[4]}',
                email = '{record[5]}',
                notes = '{record[6]}'
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
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.client = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.clientsDict,
            requeryFunc=constants.queryClients,
            clearFilter=False) 
        self.name = lineEdit(self.fontSize)
        self.phone = lineEditPhone(self.fontSize)
        self.ext = lineEdit(self.fontSize)
        self.email = lineEdit(self.fontSize)
        self.notes = textEdit(self.fontSize)

        self.formItems = [self.id_, self.client, self.name, self.phone, 
            self.ext, self.email, self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Client:', self.fontSize), self.client)
        self.layoutForm.addRow(labelWidget('Name:', self.fontSize),self.name)
        self.layoutForm.addRow(labelWidget('Phone:', self.fontSize), self.phone)
        self.layoutForm.addRow(labelWidget('Extention:', self.fontSize), self.ext)
        self.layoutForm.addRow(labelWidget('Email:', self.fontSize), self.email)
        self.layoutForm.addRow(labelWidget('Notes:', 14,True,align="center"))
        self.layoutForm.addRow(self.notes)
        
    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.client.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.client.getInfo()))
        self.name.textChanged.connect(lambda: self.formDirty(2,self.name.getInfo()))
        self.phone.textChanged.connect(lambda: self.formDirty(3,self.phone.getInfo()))
        self.ext.textChanged.connect(lambda: self.formDirty(4,self.ext.getInfo()))
        self.email.textChanged.connect(lambda: self.formDirty(5,self.email.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(6,self.notes.getInfo()))

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())