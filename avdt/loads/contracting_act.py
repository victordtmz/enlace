#!/usr/bin/python3
from globalElements import constants, functions, DB, modelList, modelMain
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 
locale.setlocale(locale.LC_ALL,"")
from decimal import *
from globalElements.widgets import (buttonWidget, labelWidget, webWidget,  
    textEdit, lineEdit, truFalseRadioButtons,spinbox,dateTimeEdit, 
    checkBox, spacer, cboFilterGroup, deleteWarningBox, dateEdit)

class addForm(modelList.main): 
    def __init__(self):
        super().__init__()
        # self.btn_cerrar.deleteLater()
        
        self.configureButtons()
        self.configureFilters()
        self.setConnectionsLocal()
        
        self.requery() 
        iconSize = qtc.QSize(40,18)
        self.list.toolBar.setIconSize(iconSize)
        self.list.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.list.toolBar)


    def setGlobalVariables(self):
        self.idLoad = 0
        # self.idCarrier = 0
        # self.sqlFolderName = "AVDT_warehouses"
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
            ;
        '''
        self.size_ = "h2"
        self.titleText = "" 

        # LIST INFO"Fecha", 
        # self.horizonatalLabels = ["Id","Fecha", "Monto","Galones","Juris", "Descripcion", "Anexo"]
        # self.listTableValuesIndexes = []
        self.sortColumn = 4
        # self.rowHeight = 50
        # self.listFontSize = 11
        self.sortOrder = qtc.Qt.SortOrder.AscendingOrder
        self.listHiddenItems = (0,3,5,7,9)
        self.listColumnWidth = ((1,50),(2,65),(4,110),(6,110),(8,110),(10,110) )
        self.filterSize = 11

        self.listExpand = 4
        # self.list.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.list.toolBar)
    
    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        #1. Get all records
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()# will pass the cbo value - should be 
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
            # jurisFilterAfterUpdate
        self.jurisFilterAfterUpdate()
        self.configureColumns()  

    def configureButtons(self):
        self.btnAdd = buttonWidget(text="Agregar a este viaje", 
            icon=constants.iconAdd, size=self.mainSize)
        
        self.titleLayout.setStretch(0,1)
        self.titleLayout.insertWidget(1, self.btnAdd)

    def configureFilters(self):
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
        

    def setConnectionsLocal(self):
        self.btnAdd.pressed.connect(self.btnAddPressed)
        self.jurisFilter.cbo.currentIndexChanged.connect(self.jurisFilterAfterUpdate)
        self.filterOriginBorder.true.toggled.connect(self.originIsBorderFilterAfterUpdate)
        self.filterOriginBorder.false.toggled.connect(self.originIsBorderFilterAfterUpdate)
        self.filterDestinationBorder.true.toggled.connect(self.destinationIsBorderFilterAfterUpdate)
        self.filterDestinationBorder.false.toggled.connect(self.destinationIsBorderFilterAfterUpdate)

    def btnAddPressed(self):
        # idLoad = self.parent().parent().parent().parent().parent().parent().parent().parent().idLoad
        if self.idLoad:
            if self.list.treeview.selectionModel().hasSelection():
                indexes = self.list.treeview.selectionModel().selectedIndexes()
                idVar = indexes[0].data()
                #get the max value for this load and add 1
                sql = f'''SELECT 
                            MAX(no_) + 1
                            FROM loads_miles
                            WHERE id = {self.idLoad}
                        ;'''
                number = self.db.get_records(sql)[0][0]
                # number = number
                if not number:
                    number=1
                # get the date of the load to start with it
                sql = f'''SELECT 
                            contract_date
                            FROM loads
                            WHERE id = {self.idLoad}
                        ;'''
                date = self.db.get_records(sql)[0][0]
                # date = date
                if idVar:
                    sql = '''INSERT IGNORE INTO AVDT_Loads_Miles (idLoad, idMiles, no_, date_) VALUES '''
                    #insert the new record - notice quotations on date to enter as string
                    sql = f'{sql} ( {self.idLoad},{idVar},{number}, "{date}");'
                    # print(sql)
                    self.db.insertNewRecord(sql)

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


class main(modelMain.main):
    def __init__(self):
        super().__init__()
        
        
        #o! CONFIGURE IN FILTERS OR DELETE
        # if not constants.iftaJuris:
        #     constants.queryIftaJuris()
        # set addForm to False - this will be the widget to add records to the current load
        self.addForm = False
        self.initUi()
        self.addFormOpt = checkBox('Agregar Elementos',fontSize=self.fontSize, size=self.mainSize)
        self.widgetsOpt.append(self.addFormOpt)
        # self.titleLayout.addWidget(self.addFormOpt)

        
        self.widgetsOptSizes.append(1)#size proportion
        self.spacer3 = spacer('     ', self.formSize)
        self.titleLayout.insertWidget(3, self.spacer3)
        self.titleLayout.insertWidget(4, self.addFormOpt)
        
        

        self.btnNew.deleteLater()
        # self.configure_list()
        self.configure_form()
        self.configure_list()
        self.setConnections()
        # self.setHLayoutVariables()
        self.requery()
        
    #     # self.getIdLoad()
    # def setHLayoutVariables(self):
    #     self.rowHeight = 80

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h2"
        self.idLoad = 0
        self.idColumn = 'id' 
        self.tableVar = 'loads_miles'
        # self.sqlFolderName = "AVDT_loads_stops"
        self.listTableValuesIndexes = (0,1,2,3,4,5,6,7,8,9,10,11,12,13)
        self.widgetsOptSizes = [1,1]#list, form > relative valies
        self.formToDBItems = 5
        self.titleText = "LOAD MILES"
        # self.listExpand = 1
        # self.formExpand = 1
        # self.addFormExpand = 1
        self.widgetsOptSizes = [1,1]

        self.listHiddenItems = (0,1,6,8,10,12)
        self.listColumnWidth = ((2,40),(3,90),(4,50),(5,70),(7,110),(9,120),(11,110))
        self.sortColumn = 3
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.newRecordSql = '''
            INSERT INTO miles (idLoad, idMiles, no_, date_) VALUES  '''
        self.selectSql = '''
            SELECT
                loads_miles.id,
                idLoad,
                idMiles,
                no_ as "No.",
                date_ as "Date:",
                miles.juris as "Juris", 
                miles.miles as "Miles",
                origin.id AS "OriginId",
                origin.location_ AS "Origin",
                CASE WHEN origin.isBorder = 1 THEN "True" ELSE "False" END AS "O-Is Border", 
                origin.border_ AS "O-Border",
                destination.id AS "DestinationId",
                destination.location_ AS "Destination",
                CASE WHEN destination.isBorder = 1 THEN "True" ELSE "False" END AS "D-Is Border", 
                destination.border_ AS "D-Border"
                
                FROM loads_miles 
                -- LEFT JOIN AVDT_Loads load_ ON load_.IdLoad = idLoad 
                LEFT JOIN miles ON miles.id = loads_miles.idMiles
                LEFT JOIN miles_locations origin ON origin.id = miles.origin
                LEFT JOIN miles_locations destination ON destination.id = miles.destination

            WHERE idLoad LIKE %s;'''

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idLoad  = '{record[1]}',
                idMiles  = '{record[2]}',
                no_ = '{record[3]}',
                date_ = '{record[4]}'
                WHERE id = {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        if self.idLoad:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((self.idLoad,))# will pass the cbo value - should be 
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            # self.list.search_afterUpdate()
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
        else:
            self.list.removeAllRows()
        
        self.configureColumns()

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        if self.idLoad:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((self.idLoad,))# will pass the cbo value - should be 
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.jurisFilterAfterUpdate()
            while qtw.QApplication.overrideCursor() is not None:
                qtw.QApplication.restoreOverrideCursor()
        else:
            self.list.removeAllRows()
        
        self.configureColumns()

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            no_ = self.no_.getInfo()
            date = self.date_.getInfo()
            juris = self.juris.text()
            miles = self.miles.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no_}
            Date: {date}
            Juris: {juris}
            Miles: {miles}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        

    # def deleteRecord(self, text = ''): 
    #     if self.list.treeview.selectionModel().hasSelection():
    #         idVar = self.list.treeview.selectionModel().selectedIndexes()[0].data()
    #         warning_box = deleteWarningBox(text)
    #         button = warning_box.exec()

    #         if button == qtw.QMessageBox.StandardButton.Yes:
    #             self.save_record_main(True,False)
    #             # values_ = (IdVar,)
    #             idMiles = self.idLoad_.getInfo()
    #             sql = f"""
    #                 DELETE FROM {self.tableVar} WHERE idLoad = {self.idColumn} AND idMiles = {idMiles}
    #             """
    #             self.db.run_sql_commit(sql)
    #             #find row of standard model to delete regarldess of filter
    #             #clear list values to avoid saving after deletion because selection will change
    #             self.listTableValues.clear()
    #             #find row of standard model to delete regarldess of filter
    #             rowVar = self.list.findItem(0,idVar)
    #             if rowVar:
    #                 self.list.standardModel.removeRow(rowVar)
        

#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(400)
        self.layoutFormBox.setMaximumWidth(450)
        self.setFormElements()
        # self.btnAdd = buttonWidget("   Agregar elementos", "h2", constants.iconAdd)
        # self.titleLayout.insertWidget(2, self.btnAdd)

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        self.idLoad_ = lineEdit(self.fontSize)
        self.idLoad_.setReadOnly(True)
 
        self.no_ = spinbox(self.fontSize)
        self.no_.setMinimum(1)
        # self.no_.setSingleStep()

        self.date_ = dateEdit(self.fontSize)

        self.juris = lineEdit(self.fontSize)
        self.juris.setEnabled(False)
        self.miles = lineEdit(self.fontSize)
        self.miles.setEnabled(False)
        self.originId = lineEdit(self.fontSize)
        self.originId.setEnabled(False)
        self.destinationId = lineEdit(self.fontSize)
        self.destinationId.setEnabled(False)

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
            self.idLoad_,
            
            self.no_,
            self.date_,

            self.juris, 
            self.miles,
            
            self.originId,
            self.originLocation,
            self.originIsBorder,
            self.originBorder,

            self.destinationId,
            self.destinationLocation,
            self.destinationIsBorder,
            self.destinationBorder]
        
        self.layoutForm.addRow(labelWidget('IdMiles:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdLoad:', self.fontSize), self.idLoad_)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.no_)
        self.layoutForm.addRow(labelWidget('Date:', self.fontSize), self.date_)
        self.layoutForm.addRow(labelWidget('Jurisdiction:', self.fontSize), self.juris)
        self.layoutForm.addRow(labelWidget('Miles:', self.fontSize), self.miles)
        
        self.layoutForm.addRow(labelWidget("Origin", 16, fontColor="Blue", align="center"))
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.originId)
        self.layoutForm.addRow(labelWidget('Location:', self.fontSize), self.originLocation)
        self.layoutForm.addRow(labelWidget('Is Border:', self.fontSize), self.originIsBorder)
        self.layoutForm.addRow(labelWidget('Border:', self.fontSize), self.originBorder)

        self.layoutForm.addRow(labelWidget("Destination", 16, fontColor="Blue", align="center"))
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
        # self.isBorderFilter = truFalseRadioButtons(self.filterSize, filter=True)
        self.list.layoutFilter.insertRow(0, labelWidget('Jurisdistion:', self.filterSize), self.jurisFilter)
        
        #g!proxy models
        self.proxyIsBorder = qtc.QSortFilterProxyModel()

        # self.btnAdd = buttonWidget("   Agregar elementos", "h2", constants.iconAdd)
        # self.listBtnsLayout = qtw.QVBoxLayout()
        # self.listBtnsLayout.setContentsMargins(5,0,0,0)
        # self.listBtnsLayout.addWidget(self.btnAdd)
        # self.listBtnsLayoutBox = qtw.QWidget()
        # self.listBtnsLayoutBox.setLayout(self.listBtnsLayout)
        # self.list.allFiltersLayout.addWidget(self.listBtnsLayoutBox,1,1)



    def setConnections(self):
        self.jurisFilter.cbo.currentIndexChanged.connect(self.jurisFilterAfterUpdate)
        # self.btnAdd.pressed.connect(self.displayAddForm)
        self.addFormOpt.toggled.connect(self.displayAddForm)
        # self.isBorderFilter.false.toggled.connect(self.jurisFilterAfterUpdate)

        #g! FORM Connections
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.no_.textChanged.connect(lambda: self.formDirty(2, self.miles.getInfo))
        self.date_.dateChanged.connect(lambda: self.formDirty(3, self.date_.getInfo))

        self.list.proxyModel.dataChanged.connect(self.calculateTotals)
        self.list.proxyModel.rowsInserted.connect(self.addToTotals)
        self.list.proxyModel.rowsRemoved.connect(self.calculateTotals) 

    def removeAllFilters(self):
        self.jurisFilter.reSet()
        self.list.filtros.txt.reSet()

    def jurisFilterAfterUpdate(self):
        filterText = self.jurisFilter.getInfo()
        self.proxyIsBorder.setSourceModel(self.list.standardModel)
        self.proxyIsBorder.setFilterFixedString(filterText)
        self.proxyIsBorder.setFilterKeyColumn(4)

        self.list.proxyModel.setSourceModel(self.proxyIsBorder)
        self.list.proxyModel.sort(2)
        self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
        
    def displayAddForm(self):
        if not self.addForm:
            #Create instance of add form
            self.addForm = addForm()
            # set the id values esential for requery
            self.addForm.idLoad = self.idLoad
            # set all form elements for this load
            self.addForm.requery()
            #place on splitter
            self.splitter.addWidget(self.addForm)
            #set connections to this item
            self.addForm.btnAdd.pressed.connect(self.addMilesLoad)
            self.configureWidth()
        else:
            self.addForm.deleteLater()
            self.addForm = False


            # self.addForm.btn_cerrar.pressed.connect(self.closeAddForm)
            #set the widget sizes for the splitter
            # totalWidgets = self.splitter.count()
            # pass_ = 0
            # while pass_ < totalWidgets:
            #     print(self.splitter.widget(pass_))
            #     pass_+=1
            

    # def closeAddForm(self):
    #     """To avoid error when trying to requery form main loads form, set to false - from close code is set in class"""
        

    def addMilesLoad(self):
        self.requery()

    def setTotalsElements(self):
        self.totals = labelWidget("0", 13, True)
        # self.totals.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
        self.totalsLabel = labelWidget("Total miles:",13,True)
        self.totalsLayout = qtw.QHBoxLayout()
        self.totalsLayout.addWidget(self.totalsLabel)
        self.totalsLayout.addWidget(self.totals,1)
        self.totalsLayoutBox = qtw.QWidget()
        self.totalsLayoutBox.setLayout(self.totalsLayout)
        self.listBtnsLayout.addWidget(self.totalsLayoutBox)

    def calculateTotals(self):
        miles = self.list.getColumnValues(5)
        total = 0
        if miles:
            for i in miles:
                total += int(i[0])
        self.totals.setText(str(total))
    
    def addToTotals(self):
        #get the value from the last row - shoud be the last row
        row = self.list.standardModel.rowCount() -1
        value = int(self.list.standardModel.index(row,5).data())
        # get the current total
        curTotal = self.totals.text()
        try:
            curTotal = int(curTotal)
        except:
            curTotal = curTotal.replace(",", "")
            curTotal = int(curTotal)
        
        if curTotal:
            total = value + curTotal
        elif value:
            total = value
        else:
            total = 0 
        total = "{:,}".format(total)
        self.totals.setText(total)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec()) 