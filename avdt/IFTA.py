#!/usr/bin/python3
from globalElements import constants, modelEmpty, modelList, DB
from globalElements.widgets import buttonWidget, labelWidget, lineEdit, cboFilterGroup
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 
locale.setlocale(locale.LC_ALL,"")
from decimal import *

class diesel(modelList.main):
    def __init__(self):
        super().__init__()
        self.btn_cerrar.deleteLater()
        self.listFontSize = 14
        
        iconSize = qtc.QSize(40,18)
        self.list.toolBar.setIconSize(iconSize)
        self.list.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.list.toolBar)

    def setGlobalVariables(self):
        # self.idCarrier = 0
        # self.sqlFolderName = "AVDT_IFTA_diesel"
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
        SELECT 
            diesel.jurisdiction AS "Juris",
            SUM(diesel.gallons) AS "Gallons"
            
            FROM bookkeeping 
            -- Connect the accounting 
            JOIN carriers ON bookkeeping.idCarrier = carriers.id
            -- connect the load to miles through the many to many table
            JOIN bookkeeping_diesel diesel ON bookkeeping.id = diesel.id
            WHERE carriers.id LIKE %s
            AND YEAR(bookkeeping.date_) LIKE %s
            AND QUARTER(bookkeeping.date_) LIKE %s
            AND DATE_FORMAT(bookkeeping.date_, "%m") LIKE %s
            GROUP BY diesel.jurisdiction;
        '''
        self.size_ = "h2"
        self.titleText = "DIESEL"

        # self.sortOrder = qtc.Qt.SortOrder.AscendingOrder
        self.sortColumn = 0
        self.listHiddenItems = ()
        self.listColumnWidth = ((0,100),)
        self.filterSize = 11
    
    def requery(self, carrier , year,quarter , month):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll((carrier, year, quarter, month))
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        
        self.configureColumns()  
        self.list.search_afterUpdate(self.sortColumn)
        # self.applyFilterJuris()
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()

    def btn_cerrar_pressed(self):
        self.deleteLater()
class miles(modelList.main):
    def __init__(self):
        super().__init__()
        self.btn_cerrar.deleteLater()
        self.listFontSize = 14

        iconSize = qtc.QSize(40,18)
        self.list.toolBar.setIconSize(iconSize)
        self.list.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.list.toolBar)

    def setGlobalVariables(self):
        # self.idCarrier = 0
        # self.sqlFolderName = "AVDT_IFTA_miles"
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
        SELECT 
            miles.juris AS "Juris",
            SUM(miles.miles) AS "Miles"

        
            FROM loads 
            -- get the carrier name from the load
            JOIN carriers ON loads.idHauling = carriers.id
            -- connect the load to miles through the many to many table
            JOIN loads_miles loadMiles ON loads.id = loadMiles.idLoad
            -- use last connection to connect to the miles table
            LEFT JOIN miles ON miles.id = loadMiles.idMiles
            WHERE carriers.id LIKE %s
            AND YEAR(loadMiles.date_) LIKE %s
            AND QUARTER(loadMiles.date_) LIKE %s
            AND DATE_FORMAT(loadMiles.date_, "%m") LIKE %s
            GROUP BY miles.juris;
        '''
        self.size_ = "h2"
        self.titleText = "MILES"

        # self.sortOrder = qtc.Qt.SortOrder.AscendingOrder
        self.sortColumn = 0
        self.listHiddenItems = ()
        self.listColumnWidth = ((0,100),)
        self.filterSize = 11
        # self.listWidth = 4
    
    def requery(self, carrier , year,quarter , month):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll((carrier, year, quarter,month))# will pass the cbo value - should be 
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        
        self.configureColumns()  
        self.list.search_afterUpdate(self.sortColumn)
        
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()

    def btn_cerrar_pressed(self):
        self.deleteLater()

class main(modelEmpty.main):
    def __init__(self):
        super().__init__()
        self.addForm = False
        self.initUi()

        self.configure_form()
        self.configureFilters()
        self.setTotalsElements()
        self.setConnections()
        
    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.titleText = "IFTA"

    def requery(self):
        idCarrier = f"%{self.filterCarrier.getDbInfo()}%"
        year = f"%{self.filterYear.getInfo()}%"
        month = f"%{self.filterMonth.getInfo()}%"
        quarter = f"%{self.filterQuarter.getInfo()}%"
        self.diesel.requery(idCarrier, year,quarter, month )
        self.miles.requery(idCarrier, year,quarter, month)
        self.calculateTotals()
        
