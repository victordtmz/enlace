#!/usr/bin/python3
from globalElements import constants, DB, mainModel
from globalElements.widgets import (labelWidget, truFalseRadioButtons, incomeExpenseRadioButtons,
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

class main(mainModel.main):
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
        if idCarrier:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((int(idCarrier), year))# will pass the cbo value - should be 
            self.list.requeryColorAccounting(records, 
                isIncomeColumn=10,isBusinessColumn= 8, sizeVar=self.listFontSize, rowHeight= self.rowHeight)
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
            #2. populate accounts filterCbo
            
            self.monthFilterApply()
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
            text = f'''Delete trailer record:
            id: {idVar}
            No: {date_}
            Amount: {amount}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        pass

    def setGlobalVariables(self):
       # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'bookkeeping'
        self.listTableValuesIndexes = (0,4,7,9,1,2,10,3,5,8)
        # self.formToDBItems = 4
        self.titleText = "BOOKKEEPING"
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (4,5,6,7,8,9,10)
        self.listColumnWidth = ((1,100),(2,100),(3,300) )
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.evaluateSaveIndex = (1,3,5)
        self.selectSql = '''
            SELECT
                -- DISPLAY VALUES
                bookkeeping.id AS "ID",
                bookkeeping.date_ AS "Date",
                CONCAT("$", FORMAT(bookkeeping.amount,2)) as "Amount", 

                bookkeeping.description_ AS "Description",

                -- HIDDEN VALUES
                bookkeeping.idCarrier AS "4-Carrier",
                -- bookkeeping.idCategorie AS "5-Categorie",
                bookkeeping.anexo AS "5-Anexo",

                -- FILTER VALUES
                DATE_FORMAT(bookkeeping.date_, '%m') AS "6-Month",
                categories.categorie "7-Categorie",
                CASE WHEN bookkeeping.isBusiness = 1 THEN "True" ELSE "False" END as "8- IsBusiness",
                bookkeeping.account_ AS "9-Account",
                CASE WHEN bookkeeping.isIncome = 1 THEN "Income" ELSE "Expense" END as "10-Type"
                -- Main Table 
                FROM bookkeeping
                -- Join Statements
                LEFT JOIN bookkeeping_categories categories ON  categories.id = bookkeeping.idCategorie
                -- Where condition statements
                WHERE bookkeeping.idCarrier = %s
                AND YEAR(bookkeeping.date_) LIKE %s
                ;'''

        self.newRecordSql = '''
            INSERT INTO bookkeeping (idCarrier, idCategorie,
                account_, date_, amount, isIncome, description_,
                anexo, isBusiness) VALUES'''

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idCarrier = '{record[1]}',
                idCategorie = '{record[2]}',
                account_ = '{record[3]}',
                date_ = '{record[4]}',
                amount = '{record[5]}',
                isIncome = '{record[6]}',
                description_ = '{record[7]}',
                anexo = '{record[8]}',
                isBusiness  = '{record[9]}'
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
        
        if not constants.carriersItems:
            constants.queryCarriers()
        self.carrier = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.carriersDict, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            requeryFunc= constants.queryCarriers,   
            clearFilter=False         
            )
        
        if not constants.bookkeepingTruckingCategoriesList:
            constants.querybookkeepingTruckingCategories()
        self.categorie = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.bookkeepingTruckingCategoriesDict, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            requeryFunc= constants.querybookkeepingTruckingCategories,
            clearFilter=False        
            )
        

        self.account = cboFilterGroup(
            fontSize= self.fontSize, clearFilter=False )
        self.date_ = dateWidget(self.fontSize)
        self.amount = lineEditCurrency(self.fontSize)
        self.isIncome = incomeExpenseRadioButtons(self.fontSize)
        self.description = textEdit(self.fontSize)

        #o! ADD TO TREE
        self.anexoBox = self.filesFolder.layoutLineEditFileBox
        self.anexo = self.filesFolder.lineEditItems.txt
        # self.anexo.lineEditItems.lbl.setText('Attachment: ')
        # self.anexo.filesTree = self.filesFolder

        self.business = truFalseRadioButtons(self.fontSize)

        #p! Form Items
        self.formItems = [
            self.id_, 
            self.carrier, 
            self.categorie, 
            self.account, 
            self.date_, 
            self.amount,
            self.isIncome, 
            self.description, 
            self.anexo, 
            self.business]
        
        self.spacer = qtw.QSpacerItem(0,20)
        # self.layoutForm.addRow(self.title)
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.insertRow(3,self.anexoBox)
        # self.layoutForm.addRow(self.isBusiness)
        self.layoutForm.addRow(labelWidget('Business?:', self.fontSize,True, "Blue"), self.business)
        
        self.layoutForm.addRow(labelWidget('Carrier:', self.fontSize), self.carrier)
        self.layoutForm.addRow(labelWidget('Account:', self.fontSize), self.account)
        self.layoutForm.addRow(labelWidget('Category:', self.fontSize), self.categorie)
        
        self.layoutForm.addRow(labelWidget('Date:', self.fontSize), self.date_)
        self.layoutForm.addRow(labelWidget('Amount:', self.fontSize), self.amount)
        self.layoutForm.addRow(labelWidget('Type:', self.fontSize), self.isIncome)
        
        self.layoutForm.addRow(labelWidget('Description', 16, True, "Blue" , "center"))
        self.layoutForm.addRow(self.description)
        
    def configure_list(self):
        if not constants.carriersItems:
            constants.queryCarriers()
        self.carrierFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.carriersDict, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            requeryFunc= constants.queryCarriers            
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
        
        if not constants.monthsItems:
            constants.queryMonths()
        self.monthFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.monthsItems, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            )

        if not constants.bookkeepingTruckingCategoriesList:
            constants.querybookkeepingTruckingCategories()
        self.categoriesFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = constants.bookkeepingTruckingCategoriesDict, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
            requeryFunc= constants.querybookkeepingTruckingCategories()            
            )
       
        self.businessFilter = truFalseRadioButtons(fontSize=self.filterSize, filter=True)
        self.incomeExpenseFilter = incomeExpenseRadioButtons(self.filterSize, filter=True)
        #will populate when changing client - on requery form
        self.accountFilter = cboFilterGroup(
            fontSize= self.fontSize)

        # self.list.layoutHiddenFilters.addRow(labelWidget('Año:', self.filterSize), self.yearFilter)
        self.list.layoutHiddenFilters.addRow(labelWidget('Mes:', self.filterSize), self.monthFilter)
        self.list.layoutHiddenFilters.addRow(labelWidget('Categoria:', self.filterSize), self.categoriesFilter)
        self.list.layoutHiddenFilters.addRow(labelWidget('Cuenta:', self.filterSize), self.accountFilter)
        self.list.layoutHiddenFilters.addRow(labelWidget('Business:', self.filterSize), self.businessFilter)
        self.list.layoutHiddenFilters.addRow(labelWidget('Tipo:', self.filterSize), self.incomeExpenseFilter)
        
        #G! CONFIGURE TOTAL  
        self.setTotalsOpt = qtw.QCheckBox()
        self.list.layoutDetails.addRow(labelWidget("Totales:", 11), self.setTotalsOpt)
        
        #g!proxy models
        # self.proxyYear = qtc.QSortFilterProxyModel()
        self.proxyMonth = qtc.QSortFilterProxyModel()
        self.proxyCategorie = qtc.QSortFilterProxyModel()
        self.proxyBusiness = qtc.QSortFilterProxyModel()
        self.proxyAccount = qtc.QSortFilterProxyModel()
        self.proxyIncomeExpense = qtc.QSortFilterProxyModel()


    def setConnections(self):
        self.carrierFilter.cbo.currentIndexChanged.connect(self.carrierFilterAfterUpdate)
        self.list.proxyModel.dataChanged.connect(self.setTotals)
        self.list.proxyModel.rowsInserted.connect(self.setTotals)
        self.list.proxyModel.rowsRemoved.connect(self.setTotals) 
        self.setTotalsOpt.stateChanged.connect(self.setTotals)
        #g! SET FILTER CONNECTIONS
        # self.yearFilter.cbo.currentTextChanged.connect(self.yearFilterApply)
        self.monthFilter.cbo.currentTextChanged.connect(self.monthFilterApply)
        self.categoriesFilter.cbo.currentTextChanged.connect(self.categorieFilterApply)
        self.businessFilter.true.toggled.connect(self.businessFilterApply)
        self.businessFilter.false.toggled.connect(self.businessFilterApply)
        self.accountFilter.cbo.currentTextChanged.connect(self.accountFilterApply)
        self.incomeExpenseFilter.income.toggled.connect(self.incomeExpenseFilterApply)
        self.incomeExpenseFilter.expense.toggled.connect(self.incomeExpenseFilterApply)

        #g! FORM Connections
        #The values we need, are the ones corresponding to the table. 
        #first formDirty parameter is the index corresponding to the table value
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        # self.carrier.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.carrier.getInfo()))
        self.carrier.cbo.currentIndexChanged.connect(lambda: self.formDirty(1,self.carrier.getDbInfo()))
        self.categorie.cbo.currentIndexChanged.connect(lambda: self.formDirty(2,self.categorie.getInfo())) 
        self.categorie.cbo.currentTextChanged.connect(lambda: self.formDirty(2,self.categorie.getInfo))
        self.account.cbo.currentIndexChanged.connect(lambda: self.formDirty(3,self.account.cbo.getInfo()))
        self.date_.dateEdit.dateChanged.connect(lambda: self.formDirty(4, self.date_.getInfo()))
        self.amount.textChanged.connect(lambda:self.formDirty(5,self.amount.getInfo()))
        self.isIncome.income.toggled.connect(lambda: self.formDirty(6, self.isIncome.getInfo()))
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
        self.carrier.populate(idVar)
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
    
    
    
    
    
    #p! DATABASE FUNCTIONS ------------------------------
    


    def getListInfo(self):
        i0 = self.id_.getInfo()
        i1 = self.date_.getInfo()
        i2 = self.amount.getInfo()
        i3 = self.description.getInfo()
        i4 = str(self.carrier.getDbInfo())
        i5 = self.anexo.getInfo()
        i6 = str(self.date_.dateEdit.date().year()) 
        i7 = str(self.date_.dateEdit.date().toString('MM'))
        i8 = self.categorie.getInfo()
        i9 = self.business.getInfo()
        i10 = self.account.getInfo()
        i11 = self.isIncome.getInfo()
        record = ([i0, i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11])
        return record
    
    
    def setFilesFolder(self):
        carrier = self.carrier.getInfo()
        month = self.date_.dateEdit.date().toString('MM')
        year = self.date_.dateEdit.date().toString('yyyy')
        isIncome = self.isIncome.getInfo()
        
        folderPath = self.filesFolder.root
        if not carrier:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        else:
            folderPath = f'{self.filesFolder.root}\{carrier}\Accounting\{year}'
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
            if isIncome == "Income":
                folderPath = f'{folderPath}\Income'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
                folderPath = f'{folderPath}\{month}'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
                 
            else:
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
        if self.categoriesFilter.currentText():
            self.categoriesFilter.reSet()
        if self.businessFilter.true.isChecked() or self.businessFilter.false.isChecked():
            self.businessFilter.reSet()
        if self.accountFilter.cbo.currentText():
            self.accountFilter.cbo.reSet()
        if self.list.filtros.txt.text():
            self.list.filtros.txt.reSet()
        if self.incomeExpenseFilter.income.isChecked() or self.incomeExpenseFilter.expense.isChecked():
            self.incomeExpenseFilter.reSet()

    def monthFilterApply(self):
        filterText = self.monthFilter.currentText()
        self.proxyMonth.setSourceModel(self.list.standardModel)
        self.proxyMonth.setFilterFixedString(filterText)
        self.proxyMonth.setFilterKeyColumn(6)
        self.categorieFilterApply()

    def categorieFilterApply(self):
        filterText = self.categoriesFilter.currentText()
        self.proxyCategorie.setSourceModel(self.proxyMonth)
        self.proxyCategorie.setFilterFixedString(filterText)
        self.proxyCategorie.setFilterKeyColumn(7)

        self.businessFilterApply()

    def businessFilterApply(self):
        filterText = self.businessFilter.getInfo()
        self.proxyBusiness.setSourceModel(self.proxyCategorie)
        self.proxyBusiness.setFilterFixedString(filterText)
        self.proxyBusiness.setFilterKeyColumn(8)
        self.accountFilterApply()

    def accountFilterApply(self):
        filterText = self.accountFilter.currentText()
        self.proxyAccount.setSourceModel(self.proxyBusiness)
        self.proxyAccount.setFilterFixedString(filterText)
        self.proxyAccount.setFilterKeyColumn(9)
        self.incomeExpenseFilterApply()

    def incomeExpenseFilterApply(self):
        filterText = self.incomeExpenseFilter.getInfo()
        self.proxyIncomeExpense.setSourceModel(self.proxyAccount)
        self.proxyIncomeExpense.setFilterFixedString(filterText)
        self.proxyIncomeExpense.setFilterKeyColumn(10)

        self.list.proxyModel.setSourceModel(self.proxyIncomeExpense)
        self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
            
    


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())