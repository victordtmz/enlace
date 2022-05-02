#!/usr/bin/python3

from globalElements import DB, constants, mainModel
from globalElements.widgets import (dateWidget, dateEdit, labelWidget,  lineEditCurrency, 
    textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone, truFalseRadioButtons, checkBox)
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
        self.listFontSize = 10
        # self.setTotalsElements()
        self.requery()
        self.showMaximized()
        self.splitter.setSizes([360,1000])
        
        # self.getIdLoad()

   

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'loads'
        self.listTableValuesIndexes = (0,1,2,3,4,5,7,8,6,9,10,11,12,13,14,15,16,17,18,19)
        # self.formToDBItems = 4
        self.titleText = "LOADS"
        self.listWidth = 0
        self.formWidth = 3
        self.listHiddenItems = (1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19)
        self.listColumnWidth = ((0,50),(6,80),(7,220))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        sqlFiles = 'avdt\\loads'
        self.selectFile = f'{sqlFiles}\selectAll.sql'
        self.newRecordSql = f'{sqlFiles}\insertNewRecord.sql'
        
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.carriersList: 
            constants.queryCarriers()
        if not constants.trucksList: 
            constants.queryTrucks()
        if not constants.trailersList: 
            constants.queryTrailers()
        if not constants.driversList: 
            constants.queryDrivers()
        if not constants.clientsList: 
            constants.queryClients()
        if not constants.agentsList: 
            constants.queryAgents()

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idContracting = '{record[1]}',
                idHauling = '{record[2]}',
                idTruck = '{record[3]}',
                idTrailer = '{record[4]}',
                idDriver = '{record[5]}',
                idClient = '{record[6]}',
                idClientAgent = '{record[7]}',
                contractDate = '{record[8]}',
                referenceNo = '{record[9]}',
                rate = '{record[10]}',
                dateInvoice = '{record[11]}',
                amountPaid = '{record[12]}',
                datePaid = '{record[13]}',
                notes = '{record[14]}',
                delivered = '{record[15]}',
                invoiced = '{record[16]}',
                paid = '{record[17]}',
                paidHCarrier = '{record[18]}',
                completed = '{record[19]}'
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
            no = self.reference.getInfo()
            

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutTabsFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)

        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        
        self.contracting = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.carriersDict,
            requeryFunc=constants.queryCarriers,
            clearFilter=False) 
        
        self.hauling = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.carriersDict,
            requeryFunc=constants.queryCarriers,
            clearFilter=False) 

        self.truck = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.trucksDict,
            requeryFunc=constants.queryTrucks,
            clearFilter=False) 
        
        self.trailer = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.trailersDict,
            requeryFunc=constants.queryTrailers,
            clearFilter=False) 
        
        self.driver = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.driversDict,
            requeryFunc=constants.queryDrivers,
            clearFilter=False) 
        
        self.client = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.clientsDict,
            requeryFunc=constants.queryClients,
            clearFilter=False) 
        
        self.agent = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.agentsDict,
            requeryFunc=constants.queryAgents,
            clearFilter=False) 
        
        self.contractDate = dateWidget(self.fontSize)

        self.reference = lineEdit(self.fontSize)
        self.rate = lineEditCurrency(self.fontSize)
        
        self.invoiceDate = dateWidget(self.fontSize)
        self.amountPaid = lineEditCurrency(self.fontSize)
        self.datePaid = dateWidget(self.fontSize)
        self.notes = textEdit(self.fontSize)

        self.delivered = checkBox()
        self.invoiced = checkBox()
        self.paid = checkBox()
        self.paidHCarrier = checkBox()
        self.completed = checkBox()

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.contracting, self.hauling, self.truck,
            self.trailer, self.driver, self.client, self.agent, self.contractDate,
            self.reference, self.rate, self.invoiceDate, self.amountPaid, 
            self.datePaid,self.notes, self.delivered, self.invoiced, self.paid, 
            self.paidHCarrier, self.completed]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Contracting:', self.fontSize), self.contracting)
        self.layoutForm.addRow(labelWidget('Hauling:', self.fontSize), self.hauling)
        self.layoutForm.addRow(labelWidget('Truck:', self.fontSize), self.truck)
        self.layoutForm.addRow(labelWidget('Trailer:', self.fontSize), self.trailer)
        self.layoutForm.addRow(labelWidget('Driver:', self.fontSize), self.driver)
        self.layoutForm.addRow(labelWidget('Client:', self.fontSize), self.client)
        self.layoutForm.addRow(labelWidget('Agent:', self.fontSize), self.agent)
        self.layoutForm.addRow(labelWidget('Contracted:', self.fontSize), self.contractDate)
        self.layoutForm.addRow(labelWidget('Reference:', self.fontSize),self.reference)
        self.layoutForm.addRow(labelWidget('Rate:', self.fontSize),self.rate)
        self.layoutForm.addRow(labelWidget('Invoiced:', self.fontSize), self.invoiceDate)
        self.layoutForm.addRow(labelWidget('$ Paid:', self.fontSize), self.amountPaid)
        self.layoutForm.addRow(labelWidget('Paid:', self.fontSize), self.datePaid)
        self.layoutForm.addRow(labelWidget('Delivered:', self.fontSize), self.delivered)
        self.layoutForm.addRow(labelWidget('Invoiced:', self.fontSize), self.invoiced)
        self.layoutForm.addRow(labelWidget('Paid:', self.fontSize), self.paid)
        self.layoutForm.addRow(labelWidget('Paid Hauler:', self.fontSize), self.paidHCarrier)
        self.layoutForm.addRow(labelWidget('Completed:', self.fontSize), self.completed)
        self.layoutForm.addRow(labelWidget('Notes:', 14,True,align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.contracting.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.contracting.getInfo()))
        self.hauling.cbo.currentTextChanged.connect(lambda: self.formDirty(2,self.hauling.getInfo()))
        self.truck.cbo.currentTextChanged.connect(lambda: self.formDirty(3,self.truck.getInfo()))
        self.trailer.cbo.currentTextChanged.connect(lambda: self.formDirty(4,self.trailer.getInfo()))
        self.driver.cbo.currentTextChanged.connect(lambda: self.formDirty(5,self.driver.getInfo()))
        self.client.cbo.currentTextChanged.connect(lambda: self.formDirty(6,self.client.getInfo()))
        self.agent.cbo.currentTextChanged.connect(lambda: self.formDirty(7,self.agent.getInfo()))
        self.contractDate.dateEdit.dateChanged.connect(lambda: self.formDirty(8,self.contractDate.getInfo()))
        self.reference.textChanged.connect(lambda: self.formDirty(9,self.reference.getInfo()))
        self.rate.textChanged.connect(lambda: self.formDirty(10,self.rate.getInfo()))
        self.invoiceDate.dateEdit.dateChanged.connect(lambda: self.formDirty(11,self.contracting.getInfo()))
        self.amountPaid.textChanged.connect(lambda: self.formDirty(12,self.amountPaid.getInfo()))
        self.datePaid.dateEdit.dateChanged.connect(lambda: self.formDirty(13,self.datePaid.getInfo()))
        self.notes.textChanged.connect(lambda: self.formDirty(14,self.notes.getInfo()))
        self.delivered.toggled.connect(lambda: self.formDirty(15, self.delivered.getInfo()))
        self.invoiced.toggled.connect(lambda: self.formDirty(16, self.invoiced.getInfo()))
        self.paid.toggled.connect(lambda: self.formDirty(17, self.paid.getInfo()))
        self.paidHCarrier.toggled.connect(lambda: self.formDirty(18, self.paidHCarrier.getInfo()))
        self.completed.toggled.connect(lambda: self.formDirty(19, self.completed.getInfo()))

    def setFilesFolder(self):
        carrier = self.contracting.getInfo()
        date_ = self.contractDate.getInfo()
        client = self.client.getInfo()
        if carrier and client and date_:
            folderPath = f'{self.filesFolder.root}\{carrier}\Loads\{date_}_{client}'
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