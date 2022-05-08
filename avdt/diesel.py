#!/usr/bin/python3
from globalElements import constants, DB, functions as gf, modelMain
from globalElements.widgets import (labelWidget, truFalseRadioButtons, 
    dateWidget, lineEditCurrency, textEdit, lineEdit, cboFilterGroup)
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale
import pathlib
import os
locale.setlocale(locale.LC_ALL,"") 
from decimal import *
import re


# evaluateSaveIndex = (1,)
# listTableValuesIndexes = (0,4,8,10,1,2,11,3,5,9)

class main(modelMain.main):
    def __init__(self):
        super().__init__()
        #o! TEMP - DELETE - JUST FOR TESTING ON ITS OWN - WHEY DB IS OPERATED THEY WILL POPULATE FORM MENU
        constants.queryIftaJuris()
        constants.querybookkeepingTruckingCategories()
        #@abstract methods - def updateRecord - def requery - def btn_delete_pressed
        
        # self.setGlobalVariables()
        self.configure_list()
        self.configure_form()
        
        self.setConnections()

    

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        #1. Get all records
        idCarrier = self.carrierFilter.getDbInfo()
        year = self.yearFilter.getInfo()
        if not year:
            year = '%'
        quarter = self.quarterFilter.getInfo()
        if not quarter:
            quarter = '%'
        month = self.monthFilter.getInfo()
        if not month:
            month = '%'
        if idCarrier:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((int(idCarrier), year, quarter, month))# will pass the cbo value - should be 
            self.list.requery(records, sizeVar=self.listFontSize, rowHeight= self.rowHeight,colorVar='red')
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
            #2. populate accounts filterCbo
            
            self.accountFilterApply()
        else:
            self.list.removeAllRows()
        self.configureColumns()

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            date_ =self.date_.dateEdit.text()
            amount = self.amount.text()
            juris = self.jurisdiction.getInfo()
            gallons = self.gallons.getInfo()
            text = f'''Delete trailer record:
            id: {idVar}
            No: {date_}
            Amount: {amount}
            Juris: {juris}
            Gallons: {gallons}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def setSizes(self):
        self.size_ = "h1"
        self.btnNew.deleteLater()
    
    def mutableVariables(self):
        '''
        This are separated from global so they can be changed in the subfor used in loads
        '''
       # DB INFO
        # self.size_ = "h1"
        
        self.layoutVar = self.formLayoutSideFilesTree
        self.selectSql = '''
            SELECT
                diesel.id AS "ID",
                bookkeeping.id AS "idBookkeeping",
                bookkeeping.date_ AS "Date",
                diesel.gallons AS "Gallons",
                diesel.jurisdiction AS "Juris",
                CONCAT("$", FORMAT(bookkeeping.amount,2)) as "Amount", 
                bookkeeping.description_ AS "Description",
                bookkeeping.anexo AS "5-Anexo",              
                CASE WHEN bookkeeping.isBusiness = 1 THEN "True" ELSE "False" END as "8- IsBusiness",
                bookkeeping.account_ AS "9-Account"
                -- Main Table 
                FROM bookkeeping
                -- Join Statements
                LEFT JOIN bookkeeping_diesel diesel ON  diesel.id = bookkeeping.id
                -- Where condition statements
                WHERE bookkeeping.idCarrier = %s
                AND bookkeeping.idCategorie = 1
                AND YEAR(bookkeeping.date_) LIKE %s
                AND QUARTER(bookkeeping.date_) LIKE %s
				AND DATE_FORMAT(bookkeeping.date_, "%m") LIKE %s
                
                ;'''
        

    def setGlobalVariables(self):
       # DB INFO
        # self.size_ = "h1"
        self.setSizes()
        self.idColumn = 'id' 
        self.tableVar = 'bookkeeping_diesel'
        #position where index = fomvalue index(this is the list order)
        self.listTableValuesIndexes = (0,3,4,1,2,5,6,7,8,9)
        # self.formToDBItems = 4
        self.titleText = "DIESEL"
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (0,1,6,7,8,9)
        self.listColumnWidth = ((2,130),(3,130),(4,130),(5,150) )
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.evaluateSaveIndex = (1,2)
        self.andOr = 'or'
        self.newRecordSql = '''INSERT INTO bookkeeping_diesel (id, gallons, jurisdiction)
        VALUES '''
        self.mutableVariables()

        

        

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                gallons = '{record[1]}',
                jurisdiction = '{record[2]}'
                WHERE {self.idColumn} = {record[0]};'''
        self.db.run_sql_commit(sql)

