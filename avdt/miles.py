#!/usr/bin/python3
from globalElements import constants, DB, modelMain, modelEmpty
from globalElements.treeview import treeviewSearchBox
from globalElements.widgets import (buttonWidget, labelWidget, tabWidget,
    lineEdit, cboFilterGroup, checkBox, truFalseRadioButtons)
import sys 
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale
locale.setlocale(locale.LC_ALL,"")
from decimal import *



class miles(modelMain.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configure_list()
        self.configure_form()
        self.setConnections()
        self.requery()
        self.createSelectionTreeView()
    
    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h2"
        self.idColumn = 'id' 
        self.tableVar = 'miles'
        self.listTableValuesIndexes = (0,1,2,3,7,4,5,6,8,9,10)
        self.formToDBItems = 4
        self.titleText = "MILES"
        self.widgetsOptSizes = [2,1]
        self.listHiddenItems = (0,3,7)
        self.listColumnWidth = ((1,60),(2,60),(4,180),(5,100),(6,120),(8,180)  )
        # self.listWidth = 2
        # self.formWidth = 1
        self.sortColumn = 4

        self.evaluateSaveIndex = (1,2)
        self.onNewFocusWidget = 1
        #number of items on formItems that will be evaluated for db saving 
        self.formToDBItems = 5
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
            SELECT
                miles.id AS "Id", 
                juris AS "Juris",
                miles AS "Miles",
                
                origin AS "IdOrigen",
                tbl_origin.location_ AS "Origin Location",
                CASE WHEN tbl_origin.isBorder = 1 THEN "True" ELSE "False" END AS "Origin Is Border",
                tbl_origin.border_ AS "Origin Border",

                destination AS "IdDestination", 
                tbl_destination.location_ AS "Destination Location",
                CASE WHEN tbl_destination.isBorder = 1 THEN "True" ELSE "False" END AS "Destination Is Border",
                tbl_destination.border_ AS "Destination Border"

            FROM miles
            -- Join Statements 
            LEFT JOIN miles_locations tbl_origin ON  tbl_origin.id = miles.origin
            LEFT JOIN miles_locations tbl_destination ON  tbl_destination.id = miles.destination
            ;'''
        self.newRecordSql = '''
            INSERT INTO miles (juris, miles, origin, destination) VALUES'''
        
    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                juris = '{record[1]}',
                miles = '{record[2]}',
                origin = '{record[3]}',
                destination = '{record[4]}'
                WHERE {self.idColumn} = {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        #1. Get all records
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()# will pass the cbo value - should be 
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        self.jurisFilterAfterUpdate()
        self.configureColumns()
        # else:
        #     self.list.removeAllRows()
        # self.configureColumns()

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            juris =self.juris.getInfo()
            origin = self.originLocation.getInfo()
            destination = self.destinationLocation.getInfo()
            text = f'''Eliminar el registro:
            id: {idVar}
            Juris: {juris}
            Origin: {origin}
            Destination: {destination}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        pass
    
#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self): 
        #p!Confirgure files tree
        #o! CHANGE CONFIGURATION FOR ADDING AND NORMAL DIESEL VIEW
        self.formLayoutStraight()
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        self.juris = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.iftaJuris,
            requeryFunc=constants.queryIftaJuris,
            clearFilter=False
        )
        self.miles = lineEdit(self.fontSize)
        self.originId = lineEdit(self.fontSize)
        self.destinationId = lineEdit(self.fontSize)

        #y! ORIGIN
        self.originLocation = lineEdit(self.fontSize)
        self.originLocation.setEnabled(False)
        self.originIsBorder = checkBox()
        self.originIsBorder.setEnabled(False)
        self.originBorder = lineEdit(self.fontSize)
        self.originBorder.setEnabled(False)
        #y! DESTINATION
        self.destinationLocation = lineEdit(self.fontSize)
        self.destinationLocation.setEnabled(False)
        self.destinationIsBorder = checkBox()
        self.destinationIsBorder.setEnabled(False)
        self.destinationBorder = lineEdit(self.fontSize)
        self.destinationBorder.setEnabled(False)


        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [
            self.id_, 
            self.juris, 
            self.miles,
            
            self.originId,
            self.destinationId,

            self.originLocation,
            self.originIsBorder,
            self.originBorder,

            
            self.destinationLocation,
            self.destinationIsBorder,
            self.destinationBorder]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Jurisdiction:', self.fontSize), self.juris)
        self.layoutForm.addRow(labelWidget('Miles:', self.fontSize), self.miles)
        
        self.layoutForm.addRow(labelWidget("Origin", 14, fontBolt=True, align="center"))
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.originId)
        self.layoutForm.addRow(labelWidget('Location:', self.fontSize), self.originLocation)
        self.layoutForm.addRow(labelWidget('Is Border:', self.fontSize), self.originIsBorder)
        self.layoutForm.addRow(labelWidget('Border:', self.fontSize), self.originBorder)

        self.layoutForm.addRow(labelWidget("Destination", 14, fontBolt=True, align="center"))
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.destinationId)
        self.layoutForm.addRow(labelWidget('Location:', self.fontSize), self.destinationLocation)
        self.layoutForm.addRow(labelWidget('Is Border:', self.fontSize), self.destinationIsBorder)
        self.layoutForm.addRow(labelWidget('Border:', self.fontSize), self.destinationBorder)
        
    def configure_list(self):
        #g! FILTER ITEMS
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        self.jurisFilter = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.iftaJuris,
            requeryFunc=constants.queryIftaJuris,
            clearFilter=True
        )
        self.filterOriginBorder = truFalseRadioButtons(self.filterSize, filter=True)
        self.filterDestinationBorder = truFalseRadioButtons(self.filterSize, filter=True)
        # self.isBorderFilter = truFalseRadioButtons(self.filterSize, filter=True)
        self.list.layoutFilter.insertRow(0, labelWidget('Jurisdistion:', self.filterSize), self.jurisFilter)
        self.list.layoutFilter.insertRow(0, labelWidget('Destination Border:', self.filterSize), self.filterDestinationBorder)
        self.list.layoutFilter.insertRow(0, labelWidget('Origin Border:', self.filterSize), self.filterOriginBorder)
        
        #g!proxy models
        self.proxyJuris = qtc.QSortFilterProxyModel()
        self.proxyOriginBorder = qtc.QSortFilterProxyModel()
        self.proxyDestinationBorder = qtc.QSortFilterProxyModel()

    def setConnections(self):
        self.jurisFilter.cbo.currentIndexChanged.connect(self.jurisFilterAfterUpdate)
        self.filterOriginBorder.true.toggled.connect(self.originIsBorderFilterAfterUpdate)
        self.filterOriginBorder.false.toggled.connect(self.originIsBorderFilterAfterUpdate)
        self.filterDestinationBorder.true.toggled.connect(self.destinationIsBorderFilterAfterUpdate)
        self.filterDestinationBorder.false.toggled.connect(self.destinationIsBorderFilterAfterUpdate)

        # self.isBorderFilter.false.toggled.connect(self.jurisFilterAfterUpdate)

        #g! FORM Connections
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.juris.cbo.currentTextChanged.connect(lambda: self.formDirty(1,self.juris.getInfo()))
        self.miles.textChanged.connect(lambda: self.formDirty(2, self.miles.getInfo))
        self.originId.textChanged.connect(lambda: self.formDirty(3, self.originId.getInfo))
        self.destinationId.textChanged.connect(lambda: self.formDirty(4, self.destinationId.getInfo))

    def removeAllFilters(self):
        self.jurisFilter.reSet()
        self.list.filtros.txt.reSet()

    def jurisFilterAfterUpdate(self):
        filterText = self.jurisFilter.getInfo()
        self.proxyJuris.setSourceModel(self.list.standardModel)
        self.proxyJuris.setFilterFixedString(filterText)
        self.proxyJuris.setFilterKeyColumn(1)

        self.originIsBorderFilterAfterUpdate()

    def originIsBorderFilterAfterUpdate(self):
        filterText = self.filterOriginBorder.getInfo()
        self.proxyOriginBorder.setSourceModel(self.proxyJuris)
        self.proxyOriginBorder.setFilterFixedString(filterText)
        self.proxyOriginBorder.setFilterKeyColumn(5)
        self.destinationIsBorderFilterAfterUpdate()

    def destinationIsBorderFilterAfterUpdate(self):
        filterText = self.filterDestinationBorder.getInfo()
        self.proxyDestinationBorder.setSourceModel(self.proxyOriginBorder)
        self.proxyDestinationBorder.setFilterFixedString(filterText)
        self.proxyDestinationBorder.setFilterKeyColumn(9)

        self.list.proxyModel.setSourceModel(self.proxyDestinationBorder)
        self.list.proxyModel.sort(8)
        self.list.search_afterUpdate(self.sortColumn, self.sortOrder)

    def getListInfo(self):
        i0 = self.id_.getInfo()
        i1 = self.juris.getInfo()
        i2 = self.miles.getInfo()
        i3 = self.originId.getInfo()
        i4 = self.originLocation.getInfo()
        i5 = self.originIsBorder.getInfo()
        i6 = self.originBorder.getInfo()
        i7 = self.destinationId.getInfo()
        i8 = self.destinationLocation.getInfo()
        i9 = self.destinationIsBorder.getInfo()
        i10 = self.destinationBorder.getInfo()

        record = ([i0, i1,i2,i3, i4, i5, i6, i7, i8, i9, i10])
        return record

    def createSelectionTreeView(self):
        #create Treeview for items selection
        self.addTree = treeviewSearchBox(11,1)
        
        
        self.requeryAddTree()

        self.btnAddOrigin = buttonWidget("   Add to Origin", "h2_", constants.iconAdd)
        self.btnAddDestination = buttonWidget("   Add to Destination", "h2_", constants.iconAdd)

        self.selectionTreeLayout = qtw.QGridLayout()
        self.selectionTreeLayout.addWidget(self.btnAddOrigin,0,0)
        self.selectionTreeLayout.addWidget(self.btnAddDestination,0,1)
        self.selectionTreeLayout.addWidget(self.addTree,1,0,1,2)
        self.selectionTreeLayoutBox = qtw.QWidget()
        self.selectionTreeLayoutBox.setLayout(self.selectionTreeLayout)

        self.layoutForm.addRow(labelWidget("LOCATIONS", 18, fontColor="Blue", align="center"))
        self.layoutForm.addRow(self.selectionTreeLayoutBox)
        
        #Connections
        self.addTree.actRefresh.triggered.connect(self.requeryAddTree)
        self.btnAddOrigin.pressed.connect(self.btnAddOriginPressed)
        self.btnAddDestination.pressed.connect(self.btnAddDestinationPressed)
        
    def btnAddOriginPressed(self):
        values = self.addTree.getCurrentValues()
        self.originId.setText(values[0])
        self.originLocation.populate(values[1])
        self.originIsBorder.populate(values[2])
        self.originBorder.populate(values[3])

    def btnAddDestinationPressed(self):
        values = self.addTree.getCurrentValues()
        self.destinationId.setText(values[0])
        self.destinationLocation.populate(values[1])
        self.destinationIsBorder.populate(values[2])
        self.destinationBorder.populate(values[3])


    def requeryAddTree(self):
        #get the sql from the selectAll miles/locations table
        # filePath = "oth/sql/miles_locations/selectAll.sql"
        # sqlFile = open(filePath, "r")
        # sqlFileText = sqlFile.read()
        # sqlFile.close()
        sql =''' SELECT 
            id AS "Id",
            location_ AS "Location",
            CASE WHEN isBorder = 1 THEN "True" ELSE "False" END AS "Is Border", 
            border_ AS "Border"
        FROM miles_locations;
        '''
        #run Query
        records = self.db.get_records_clearNull (sql)
        horizontalLabels = self.db.cursor.column_names
        #add items to tree
        self.addTree.requery(records,11,30)
        #set the labels to the tree
        self.addTree.standardModel.setHorizontalHeaderLabels(horizontalLabels) 
            

