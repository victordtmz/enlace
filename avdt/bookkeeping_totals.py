#!/usr/bin/python3
import sys
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from globalElements import constants, DB, modelList
from globalElements.widgets import labelWidget, buttonWidget, cboFilterGroup


class main(modelList.main): 
    def __init__(self):
        super().__init__()

        self.configure_list()
        self.configureButtons()
        self.setConnectionsLocal()
        self.requery()
        # self.db = DB_MySql

    # def getConstantsValues(self):
    #     if not constants.carriersItems:
    #         constants.queryCarriers()
        
    #     if not constants.yearsItems:
    #         constants.queryYears()
        # constants.queryAccountingYear()
        # constants.queryDieselJurisdictions()
        # constants.queryAccountingCategories()


    def setGlobalVariables(self):
        self.thisFileName = "AVDT_Accounting_totals"
        self.titleText = "EXPENSES AND INCOME TOTALS"
        self.mainSize = "h1"
        self.size_ = "h1"

        # LIST INFO
        self.horizonatalLabels = ["Total","Categoria"]
        self.sortColumn = 2
        self.fontSize = 13
        self.rowHeight = 32
        self.listFontSize = 13
        self.sortOrder = qtc.Qt.SortOrder.DescendingOrder
        self.listHiddenItems = ()
        self.listColumnWidth = ((0,150),(2,120))
        self.filterSize = 11
        self.listWidth = 10
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
        SELECT 
            CONCAT("$", FORMAT(SUM(trans.amount),2)) AS "TOTAL",
            cat.categorie as "Categorie"
        
        FROM bookkeeping trans

        LEFT JOIN bookkeeping_categories cat ON  cat.id = trans.idCategorie
        WHERE trans.idCarrier = %s
        AND YEAR(trans.date_) LIKE %s
        AND DATE_FORMAT(trans.date_, '%m') LIKE %s
        AND isBusiness = 1
        GROUP BY cat.categorie
        ;
        '''
        
    
    def requery(self):
        year = "%"
        yearVar = self.yearFilter.getInfo()
        if yearVar:
            year = yearVar
        month = "%"
        monthVar = self.monthFilter.getInfo()
        if monthVar:
            month = monthVar
        idCarrier = self.carrierFilter.getDbInfo()
        if idCarrier:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((int(idCarrier), year, month))# will pass the cbo value - should be 
            self.list.requery(records, self.listFontSize, self.rowHeight, "Red")
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
        else:
            self.list.removeAllRows()
        self.configureColumns() 

    def configureButtons(self):
        self.btnRequery = buttonWidget(text="   Obtener registros", icon=constants.iconRefresh, size=self.mainSize)
        self.titleLayout.insertWidget(0, self.btnRequery)

    def setConnectionsLocal(self):
        # self.carrierFilter.cbo.currentIndexChanged.connect(self.requery)
        self.btnRequery.pressed.connect(self.requery)

    def configure_list(self):
        #g! FILTER ITEMS
        if not constants.carriersItems:
            constants.queryCarriers()
        carriers = constants.carriersDict.copy()
        del carriers[""]
        self.carrierFilter = cboFilterGroup(
            fontSize= self.fontSize, 
            items = carriers, 
            completionMode=qtw.QCompleter.CompletionMode.InlineCompletion,
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
        self.list.layoutFilter.insertRow(0, labelWidget('Month:', self.filterSize), self.monthFilter)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())