#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self):
        self.formLayoutSideFilesTree()
        self.filesFolder.setLineEditFileBox(self.fontSize)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        self.idBookkeeping = lineEdit(self.fontSize)#
        self.idBookkeeping.setReadOnly(True)

        self.date_ = dateWidget(self.fontSize)
        
        self.gallons = lineEdit(self.fontSize)
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        self.jurisdiction = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.iftaJuris,
            requeryFunc=constants.queryIftaJuris,
            clearFilter=False
        )
        self.account = cboFilterGroup(
            fontSize= self.fontSize, clearFilter=False )
        self.amount = lineEditCurrency(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.anexoBox = self.filesFolder.layoutLineEditFileBox
        self.anexo = self.filesFolder.lineEditItems.txt
        self.business = truFalseRadioButtons(self.fontSize)

        #p! Form Items - in the same order as needed to save
        self.formItems = [
            self.id_, 
            
            
            self.gallons,
            self.jurisdiction,
            self.idBookkeeping,
            self.date_,
            self.amount,
            self.description, 
            self.anexo, 
            self.business,
            self.account]
        
        self.spacer = qtw.QSpacerItem(0,20)
        # self.layoutForm.addRow(self.title)
        
        self.layoutForm.insertRow(3,self.anexoBox)
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdBookkeeping:', self.fontSize), self.idBookkeeping)
        self.layoutForm.addRow(labelWidget('Business?:', self.fontSize,True, "Blue"), self.business)
        self.layoutForm.addRow(labelWidget('Date:', self.fontSize), self.date_)
        self.layoutForm.addRow(labelWidget('Gallons:', self.fontSize), self.gallons)
        self.layoutForm.addRow(labelWidget('Jurisdiction:', self.fontSize), self.jurisdiction)
        self.layoutForm.addRow(labelWidget('Account:', self.fontSize), self.account)
        self.layoutForm.addRow(labelWidget('Amount:', self.fontSize), self.amount)
        self.layoutForm.addRow(labelWidget('Description', 14, True, "Black" , "center"))
        self.layoutForm.addRow(self.description)
    
    def getCarriers(self):
        if not constants.carriersItems:
            constants.queryCarriers()
        self.carriers = constants.carriersDict.copy()
        del self.carriers['']

    def configure_list(self):
        self.getCarriers()
        self.carrierFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = self.carriers, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            requeryFunc= self.getCarriers            
            )
        self.list.layoutFilter.insertRow(0, labelWidget('Carrier:', self.filterSize), self.carrierFilter)
        
        if not constants.yearsItems:
            constants.queryYears()
        self.yearFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            )
        self.yearFilter.cbo.addItems(constants.yearsItems)
        completer = qtw.QCompleter(constants.yearsItems)
        self.yearFilter.cbo.setCompleter(completer)
        self.list.layoutFilter.insertRow(0, labelWidget('Year:', self.filterSize), self.yearFilter)
 
        self.quarterFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = ["","1","2","3","4"], 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            )
        self.list.layoutFilter.insertRow(0, labelWidget('Quarter:', self.filterSize), self.quarterFilter)

        if not constants.monthsItems:
            constants.queryMonths()
        self.monthFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.monthsItems, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            )
        self.list.layoutFilter.insertRow(0, labelWidget('Month:', self.filterSize), self.monthFilter)

        #will populate when changing client - on requery form
        self.accountFilter = cboFilterGroup(
            fontSize= self.fontSize)

        # self.list.layoutHiddenFilters.addRow(labelWidget('Año:', self.filterSize), self.yearFilter)
        self.list.layoutFilter.insertRow(0,labelWidget('Cuenta:', self.filterSize), self.accountFilter)
        
        #G! CONFIGURE TOTAL  
        self.setTotalsOpt = qtw.QCheckBox()
        self.list.layoutDetails.addRow(labelWidget("Totales:", 11), self.setTotalsOpt)
        
        #g!proxy models
        self.proxyAccount = qtc.QSortFilterProxyModel()

    def setConnections(self):
        self.carrierFilter.cbo.currentIndexChanged.connect(self.carrierFilterAfterUpdate)
        self.list.proxyModel.dataChanged.connect(self.setTotals)
        self.list.proxyModel.rowsInserted.connect(self.setTotals)
        self.list.proxyModel.rowsRemoved.connect(self.setTotals) 
        self.setTotalsOpt.stateChanged.connect(self.setTotals)
        #g! SET FILTER CONNECTIONS
        # self.yearFilter.cbo.currentTextChanged.connect(self.yearFilterApply)
        self.accountFilter.cbo.currentTextChanged.connect(self.accountFilterApply)

        #g! FORM Connections
        #The values we need, are the ones corresponding to the table. 
        #first formDirty parameter is the index corresponding to the table value
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        # self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
        self.account.cbo.currentIndexChanged.connect(lambda: self.formDirty(3,self.account.cbo.getInfo()))
        self.date_.dateEdit.dateChanged.connect(lambda: self.formDirty(4, self.date_.getInfo()))
        self.amount.textChanged.connect(lambda:self.formDirty(5,self.amount.getInfo()))
        # self.isIncome.false.hitButton.connect(lambda: self.formDirty(6, self.isIncome.getInfo()))
        self.description.textChanged.connect(lambda: self.formDirty(7, self.description.getInfo()))
        self.anexo.textChanged.connect(lambda: self.formDirty(8,self.anexo.getInfo()))
        self.business.true.toggled.connect(lambda: self.formDirty(9,self.business.getInfo()))
        
        
    def carrierFilterAfterUpdate(self):
        # self.requery()
        #after updating the carrier filter - carrier should be selected and accounts populated on form
        # No values should be added if filter has not been set to carrier
        idVar = str(self.carrierFilter.getDbInfo())
        # if idVar:
        #Select the corresponding carrier when filter is set
        #get the values from the dictionary that has the bank accounts to use it for the cbo
        if not constants.accountsItems:
            constants.queryAccounts()
        accounts = constants.accountsDict.get(idVar)
        self.account.cbo.clear()
        self.accountFilter.cbo.clear()
        if accounts:
            self.account.cbo.addItems(accounts)
            self.accountFilter.cbo.addItems(accounts)
            completer = qtw.QCompleter(accounts)
            completer.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
            self.account.cbo.setCompleter(completer)
            
            self.accountFilter.cbo.addItems(accounts)
            filtercompleter = qtw.QCompleter(accounts)
            filtercompleter.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
            self.accountFilter.cbo.setCompleter(filtercompleter)
    
    # def getListInfo(self):
    #     i0 = self.id_.getInfo()
    #     i1 = self.date_.getInfo()
    #     i2 = self.amount.getInfo()
    #     i3 = self.description.getInfo()
    #     i4 = str(self.carrier.getDbInfo())
    #     i5 = self.anexo.getInfo()
    #     i6 = str(self.date_.dateEdit.date().year()) 
    #     i7 = str(self.date_.dateEdit.date().toString('MM'))
    #     i9 = self.business.getInfo()
    #     i10 = self.account.getInfo()
    #     # i11 = self.isIncome.getInfo()
    #     record = ([i0, i1,i2,i3,i4,i5,i6,i7,i9,i10])
    #     return record
    
    
    def setFilesFolder(self):
        carrier = self.carrierFilter.getInfo()
        month = self.date_.dateEdit.date().toString('MM')
        year = self.date_.dateEdit.date().toString('yyyy')
        folderPath = self.filesFolder.root
        if not carrier:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        else:
            folderPath = f'{self.filesFolder.root}\{carrier}\Accounting\{year}'
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
            
            folderPath = f'{folderPath}\Expenses'
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
            folderPath = f'{folderPath}\{month}'
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
        self.filesFolder.txtFilePath.setText(folderPath)
    
        

    def setTotals(self):
        widgets = self.list.layoutDetails.rowCount()
        if self.setTotalsOpt.isChecked():
            if widgets == 2:
                self.totals = labelWidget('', 13, True)
                self.totals.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
                self.income = labelWidget('', 11)
                self.income.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
                self.expenses = labelWidget('', 11, False, "Red")
                self.expenses.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
                self.list.layoutDetails.addRow(labelWidget("Income:", 11), self.income)
                self.list.layoutDetails.addRow(labelWidget("Expenses:", 11), self.expenses)
                self.list.layoutDetails.addRow(labelWidget("Total:", 13, True), self.totals)
            
            amounts = self.list.getColumnValues((2,11))
            if amounts:
                total = Decimal('0.00') 
                incomes = Decimal('0.00') 
                expenses = Decimal('0.00') 
                for i in amounts:
                    if i[1] == "Expense":
                        expenses += Decimal(re.sub(r"[^\d.]","", i[0]))
                    elif i[1] == "Income":
                        incomes += Decimal(re.sub(r"[^\d.]","", i[0]))
                    
                total = incomes - expenses
                total = Decimal(total.quantize(Decimal(".01")))
                total = locale.currency(float(total), grouping=True)
                self.totals.setText(str(total))

                incomes = Decimal(incomes.quantize(Decimal(".01")))
                incomes = locale.currency(float(incomes), grouping=True)
                self.income.setText(incomes)

                expenses = Decimal(expenses.quantize(Decimal(".01")))
                expenses = locale.currency(float(expenses), grouping=True)
                self.expenses.setText(expenses)
        else:  
            if widgets == 5:
                self.list.layoutDetails.removeRow(2)
                self.list.layoutDetails.removeRow(2)
                self.list.layoutDetails.removeRow(2)
            
    def removeAllFilters(self):
        if self.yearFilter.cbo.currentText():
            self.yearFilter.reSet() 
        if self.monthFilter.currentText():
            self.monthFilter.reSet()
        if self.accountFilter.cbo.currentText():
            self.accountFilter.cbo.reSet()
        if self.list.filtros.txt.text():
            self.list.filtros.txt.reSet()


    def accountFilterApply(self):
        filterText = self.accountFilter.currentText()
        self.proxyAccount.setSourceModel(self.list.standardModel)
        self.proxyAccount.setFilterFixedString(filterText)
        self.proxyAccount.setFilterKeyColumn(9)

        self.list.proxyModel.setSourceModel(self.proxyAccount)
        self.list.search_afterUpdate(self.sortColumn, self.sortOrder)

    def save_record_toDb(self, newRecord):
        record = self.getDBInfo()
        
        # dieselRecord = dieselRecord[]
        queryRecord = record.copy()
        queryRecord = gf.recordToSQL(queryRecord)
        dieselRecord = queryRecord[1:3]
        
        bookkeepingRecord = queryRecord[3:10]
        dieselRecord.insert(0, bookkeepingRecord[0])

        if newRecord:
            idVar = self.insertNewRecord(dieselRecord)
            # form item 0 should always hold the id value
            self.formItems[0].populate(str(idVar))
        else:
            self.updateRecord(dieselRecord)
        
        sql =f'''UPDATE bookkeeping SET 
                date_ = '{bookkeepingRecord[1]}',
                amount = '{bookkeepingRecord[2]}',
                description_ = '{bookkeepingRecord[3]}',
                anexo = '{bookkeepingRecord[4]}',
                isBusiness  = '{bookkeepingRecord[5]}',
                account_ = '{bookkeepingRecord[6]}'
                WHERE id = {bookkeepingRecord[0]};'''
        self.db.run_sql_commit(sql)
    


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())