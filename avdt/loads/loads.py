#!/usr/bin/python3

from globalElements import DB, constants, modelMain
from globalElements.widgets import (buttonWidget, dateWidget, labelWidget,  lineEditCurrency, 
    textEdit, lineEdit, cboFilterGroup, checkBox)
import sys
import os
import pathlib
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 

locale.setlocale(locale.LC_ALL,"")
from decimal import *
from avdt.loads import miles, stops, bookkeeping, diesel, pay, invoice


class main(modelMain.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configToolbar()
        self.configure_form()
        self.setConnections()
        self.listFontSize = 10
        self.configAdditionalTabs()
        # self.setTotalsElements()
        self.requery()
        self.showMaximized()
        self.splitter.setSizes([400,1000])
        
        # self.getIdLoad()

    def configAdditionalTabs(self):
        self.stops = ''
        self.miles = ''
        self.contractingBook = ''
        self.haulingBook = ''
        self.diesel = ''
        self.invoice = ''
        #o! CONFIGURE DIESEL 

    def configToolbar(self):
        iconRoot = f'{constants.rootDb}\oth\icons'
        self.iconAccounting = qtg.QIcon(f'{iconRoot}\\bank-account.png')
        self.iconDiesel = qtg.QIcon(f'{iconRoot}\\fuel.png')
        self.iconMoney = qtg.QIcon(f'{iconRoot}\moneyBag.png')
        self.iconRoad = qtg.QIcon(f'{iconRoot}\\road.png')
        self.iconStops = qtg.QIcon(f'{iconRoot}\placeholder.png')
        self.iconInvoice = qtg.QIcon(f'{iconRoot}\\accounting.png')

        #Stops toolbar button
        self.btnStops = buttonWidget('Stops', self.mainSize, self.iconStops)
        self.btnStops.pressed.connect(self.stopsOpen)
        self.titleLayout.insertWidget(3, self.btnStops)
        
        #diesel toolbar button
        self.btnDiesel = buttonWidget('Diesel', self.mainSize, self.iconDiesel)
        self.btnDiesel.pressed.connect(self.dieselOpen)
        self.titleLayout.insertWidget(4, self.btnDiesel)

        #Miles toolbar button
        self.btnMiles = buttonWidget('Miles', self.mainSize, self.iconRoad)
        self.btnMiles.pressed.connect(self.milesOpen)
        self.titleLayout.insertWidget(5, self.btnMiles)

        #contracting $$ toolbar button
        self.btnContractingBookkeeping = buttonWidget('Contracting', self.mainSize, self.iconMoney)
        self.btnContractingBookkeeping.pressed.connect(self.contractingBookOpen)
        self.titleLayout.insertWidget(6, self.btnContractingBookkeeping)

        #hauling $$ toolbar button
        self.btnHaulingBookkeeping = buttonWidget('Hauling', self.mainSize, self.iconMoney)
        self.btnHaulingBookkeeping.pressed.connect(self.haulingBookOpen)
        self.titleLayout.insertWidget(7, self.btnHaulingBookkeeping)

        #PAY $$ toolbar button
        self.btnPay = buttonWidget('Pay', self.mainSize, self.iconMoney)
        self.btnPay.pressed.connect(self.payOpen)
        self.titleLayout.insertWidget(8, self.btnPay)

        #invoice  button
        self.btnInvoice = buttonWidget('Invoice', self.mainSize, self.iconInvoice)
        self.btnInvoice.pressed.connect(self.invoiceOpen)
        self.titleLayout.insertWidget(8, self.btnInvoice)

        # #Toolbar button Contracting carrier accounting
        # self.actCCarrierAccounting = qtg.QAction('C ACCOUNTING')
        # self.actCCarrierAccounting.setIcon(self.iconAccounting)
        # # self.actCCarrierAccounting.triggered.connect(self.cCarrierAccountingOpen)
        # #toolbar button hauling carrier accounting
        # self.actHCarrierAccounting = qtg.QAction('H ACCOUNTING')
        # self.actHCarrierAccounting.setIcon(self.iconAccounting)
        # # self.actHCarrierAccounting.triggered.connect(self.hCarrierAccountingOpen)
        

        

        # #Invoice toolbar button
        # self.actInvoice = qtg.QAction('INVOICE ITEMS')
        # self.actInvoice.setIcon(self.iconInvoice)
        # # self.actInvoice.triggered.connect(self.invoiceOpen)

        # #toolbar button hauling carrier accounting
        # self.actLoadsPay = qtg.QAction('PAY INFO')
        # self.actLoadsPay.setIcon(self.iconMoney)
        # # self.actLoadsPay.triggered.connect(self.loadsPayOpen)

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'loads'
        self.listTableValuesIndexes = (0,1,2,3,4,5,7,8,6,9,10,11,12,13,14,15,16,17,18,19)
        # self.formToDBItems = 4
        self.titleText = "LOADS"
        # self.listExpand = 1
        # self.listExpand = 500
        # self.formExpand = 4
        self.widgetsOptSizes = [2,7]#list, form => relative size 
        # self.formExpand = 500
        self.listHiddenItems = (1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19)
        self.listColumnWidth = ((0,50),(6,80),(7,220))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
            SELECT 
                loads.id, 
                contracting.name_ AS "Contractin",
                hauling.name_ AS "Hauling",
                trucks.no_ AS "Truck",
                trailers.no_ AS "Trailer",
                drivers.name_ AS "Driver",
                loads.contractDate AS "Date",
                clients.name_ AS "Client",
                agents.name_ AS "Clients Agent",
                loads.referenceNo AS "Reference",
                loads.rate AS "Rate",
                loads.dateInvoice AS "Invoice Date",
                loads.amountPaid AS "Amount Paid",
                loads.datePaid AS "Date Paid",
                loads.notes AS "Notes",
                loads.delivered AS "Delivered",
                loads.invoiced AS "invoiced",
                loads.paid AS "Paid",
                loads.paidHCarrier AS "Paid H Carrier",
                loads.completed AS "Completed"
                FROM loads
                LEFT JOIN carriers contracting ON contracting.id = loads.idContracting
                LEFT JOIN carriers hauling ON hauling.id = loads.idHauling
                LEFT JOIN trucks ON trucks.id = loads.idTruck
                LEFT JOIN trailers ON trailers.id = loads.idTrailer
                LEFT JOIN drivers ON drivers.id = loads.idDriver
                LEFT JOIN clients ON clients.id = loads.idClient
                LEFT JOIN clients_agents agents ON agents.id = loads.idClientAgent
                ORDER BY loads.contractDate DESC
                ;
        '''
        self.newRecordSql = ''' INSERT INTO loads (idContracting, idHauling, idTruck,
            idTrailer, idDriver, idClient, idClientAgent, contractDate, referenceNo,
            rate, amountPaid, datePaid, notes, delivered, invoiced, paid, paidHCarrier, 
            completed) VALUES '''
        
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        if not constants.carriersItems: 
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
            idVar = self.id_.getInfo()
            client =self.client.getInfo()
            reference =self.reference.getInfo()
            text = f'''Delete load record:
            id: {idVar}
            Client/Broker: {client}
            Reference No. : {reference}'''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutTabsFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.title.deleteLater()
        self.titleLayoutBox.setMinimumHeight(40)

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

        self.list.treeview.selectionModel().selectionChanged.connect(self.loadSelectionChange)

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

    def payOpen(self):
        self.pay = pay.main()
        self.tabsWidget.addTab(self.pay, '   PAYMENTS   ')
        self.tabsWidget.setCurrentWidget(self.pay)
        self.pay.treeview.proxyModel.setSourceModel(self.list.proxyModel)
        self.pay.configureColumns()
        self.pay.setTotals()

    def stopsOpen(self):
        self.stops = stops.main()
        self.tabsWidget.addTab(self.stops, '   STOPS   ')
        self.tabsWidget.setCurrentWidget(self.stops)
        idLoad = self.id_.text()
        #set items to current selection 
        if idLoad:
            #set the values for idLoad and id Carrier on List for to be used on requery
            self.stops.idLoad = idLoad
            self.stops.screenshotItems.carrier.setText(self.contracting.getInfo())
            self.stops.screenshotItems.loadNo.setText(self.reference.getInfo())
        else:
            self.stops.idLoad = 0
        self.stops.requery()

    def milesOpen(self):
        self.miles = miles.main()
        self.tabsWidget.addTab(self.miles, '   MILES   ')
        self.tabsWidget.setCurrentWidget(self.miles)
        idLoad = self.id_.text()
        #set items to current selection 
        if idLoad:
            self.miles.idLoad = idLoad
        else:
            self.miles.idLoad = 0
        self.miles.requery()

    def invoiceOpen(self):
        self.invoice = invoice.main()#r! CHANGE
        self.tabsWidget.addTab(self.invoice, '   INVOICE   ')
        self.tabsWidget.setCurrentWidget(self.invoice)
        idLoad = self.id_.text()
        #set items to current selection 
        if idLoad:
            self.invoice.loadFolder = self.filesFolder.txtFilePath
        else:
            self.invoice.loadFolder = ''
        self.miles.requery()

    def contractingBookOpen(self):
        self.contractingBook = bookkeeping.main()
        self.tabsWidget.addTab(self.contractingBook, '   CONTRACTING $$   ')
        self.tabsWidget.setCurrentWidget(self.contractingBook)
        idLoad = self.id_.text()
        idCarrier = self.contracting.getDbInfo()# DIFF WITH HAULING
        if idLoad and idCarrier:
            self.contractingBook.idLoad = idLoad
            self.contractingBook.idCarrier = idCarrier
        else:
            self.contractingBook.idLoad = 0
            self.contractingBook.idCarrier = 0
        self.contractingBook.requery()

    def haulingBookOpen(self):
        self.haulingBook = bookkeeping.main()
        self.tabsWidget.addTab(self.haulingBook, '   HAULING $$   ')
        self.tabsWidget.setCurrentWidget(self.haulingBook)
        idLoad = self.id_.text()
        idCarrier = self.hauling.getDbInfo()# DIFF WITH HAULING
        if idLoad and idCarrier:
            self.haulingBook.idLoad = idLoad
            self.haulingBook.idCarrier = idCarrier
        else:
            self.haulingBook.idLoad = 0
            self.haulingBook.idCarrier = 0
        self.haulingBook.requery()

    def dieselOpen(self):
        self.diesel = diesel.main()
        self.tabsWidget.addTab(self.diesel, '   DIESEL   ')
        self.tabsWidget.setCurrentWidget(self.diesel)
        idLoad = self.id_.text()
        idCarrier = self.hauling.getDbInfo()# DIFF WITH HAULING
        if idLoad and idCarrier:
            self.diesel.idLoad = idLoad
            self.diesel.idCarrier = idCarrier
            if self.diesel.addForm:
                self.diesel.addForm.idCarrier = idCarrier
                self.diesel.addForm.requery()
        else:
            self.diesel.idLoad = 0
            self.diesel.idCarrier = 0
            if self.diesel.addForm:
                self.diesel.addForm.idCarrier = 0
        self.diesel.requery()

    def loadSelectionChange(self):
        idLoad = self.id_.getInfo()
        if idLoad:
            date = self.contractDate.getInfo()
            client = self.client.getInfo()
            self.tabsWidget.setTabText(0, f'{idLoad}  |  {date}  |  {client}')
        else: self.tabsWidget.setTabText(0, 'MAIN')
        self.idLoad = idLoad
        idCCarrier = self.contracting.getDbInfo()
        idHCarrier = self.hauling.getDbInfo()
        
        counter = 0
        while counter < self.tabsWidget.count():
            if self.tabsWidget.widget(counter) == self.contractingBook:
                if idLoad and idCCarrier:
                    #set the values for idLoad and id Carrier on List for to be used on requery
                    self.contractingBook.idLoad = idLoad
                    self.contractingBook.idCarrier = idCCarrier
                    #set the filter values for the list of account transactions
                    # self.cCarrierAccounting.accounting.addList.carrierFilter_.populate(idCCarrier)
                    # self.cCarrierAccounting.accounting.form.clear()
                    # self.cCarrierAccounting.accounting.setCarrierAccount()
                else: 
                    self.contractingBook.idLoad = 0
                    self.contractingBook.idCarrier = 0
                self.contractingBook.requery()
            
            if self.tabsWidget.widget(counter) == self.haulingBook:
                if idLoad and idHCarrier:
                    #set the values for idLoad and id Carrier on List for to be used on requery
                    self.haulingBook.idLoad = idLoad
                    self.haulingBook.idCarrier = idHCarrier
                    #set the filter values for the list of account transactions
                    # self.cCarrierAccounting.accounting.addList.carrierFilter_.populate(idCCarrier)
                    # self.cCarrierAccounting.accounting.form.clear()
                    # self.cCarrierAccounting.accounting.setCarrierAccount()
                else: 
                    self.haulingBook.idLoad = 0
                    self.haulingBook.idCarrier = 0
                self.haulingBook.requery()

            if self.tabsWidget.widget(counter) == self.diesel:
                if idLoad and idHCarrier:
                    #set the values for idLoad and id Carrier on List for to be used on requery
                    self.diesel.idLoad = idLoad
                    self.diesel.idCarrier = idHCarrier
                    if self.diesel.addForm:
                        self.diesel.addForm.idCarrier = idHCarrier
                        self.diesel.addForm.requery()
                    #set the filter values for the list of account transactions
                    # self.cCarrierAccounting.accounting.addList.carrierFilter_.populate(idCCarrier)
                    # self.cCarrierAccounting.accounting.form.clear()
                    # self.cCarrierAccounting.accounting.setCarrierAccount()
                else: 
                    self.diesel.idLoad = 0
                    self.diesel.idCarrier = 0
                    if self.diesel.addForm:
                        self.diesel.addForm.idCarrier = 0
                self.diesel.requery()
                
            # elif self.tabDetailsWidget.widget(counter) == self.diesel:
            #     if idLoad and idHCarrier:
            #         #set the values for idLoad and id Carrier on List for to be used on requery
            #         self.diesel.displayForm.idLoad = idLoad
            #         self.diesel.displayForm.idCarrier = idHCarrier
            #         if self.diesel.addForm: #if hasattr(self.diesel, "addForm"):
            #             self.diesel.addForm.idCarrier = idHCarrier
            #             self.diesel.addForm.idLoad = idLoad

                # else:
                #     self.diesel.displayForm.idLoad = 0
                #     self.diesel.displayForm.idCarrier = 0
                #     # if hasattr(self.diesel, "addForm"):
                #     if self.diesel.addForm:
                #         self.diesel.addForm.idCarrier = 0
                #         self.diesel.addForm.idLoad = 0

                # self.diesel.displayForm.requery()
                # if self.diesel.addForm:
                # # if hasattr(self.diesel, "addForm"):
                #     self.diesel.addForm.requery()
            
            # elif self.tabDetailsWidget.widget(counter) == self.miles:
            #     if idLoad:
            #         #set the values for idLoad and id Carrier on List for to be used on requery
            #         self.miles.idLoad = idLoad
            #         if self.miles.addForm: #if hasattr(self.diesel, "addForm"):
            #             self.miles.addForm.idLoad = idLoad
            #     else:
            #         self.miles.idLoad = 0
            #         if self.miles.addForm:
            #             self.miles.addForm.idLoad = 0

            #     self.miles.requery()
            #     if self.miles.addForm:
            #         self.miles.addForm.requery()
            
            if self.tabsWidget.widget(counter) == self.stops:
                if idLoad:
                    self.stops.idLoad = idLoad
                    self.stops.screenshotItems.carrier.setText(self.contracting.getInfo())
                    self.stops.screenshotItems.loadNo.setText(self.reference.getInfo())
                else:
                    self.stops.idLoad = 0
                self.stops.requery()

            elif self.tabsWidget.widget(counter) == self.miles:
                if idLoad:
                    self.miles.idLoad = idLoad
                else:
                    self.miles.idLoad = 0
                self.miles.requery()

            # elif self.tabDetailsWidget.widget(counter) == self.invoice:
            #     if idLoad:
            #         self.invoice.idLoad = idLoad
            #     else:
            #         self.invoice.idLoad = 0
            #     self.invoice.requery()
            counter +=1


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())