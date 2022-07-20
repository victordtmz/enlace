#!/usr/bin/python3
from globalElements import constants, DB, modelMain, treeview
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



class main(modelMain.main):
    """Main form that contains all transactions for the different trucking companies

    Args:
        modelMain (_type_): inherits from main model. 
    """
    def __init__(self):
        super().__init__()
        self.configure_list()
        self.configure_form()
        self.setConnections()
        self.carrierFilterAfterUpdate()

    def __repr__(self) -> str:
        return '''Bookkeeping main form, includes the list and form to change values'''

    def requery(self): 
        '''Removes all current rows, queries from database filtering by year and carrier
        all other filters are aplied locally in tree'''
        idCarrier = self.carrierFilter.getDbInfo()
        year = self.yearFilter.getInfo()
        if not year:
            year = '%'
        if idCarrier:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((int(idCarrier), year))# will pass the cbo value - should be 
            self.list.requeryColorAccounting(records, 
                isIncomeColumn=10,isBusinessColumn= 8, sizeVar=self.listFontSize, rowHeight= self.rowHeight)
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
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
        
    def setSizes(self):
        self.size_ = "h1"
    def mutableVariables(self):
        '''
        This are separated from global so they can be changed in the subfor used in loads
        '''
        self.layoutVar = self.formLayoutSideFilesTree
        a = '''--sql'''
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

    def setGlobalVariables(self):
        """Variables that are unique to this instance of the mainModel object used to create the
        combination of List/Form.

        self.listTableValuesIndexes -- contains the indexes of the elements to populate the form in order
        Example: date might be the 4th item on the DB, but needs to be displayed as item 1 in the screen, 
        the index value 4 will be placed in position 1 of this list.
        """
       # DB INFO
        
        # self.size_ = "h1"
        self.setSizes()
        self.idColumn = 'id' 
        self.tableVar = 'bookkeeping'
        # contains the indexes of the elements to populate the form in order
        # Example: date might be the 4th item on the DB, but needs to be displayed as item 1 in the screen, 
        # the index value 4 will be placed in position 1 of this list.
        self.listTableValuesIndexes = (0,4,7,9,1,2,10,3,5,8)
        # self.formToDBItems = 4
        self.titleText = "BOOKKEEPING"
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (0,4,5,6,7,8,9,10)
        self.listColumnWidth = ((1,100),(2,100),(3,300) )
        self.sortColumn = 1
        self.sortOrder = qtc.Qt.SortOrder.DescendingOrder
        
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.evaluateSaveIndex = (1,3,5)
        

        self.newRecordSql = '''
            INSERT INTO bookkeeping (idCarrier, idCategorie,
                account_, date_, amount, isIncome, description_,
                anexo, isBusiness) VALUES'''
        self.mutableVariables()

    def updateRecord(self, record): 
        """Creates the SQL use to update the record on the MySql database and then
        executes the query. 

        Args:
            record (tuple): Tuple that contains the values in the same order as the re set 
            in the DB table, id(0) is used to locate the record.
        """
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
        """Contains the configuration to all the elements of the form part of the 
        object
        """
        # self.formLayoutSideFilesTree()
        self.layoutVar()
        self.filesFolder.setLineEditFileBox(self.fontSize)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        """Defines all the widgets that are going to be used in the form, 
        at a minimum, there must be one widget per object or data element from
        the database.

        The widgets are also organized in a Form Layout to be displaid on the screen.

        The widgets that will display tha database values are organized in a list (self.formItems)
        so the database values can be extracted and used to update the record o create new records.

        self.formItems.  Contains the widgets in the same order as the DB Table, so the extraction of information
        does not have to be re arranged to save to the DB.  The list might not contain the values in order for the 
        population of the widgets when a new record is selected 
        -- self.listTableValuesIndexes -- is used to place the index of the items in the order of population.
        """
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
            fontSize= self.fontSize, clearFilter=False, 
            requeryFunc=self.carrierFilterAfterUpdate )
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
        
        self.layoutForm.addRow(labelWidget('Description', 14, True, "black" , "center"))
        self.layoutForm.addRow(self.description)
        
    def getCarriers(self):
        if not constants.carriersItems:
            constants.queryCarriers()
        self.carriers = constants.carriersDict.copy()
        del self.carriers['']
    
    def configure_list(self):
        self.rowHeight = 72
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
        accounts = constants.accountsDict.get(int(idVar))
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
    
    
    
    
    
    def getListInfo(self):
        i0 = self.id_.getInfo()
        i1 = self.date_.getInfo()
        i2 = self.amount.text()
        i3 = self.description.getInfo()
        i4 = str(self.carrier.getDbInfo())
        i5 = self.anexo.getInfo()
        i6 = str(self.date_.dateEdit.date().toString('MM'))
        i7 = self.categorie.getInfo()
        i8 = self.business.getInfo()
        i9 = self.account.getInfo()
        i10 = self.isIncome.getInfo()
        record = ([i0, i1,i2,i3,i4,i5,i6,i7,i8,i9,i10])
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
    
        

    def calculateTotals(self):
        amounts = self.list.getColumnValues((2,10))#8 is business True/False
        # total = Decimal('0.00') 
        incomes = Decimal('0.00') 
        expenses = Decimal('0.00') 
        if amounts:
            for i in amounts:
                if i[1] == "Expense":
                    expenses += Decimal(re.sub(r"[^\d.]","", i[0]))
                elif i[1] == "Income":
                    incomes += Decimal(re.sub(r"[^\d.]","", i[0]))
            
            return incomes, expenses

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
                
                incomes, expenses = self.calculateTotals()
                    
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