#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self): 
        self.diesel = diesel()
        self.miles = miles()
        self.formLayout = qtw.QHBoxLayout()
        self.formLayout.addWidget(self.diesel)
        self.formLayout.addWidget(self.miles)
        self.formLayoutBox = qtw.QWidget()
        self.formLayoutBox.setLayout(self.formLayout)
        self.layoutmain.addWidget(self.formLayoutBox)
        # self.layout_buttons.setAlignment(self.btn_cerrar, qtc.Qt.AlignmentFlag.AlignTop)
    
    def setConnections(self):
        self.btnRequery.pressed.connect(self.requery)
    
    def configureFilters(self):
        #g! Carriers filter
        if not constants.carriersItems:
            constants.queryCarriers()
        carriers = constants.carriersDict.copy()
        del carriers[""]
        del carriers["T M CALVILLO TRANSPORT"]
        self.filterCarrier = cboFilterGroup(
            self.fontSize, 
            items= carriers,
            clearFilter=False
        )

        #g! Jurisdictions filter
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        self.filterJuris = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.iftaJuris,
            requeryFunc=constants.queryIftaJuris,
            clearFilter=True
        )
        #g! years filter
        if not constants.yearsItems:
            constants.queryYears()
        self.filterYear = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.yearsItems,
            clearFilter=True
        )
        #g! month filter
        if not constants.monthsItems:
            constants.queryMonths()
        self.filterMonth = cboFilterGroup(
            self.fontSize, 
            items= constants.monthsItems,
            clearFilter=True
        )
        #g! Quarter filter
        self.filterQuarter = cboFilterGroup(
            self.fontSize, 
            items= ["","1","2","3","4"],
            clearFilter=True
        )

        self.btnRequery = buttonWidget("  Query", "h2_",constants.iconRefresh)

        self.filterLayout = qtw.QFormLayout()
        self.filterLayout.setContentsMargins(0,0,0,0)
        # self.filterLayout.addRow(labelWidget("Obtener Registros", 16,True,"white","center", "#0053a7"))
        self.filterLayout.addRow(self.btnRequery)
        self.filterLayout.addRow(labelWidget("Carrier:", self.fontSize), self.filterCarrier)
        self.filterLayout.addRow(labelWidget("Year:", self.fontSize),self.filterYear)
        self.filterLayout.addRow(labelWidget("Quarter:", self.fontSize),self.filterQuarter)
        self.filterLayout.addRow(labelWidget("Month:", self.fontSize),self.filterMonth)

        self.filterLayoutBox = qtw.QWidget()
        self.filterLayoutBox.setSizePolicy(qtw.QSizePolicy.Policy.Fixed,qtw.QSizePolicy.Policy.Fixed)
        self.filterLayoutBox.setLayout(self.filterLayout)
        
        self.filterLayoutMain = qtw.QHBoxLayout()
        # self.filterLayoutMain.setContentsMargins(0,0,0,0)
        self.filterLayoutMain.setSpacing(25)
        self.filterLayoutMain.addWidget(self.filterLayoutBox)
        # self.filterLayoutMain.addWidget(self.filterLayout2Box)
        # self.filterLayoutMain.setAlignment(self.filterLayout2Box, qtc.Qt.AlignmentFlag.AlignTop)
        self.filterLayoutMainBox = qtw.QWidget()
        self.filterLayoutMainBox.setLayout(self.filterLayoutMain)

        self.layoutmain.insertWidget(1, self.filterLayoutMainBox)

    def setTotalsElements(self):
        self.totalMiles = lineEdit(16)
        self.totalDiesel = lineEdit(16)
        self.average = lineEdit(16)
        
        self.totalsLayout = qtw.QFormLayout()
        self.totalsLayout.setContentsMargins(0,0,0,0)
        self.totalsLayout.addRow(labelWidget("TOTALES", 18,True,"white","center", "#0053a7"))
        self.totalsLayout.addRow(labelWidget("Diesel:", 16) ,self.totalDiesel)
        self.totalsLayout.addRow(labelWidget("Miles:", 16) ,self.totalMiles)
        self.totalsLayout.addRow(labelWidget("MPG:", 16) ,self.average)
        
        self.totalsLayoutBox = qtw.QWidget()
        self.totalsLayoutBox.setMinimumWidth(160)
        self.totalsLayoutBox.setLayout(self.totalsLayout)
        self.filterLayoutMain.addWidget(self.totalsLayoutBox)
        self.filterLayoutMain.setAlignment(self.totalsLayoutBox, qtc.Qt.AlignmentFlag.AlignTop)

    def calculateTotals(self):
        # get all the mies values from the table and add them
        miles = self.miles.list.getColumnValues(1)
        totalMiles = 0
        if miles:
            for i in miles:
                j = i[0]
                if j:
                    try: totalMiles += int(j)
                    except: continue
        # get all the diesel values from the corresponding table and add them
        diesel = self.diesel.list.getColumnValues(1)
        totalDiesel = 0
        if diesel:
            for i in diesel:
                j = i[0]
                if j:
                    try: totalDiesel += float(j)
                    except: return
        totalDiesel = round(totalDiesel)
        
        if totalDiesel: self.totalDiesel.setText(str(totalDiesel))
        if totalMiles: self.totalMiles.setText(str(totalMiles))
        if totalDiesel and totalMiles: self.average.setText(str(round(totalMiles/totalDiesel,2)))
    
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec()) 