#!/usr/bin/python3
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from globalElements.treeview import treeviewSearchBox
from globalElements.widgets import (labelWidget, incomeExpenseRadioButtons,
    truFalseRadioButtons, cboFilterGroup)
from globalElements import constants, modelEmpty, DB
import locale
locale.setlocale(locale.LC_ALL,"")
from decimal import *
import re

class main(modelEmpty.main):
    def __init__(self):
        super().__init__()

        mainWidget = list()
        self.layoutmain.insertWidget(1, mainWidget)
    
    def setGlobalVariables(self):
        self.titleText = "LOAD PAYMENT AMOUNT AND DATES"
        self.size_ = 'h1'

class list(qtw.QWidget): 
    def __init__(self, fontSize=12, rowHeight=60):
        super().__init__()
        self.sortColumn = 1
        self.fontSize = fontSize
        self.rowHeight = rowHeight
        self.sortOrder = qtc.Qt.SortOrder.DescendingOrder
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        
        
        
        self.initUi()
        self.requery()
        # self.setCentralWidget(self.treeview)

    def initUi(self):
        self.createProxyModels()
        self.createTreeView()
        self.createDetailsPane()
        self.createFiltersPane()
        self.setConnections()
        
        

        self.layout_ = qtw.QGridLayout()
        self.layout_.addWidget(self.treeview,0,0,2,1)
        self.layout_.addWidget(self.detailsPane,0,1)
        self.layout_.setAlignment(self.detailsPane, qtc.Qt.AlignmentFlag.AlignVCenter)
        self.layout_.addWidget(self.filtersPane,1,1)
        self.layout_.setAlignment(self.filtersPane, qtc.Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout_)

    def setTotals(self):
        amounts = self.treeview.getColumnValues((6,8))

        total = Decimal('0.00') 
        incomes = Decimal('0.00') 
        expenses = Decimal('0.00') 
        for i in amounts:
            if i[0]:
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


    def createProxyModels(self):
        self.proxyIncome =  qtc.QSortFilterProxyModel()
        self.proxyBusiness =  qtc.QSortFilterProxyModel()
        self.proxypaidHCarrier =  qtc.QSortFilterProxyModel()
        self.proxyYear =  qtc.QSortFilterProxyModel()
        self.proxyMonth =  qtc.QSortFilterProxyModel()
        self.proxyCarrier = qtc.QSortFilterProxyModel()
        # self.proxyHcarrier = qtc.QSortFilterProxyModel()
        self.proxyClient =  qtc.QSortFilterProxyModel()
    
    def createTreeView(self):
        #g! Treeview
        self.treeview = treeviewSearchBox(self.fontSize, self.sortColumn, self.sortOrder)
        horizonatalLabels = ['IdLoad',"Pickup", "Client", "Hauling", "Contracting",
            "Trans Date", "Amount", "Details", "Income", "Business", "Categorie",
            'Paid', 'Paid Hauling Carrier','Year', 'Month']
        self.treeview.standardModel.setHorizontalHeaderLabels(horizonatalLabels)   
        
        #o! list of columns index and their width to set on treeview
        columnsWidth = ((0,70),(1,110),(2,220),(6,120),(7,120))
        self.treeview.setColumnsWith(columnsWidth)
          
        #o! list of columns index to be hidden
        columnsHidden = (3,4,7,8,9,10,11,12,13,14)#(0,1,2,3,4,5,6,7,9,10,11,12,13,14)#13,14,15,16,17
        self.treeview.setHiddenColums(columnsHidden)

        


    def createDetailsPane(self):
        self.detailsPane = qtw.QWidget()
        self.detailsPane.setSizePolicy(qtw.QSizePolicy.Policy.Fixed,qtw.QSizePolicy.Policy.Fixed)
        self.totals = labelWidget('', 18, True)
        self.totals.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
        self.income = labelWidget('', 14)
        self.income.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
        self.expenses = labelWidget('', 14, fontColor='red')
        self.expenses.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)

        self.detailsPaneLayout = qtw.QFormLayout()
        self.detailsPaneLayout.addRow(labelWidget("Income:", 14), self.income)
        self.detailsPaneLayout.addRow(labelWidget("Expenses:", 14), self.expenses)
        self.detailsPaneLayout.addRow(labelWidget("Total:", 18, True), self.totals)

        self.detailsPane.setLayout(self.detailsPaneLayout)
    
    def createFiltersPane(self):
        self.filtersPane = qtw.QWidget()
        self.filtersPane.setSizePolicy(qtw.QSizePolicy.Policy.Fixed,qtw.QSizePolicy.Policy.Fixed)
        self.filtersPaneLayout = qtw.QFormLayout()
        # self.filtersPaneLayout.setAlignment()
        
        filterSize = 14
        
        self.incomeFilter  = incomeExpenseRadioButtons()
        self.filtersPaneLayout.addRow(labelWidget('Income/Expense:', filterSize), self.incomeFilter)

        # self.businessFilter = gw.truFalseRadioButtons()
        # self.businessFilter.true.setChecked(True)
        # self.filtersPaneLayout.addRow(gw.label('Business:', filterSize), self.businessFilter)

        self.paidHCarrierFilter = truFalseRadioButtons()
        self.filtersPaneLayout.addRow(labelWidget('Paid H Carrier:', filterSize), self.paidHCarrierFilter)

        if not constants.yearsItems:
            constants.queryYears()
        self.yearFilter = cboFilterGroup(filterSize, items=constants.yearsItems)
        self.filtersPaneLayout.addRow(labelWidget('Year:', filterSize), self.yearFilter)

        if not constants.monthsItems:
            constants.queryMonths()
        self.monthFilter = cboFilterGroup (filterSize,
            items=constants.monthsItems)
        self.filtersPaneLayout.addRow(labelWidget('Month:', filterSize), self.monthFilter)

        self.clientFilter = cboFilterGroup(filterSize)
        self.filtersPaneLayout.addRow(labelWidget('Client:', filterSize), self.clientFilter)
        
        self.carrierFiltros = cboFilterGroup(filterSize, items=constants.carriersDict)
        self.filtersPaneLayout.addRow(labelWidget('C Carrier:', filterSize), self.carrierFiltros)

        # self.hCarrierFilter =  gwa.cboFilterGroupCompleter(constants.carriers, filterSize)
        # self.filtersPaneLayout.addRow(gw.label('H Carrier:', filterSize), self.hCarrierFilter)

        self.filtersPane.setLayout(self.filtersPaneLayout)


    def setConnections(self):
        self.treeview.actRefresh.triggered.connect(lambda: self.requery())
        self.treeview.actClearFilters.triggered.connect(self.clearAllFilters)
        #Filtros
        self.incomeFilter.income.toggled.connect(self.incomeFilterApply)
        self.incomeFilter.expense.toggled.connect(self.incomeFilterApply)
        # self.businessFilter.true.toggled.connect(self.businessFilterApply)
        # self.businessFilter.false.toggled.connect(self.businessFilterApply)
        self.paidHCarrierFilter.true.toggled.connect(self.paidHCarrierFilterApply)
        self.paidHCarrierFilter.false.toggled.connect(self.paidHCarrierFilterApply)
        self.yearFilter.cbo.currentIndexChanged.connect(lambda: self.yearFilterApply())
        self.monthFilter.cbo.currentIndexChanged.connect(lambda: self.monthFilterApply())
        self.clientFilter.cbo.currentIndexChanged.connect(lambda: self.clientFilterApply())
        self.carrierFiltros.cbo.currentIndexChanged.connect(lambda: self.cCarrierFilterApply())
        # self.carrierFiltros.cbo.currentTextChanged.connect(lambda: self.carrierFilterRun())
        # self.hCarrierFilter.cbo.currentIndexChanged.connect(lambda: self.hCarrierFilterApply())
        #G! connections for totals
        self.treeview.proxyModel.dataChanged.connect(self.setTotals)
        self.treeview.proxyModel.rowsInserted.connect(self.setTotals)
        self.treeview.proxyModel.rowsRemoved.connect(self.setTotals) 

    def requery(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        #Remove all rows
        self.treeview.removeAllRows()
        # Get all records from Database
        records =  self.selectAll()
        #Ceate groups for each carrier
        self.treeview.addRecordsCarriers(records, 3,self.fontSize, self.rowHeight,True)
        #go through the filters and sort the items. 
        self.incomeFilterApply()
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        
    def incomeFilterApply(self):
        filterText = self.incomeFilter.getInfo()#True or false values
        self.proxyIncome.setSourceModel(self.treeview.standardModel)
        self.proxyIncome.setFilterFixedString(filterText)
        self.proxyIncome.setFilterKeyColumn(8)
        self.paidHCarrierFilterApply()

    # def businessFilterApply(self):
    #     filterText = self.businessFilter.getInfo()#True or false values
    #     self.proxyBusiness.setSourceModel(self.proxyIncome)
    #     self.proxyBusiness.setFilterFixedString(filterText)
    #     self.proxyBusiness.setFilterKeyColumn(8)
    #     self.paidHCarrierFilterApply()

    def paidHCarrierFilterApply(self):
        filterText = self.paidHCarrierFilter.getInfo()#True or false values
        self.proxypaidHCarrier.setSourceModel(self.proxyIncome)
        self.proxypaidHCarrier.setFilterFixedString(filterText)
        self.proxypaidHCarrier.setFilterKeyColumn(11)
        self.yearFilterApply()

    def yearFilterApply(self):
        filterText = self.yearFilter.cbo.getInfo()#True or false values
        self.proxyYear.setSourceModel(self.proxypaidHCarrier)
        self.proxyYear.setFilterFixedString(filterText)
        self.proxyYear.setFilterKeyColumn(12)
        self.monthFilterApply()

    def monthFilterApply(self):
        filterText = self.monthFilter.cbo.getInfo()#True or false values
        self.proxyMonth.setSourceModel(self.proxyYear)
        self.proxyMonth.setFilterFixedString(filterText)
        self.proxyMonth.setFilterKeyColumn(13)
        self.cCarrierFilterApply()

    def cCarrierFilterApply(self):
        filterText = self.carrierFiltros.cbo.getInfo()#True or false values
        self.proxyCarrier.setSourceModel(self.proxyMonth)
        self.proxyCarrier.setFilterFixedString(filterText)
        self.proxyCarrier.setFilterKeyColumn(3)
        self.clientFilterApply()

    # def hCarrierFilterApply(self):
    #     filterText = self.hCarrierFilter.cbo.getInfo()#True or false values
    #     self.proxyHcarrier.setSourceModel(self.proxyCCarrier)
    #     self.proxyHcarrier.setFilterFixedString(filterText)
    #     self.proxyHcarrier.setFilterKeyColumn(4)
        
        
        #y!set filter items for client
        noRecords = self.proxyCarrier.rowCount()
        currRow = 0
        records = set([])
        records.add('')
        while currRow < noRecords:
            index = self.proxyCarrier.index(currRow, 2)
            #Add all records to a set fro unique values
            records.add(self.proxyCarrier.data(index))
            currRow +=1
        
        
        recorsList = sorted(records)
        #Utilizar la lista de elementos para el CBO correspondiente
        self.clientFilter.cbo.clear()
        self.clientFilter.cbo.addItems(recorsList)

        #Crear el completer
        completer = qtw.QCompleter(recorsList)
        completer.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.clientFilter.cbo.setCompleter(completer)
        self.clientFilterApply()

    def clientFilterApply(self):
        #Run filter
        filterText = self.clientFilter.cbo.getInfo()#True or false values
        self.proxyClient.setSourceModel(self.proxyCarrier)
        self.proxyClient.setFilterFixedString(filterText)
        self.proxyClient.setFilterKeyColumn(2)

        self.treeview.proxyModel.setSourceModel(self.proxyClient)
        self.treeview.search_afterUpdate(self.sortColumn, self.sortOrder)

    def clearAllFilters(self):
        self.incomeFilter.reSet()
        self.businessFilter.reSet()
        self.paidHCarrierFilter.reSet()
        self.yearFilter.cbo.reSet()
        self.monthFilter.cbo.reSet()
        self.clientFilter.cbo.reSet()
        self.carrierFiltros.cbo.reSet()
        # self.hCarrierFilter.cbo.reSet()
        self.treeview.filtros.txt.clear()

    def selectAll(self):
        self.selectSql = '''
                SELECT 
            loads.id, 
            loads.contractDate AS Pickup, 
            clients.name_ AS "Client",
            carrier.name_ AS Carrier,
            cCarrier.name_ AS C_Carrier,
            -- hCarrier.name_ AS Hauling,

            bookkeeping.date_ as "Transaction Date",
            CONCAT("$", FORMAT(bookkeeping.amount,2)) as "Amount", 
            bookkeeping.description_ as Details, 
            CASE WHEN bookkeeping.isIncome = 1 THEN "Income" ELSE "Expense" END as "Is Income", 

            -- CASE WHEN bookkeeping.business = 1 THEN "True" ELSE "False" END as "Is Business",
            bookkeeping_categories.categorie as Categorie,

            CASE WHEN loads.paid  = 1 THEN "True" ELSE "False" END as Paid, 
            CASE WHEN loads.paidHCarrier  = 1 THEN "True" ELSE "False" END as "Paid Hauling Carrier", 
            IFNULL(YEAR(bookkeeping.date_),'0000') as "Year",
            IFNULL(DATE_FORMAT(bookkeeping.date_, '%m'), '00') as "Month"

            -- We start with the transaction
            FROM bookkeeping 
            -- Joing Accounting loads
            JOIN loads_bookkeeping ON bookkeeping.id = loads_bookkeeping.idBookkeeping
            -- Joing Loads 
            LEFT JOIN loads ON loads_bookkeeping.idLoads = loads.id
            -- Join transaction with the carrier 
            LEFT JOIN carriers carrier ON bookkeeping.idCarrier = carrier.id
            LEFT JOIN clients ON loads.idClient = clients.id 
            -- LEFT JOIN carriers ON loads.idH_Carrier = carriers.id 
            LEFT JOIN carriers cCarrier ON loads.idContracting = cCarrier.id 
            LEFT JOIN bookkeeping_categories ON bookkeeping.idCategorie = bookkeeping_categories.id
            WHERE bookkeeping.isBusiness = 1
            ;
        '''
        records = self.db.get_records_clearNull(self.selectSql)
        self.horizontalLabels = self.db.cursor.column_names
        return records
    
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = list()
    mw.show()
    sys.exit(app.exec())