class locations(modelMain.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configure_list()
        self.configure_form()
        self.setConnections()
        self.requery()

    def setGlobalVariables(self):
        self.size_ = "h2"
        self.idColumn = 'id' 
        self.tableVar = 'miles_locations'
        # self.sqlFolderName = "miles_locations"
        self.listTableValuesIndexes = (0,1,2,3)
        self.formToDBItems = 4
        self.titleText = "LOCATIONS"
        self.widgetsOptSizes = [2,1]
        self.listHiddenItems = ()
        self.listColumnWidth = ((1,250),(2,100), )

        self.evaluateSaveIndex = (1,)
        self.onNewFocusWidget = 2
        #number of items on formItems that will be evaluated for db saving 
        # self.formToDBItems = 0
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = f'''
            SELECT 
                id AS "Id",
                location_ AS "Location",
                CASE WHEN isBorder = 1 THEN "True" ELSE "False" END AS "Is Border", 
                border_ AS "Border"
            FROM {self.tableVar};'''
        self.newRecordSql = f'''
            INSERT INTO {self.tableVar} (location_, isBorder, border_) VALUES'''
        
    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                location_ = '{record[1]}',
                isBorder = '{record[2]}',
                border_ = '{record[3]}'
                WHERE {self.idColumn} = {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        #1. Get all records
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()# will pass the cbo value - should be 
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        self.isBorderFilterAfterUpdate()
        self.configureColumns()

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            Location =self.localtion.text()
            text = f'''Eliminar el registro:
            id: {idVar}
            Location: {Location}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        pass
    
#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self): 
        #p!Confirgure files tree
        #o! CHANGE CONFIGURATION FOR ADDING AND NORMAL DIESEL VIEW
        self.formLayoutStraight()
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.localtion = lineEdit(self.fontSize)
        self.isBorder = checkBox("True")
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        self.border = cboFilterGroup(
            self.fontSize, 
            refreshable=True, 
            items= constants.iftaJuris,
            requeryFunc=constants.queryIftaJuris,
            clearFilter=False
        )
        #o! VERIFY - SET ITEMS TO FILL DB 
        self.formItems = [
            self.id_, 
            self.localtion, 
            self.isBorder,
            self.border]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Location:', self.fontSize), self.localtion)
        self.layoutForm.addRow(labelWidget('Is Border:', self.fontSize), self.isBorder)
        self.layoutForm.addRow(labelWidget('Border:', self.fontSize), self.border)
        
    def configure_list(self):
        #g! FILTER ITEMS
        self.isBorderFilter = truFalseRadioButtons(self.filterSize, filter=True)
        self.list.layoutFilter.insertRow(0, labelWidget('Is Border:', self.filterSize), self.isBorderFilter)
        
        #g!proxy models
        self.proxyIsBorder = qtc.QSortFilterProxyModel()

    def setConnections(self):
        self.isBorderFilter.true.toggled.connect(self.isBorderFilterAfterUpdate)
        self.isBorderFilter.false.toggled.connect(self.isBorderFilterAfterUpdate)

        #g! FORM Connections
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.localtion.textChanged.connect(lambda: self.formDirty(1,self.localtion.getInfo()))
        self.isBorder.stateChanged.connect(lambda: self.formDirty(2, self.isBorder.getInfo))
        self.border.cbo.currentTextChanged.connect(lambda: self.formDirty(3, self.border.getInfo))
        
    
    def removeAllFilters(self):
        self.isBorderFilter.reSet()
        self.list.filtros.txt.reSet()

    def isBorderFilterAfterUpdate(self):
        filterText = self.isBorderFilter.getInfo()
        self.proxyIsBorder.setSourceModel(self.list.standardModel)
        self.proxyIsBorder.setFilterFixedString(filterText)
        self.proxyIsBorder.setFilterKeyColumn(2)

        self.list.proxyModel.setSourceModel(self.proxyIsBorder)
        self.list.search_afterUpdate(self.sortColumn, self.sortOrder)

    def getListInfo(self):
        i0 = self.id_.getInfo()
        i1 = self.localtion.getInfo()
        i2 = self.isBorder.getInfo()
        i3 = self.border.getInfo()
        record = ([i0, i1,i2,i3])
        return record

class main(modelEmpty.main):
    def __init__(self):
        super().__init__()

        self.configureTabsWidget()
        self.milesOpen()
    
    def setGlobalVariables(self):
        self.titleText = "MAIN MILES - LOCATIONS"
        self.size_ = 'h1'

    def configureTabsWidget(self):
        self.mainTabWidget = tabWidget('h2')
        self.layoutmain.addWidget(self.mainTabWidget,1)
        self.configToolbar()
    
    def configToolbar(self):
        iconRoot = f'{constants.rootDb}\oth\icons'
        self.iconRoad = qtg.QIcon(f'{iconRoot}\\road.png')
        self.iconLocation = qtg.QIcon(f'{iconRoot}\\placeholder.png')

        self.btnMiles = buttonWidget('Miles', self.mainSize, self.iconRoad)
        self.btnMiles.pressed.connect(self.milesOpen)
        self.titleLayout.insertWidget(0, self.btnMiles)

        self.btnLocation = buttonWidget('Locations', self.mainSize, self.iconLocation)
        self.btnLocation.pressed.connect(self.locationsOpen)
        self.titleLayout.insertWidget(0, self.btnLocation)

    def milesOpen(self):
        self.miles = miles()#list, rowHeight, fontSize
        self.mainTabWidget.addTab(self.miles, '   MILES   ')
        self.mainTabWidget.setCurrentWidget(self.miles)

    def locationsOpen(self):
        self.locations = locations()#list, rowHeight, fontSize
        self.mainTabWidget.addTab(self.locations, '   LOCATIONS   ')
        self.mainTabWidget.setCurrentWidget(self.locations)
        



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = miles()
    mw.show()
    sys.exit(app.exec())