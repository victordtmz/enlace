#!/usr/bin/python3
from globalElements import constants, functions, mainModel, DB, listModel
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 
locale.setlocale(locale.LC_ALL,"")
from decimal import *
from globalElements.widgets import buttonWidget, labelWidget, webWidget,  textEdit, lineEdit, truFalseRadioButtons,spinbox,dateTimeEdit

class warehouses(listModel.main):
    def __init__(self):
        super().__init__()
        # self.btn_cerrar.deleteLater()
        
        self.configureButtons()
        # self.setConnectionsLocal()
        
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
                id AS "ID", 
                name_ AS "Name",
                north AS "North",
                west AS "West",
                address_ AS "Address",
                city AS "City",
                state_ AS "State", 
                zip AS "Zip",
                phone AS "Phone",
                google AS "Google Maps",
                notes AS "Notes"
            FROM stops;
        '''
        self.size_ = "h2"
        self.titleText = ""

        self.sortOrder = qtc.Qt.SortOrder.AscendingOrder
        self.listHiddenItems = (0,2,3,4,8,9,10)
        self.listColumnWidth = ((1,220),(5,110),(6,60),(7,80) )
        self.filterSize = 11

        self.listWidth = 4
        # self.list.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.list.toolBar)
    
    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        #1. Get all records
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()# will pass the cbo value - should be 
        self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        # self.jurisFilterAfterUpdate()
        self.configureColumns()  

    def configureButtons(self):
        self.btnAdd = buttonWidget(text="   Agregar nueva parada", 
            icon=constants.iconAdd, size=self.mainSize)
        self.btnEditStop = buttonWidget(text="   Agregar a registro seleccionado", 
            icon=constants.iconAdd, size=self.mainSize)
        # self.titleLayout.insertWidget(0, self.spacerLeft,1)
        self.titleLayout.setStretch(0,1)
        self.titleLayout.insertWidget(1, self.btnAdd)
        self.titleLayout.insertWidget(2, self.spacer2,1)
        self.titleLayout.insertWidget(3, self.btnEditStop)
        
        # self.btnClose = buttonWidget("   Cerrar", "warning", constants.iconClose)
        # self.btnLayout = qtw.QVBoxLayout()
        # self.btnLayout.setContentsMargins(0,0,0,0)
        # self.btnLayout.addWidget(self.btnAdd)
        # self.btnLayout.addWidget(self.btnEditStop)
        # self.btnLayoutBox = qtw.QWidget()
        # self.btnLayoutBox.setLayout(self.btnLayout)
        # self.layout_buttons.insertWidget(0, self.btnLayoutBox)
        

    def btn_cerrar_pressed(self):
        self.deleteLater()


class screenshot(qtw.QWidget):
    def __init__(self):
        super().__init__()
        fontSize = 14
        self.layoutForm = qtw.QFormLayout()
        self.layoutForm.setContentsMargins(20,20,20,20)
        self.carrier = labelWidget("",18, True,"white", "center",backColor="#002142")
        self.loadNo = labelWidget("", fontSize)
        self.no_ = labelWidget("", fontSize)
        self.type = labelWidget("", fontSize)
        self.appointment = labelWidget("", fontSize)
        self.po = labelWidget("", fontSize, backColor="#D2EBD8")
        self.notes = labelWidget("", fontSize)
        self.bodega = labelWidget("", fontSize)
        self.north = labelWidget("", fontSize)
        self.west = labelWidget("", fontSize)
        self.bodegaNotes = labelWidget('', fontSize)

        self.layoutForm.addRow(self.carrier)
        self.layoutForm.addRow(labelWidget('Load No:', fontSize,True), self.loadNo)
        self.layoutForm.addRow(labelWidget('No.:', fontSize,True), self.no_)
        self.layoutForm.addRow(labelWidget('Type:', fontSize,True), self.type)
        self.layoutForm.addRow(labelWidget('Appointment:', fontSize,True), self.appointment)
        self.layoutForm.addRow(labelWidget('PO:', fontSize,True), self.po)
        self.layoutForm.addRow(self.notes)
        self.layoutForm.addRow(labelWidget("Warehouse Information:", 16, True, "#0053a7", "center"))
        self.layoutForm.addRow(self.bodega)
        self.layoutForm.addRow(labelWidget("Coordinates:", 14, True, "black", "center"))
        self.layoutForm.addRow(labelWidget('North:', fontSize), self.north)
        self.layoutForm.addRow(labelWidget('West:', fontSize), self.west)
        self.layoutForm.addRow(self.bodegaNotes)
        self.setLayout(self.layoutForm)
        
        pal = qtg.QPalette()
        pal.setColor(qtg.QPalette.ColorRole.Window, qtc.Qt.GlobalColor.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class main(mainModel.main):
    def __init__(self):
        super().__init__()
        
        if not constants.iftaJuris:
            constants.queryIftaJuris()
        # set addForm to False - this will be the widget to add records to the current load
        self.addForm = False
        self.initUi()
        
        

        self.btnNew.deleteLater()
        # self.configure_list()
        self.configure_form()
        self.setConnections()
        self.setHLayoutVariables()
        self.requery()
        
        # self.getIdLoad()
    def setHLayoutVariables(self):
        self.rowHeight = 80

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h2"
        self.idLoad = 0
        self.idColumn = 'id' 
        self.tableVar = 'loads_stops'
        # self.sqlFolderName = "AVDT_loads_stops"
        self.listTableValuesIndexes = (0,1,2,4,3,5,6,7,8,9,10,11,12)
        self.formToDBItems = 8
        self.titleText = "LOAD STOPS"
        self.listWidth = 1
        self.formWidth = 1
        self.listHiddenItems = (0,1,2,6,7,9,10,11,12)
        self.listColumnWidth = ((3,40),(4,70),(5,120),(5,120),(7,110))
        self.sortColumn = 3
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.newRecordSql = '''
                INSERT INTO loads_stops (
                    idLoad,
                    idStop,
                    type_,
                    no_,
                    appointment,
                    po,
                    notes
                )
                VALUES  
        '''
        self.selectSql = '''
            SELECT 
                loads_stops.id AS "ID", 
                loads_stops.idLoad,
                loads_stops.idStop,
                loads_stops.no_ AS "No.", 
                CASE WHEN loads_stops.type_ = 1 THEN "Pickup" ELSE "Delivery" END AS "Type",
                
                DATE_FORMAT(loads_stops.appointment, "%Y-%m-%d %H:%i") AS "Appointment",
                loads_stops.po AS "PO",
                loads_stops.notes AS "Notes",
                CONCAT(stops.name_, "\n", 
                    stops.address_, "\n", 
                    stops.city, " ",stops.state_, " ", stops.zip, "\n", 
                    stops.phone) AS "Warehouse",
                stops.north AS "North",
                stops.west AS "West",
                stops.google AS "Google",
                stops.notes AS "Notes"
                FROM loads_stops 
                LEFT JOIN stops  ON stops.id = loads_stops.idStop
                WHERE idLoad = %s
            ;'''

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idLoad = '{record[1]}',
                idStop = '{record[2]}',
                type_ = '{record[3]}',
                no_ = '{record[4]}',
                appointment = '{record[5]}',
                po = '{record[6]}',
                notes = '{record[7]}'
                WHERE {self.idColumn} = {record[0]};'''
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

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            no_ = self.no_.getInfo()
            appointment = self.appointment.getInfo()
            type = self.type.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no_}
            Appointment: {appointment}
            Type: {type}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        

#G! INIT MAIN FORM --------------------------------------------------------------
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(400)
        self.layoutFormBox.setMaximumWidth(450)
        self.setFormElements()
        self.btnAdd = buttonWidget("   Agregar elementos", "h2", constants.iconAdd)
        self.titleLayout.insertWidget(2, self.btnAdd)

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.idLoad_ = lineEdit(self.fontSize)
        self.idLoad_.setReadOnly(True)
        self.idWarehouse = lineEdit(self.fontSize)
        self.idWarehouse.setReadOnly(True)
        self.type = truFalseRadioButtons(self.fontSize)
        self.type.true.setText("Pickup")
        self.type.false.setText("Delivery")
        self.no_ = spinbox(self.fontSize)
        self.no_.setMinimum(0)
        self.appointment = dateTimeEdit(self.fontSize)
        self.po = lineEdit(self.fontSize)
        self.notes = textEdit(self.fontSize)
        self.screenshotItems = screenshot()
        self.google  = webWidget(self.fontSize)
        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [
            self.id_, 
            self.idLoad_,
            self.idWarehouse,
            self.type,
            self.no_,
            self.appointment,
            self.po, 
            self.notes,
            self.screenshotItems.bodega,
            self.screenshotItems.north,
            self.screenshotItems.west,
            self.google,
            self.screenshotItems.bodegaNotes]
        self.spacer = qtw.QSpacerItem(1,50)
        self.spacer2 = qtw.QSpacerItem(1,50)
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdLoad:', self.fontSize), self.idLoad_)
        self.layoutForm.addRow(labelWidget('IdWarehouse:', self.fontSize), self.idWarehouse)
        self.layoutForm.addRow(labelWidget('Type:', self.fontSize), self.type)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.no_)
        self.layoutForm.addRow(labelWidget('Appointment:', self.fontSize), self.appointment)
        self.layoutForm.addRow(labelWidget('PO:', self.fontSize), self.po)
        self.layoutForm.addRow(labelWidget("Notes", 16, fontColor="Blue", align="center"))
        self.layoutForm.addRow(labelWidget('Google:', self.fontSize), self.google)
        self.layoutForm.addRow(self.notes)
        self.layoutForm.addItem(self.spacer)
        self.layoutForm.addRow(self.screenshotItems)
        self.layoutForm.addItem(self.spacer2)
        
    # def configure_list(self):
        
        # self.btnAdd.setMaximumHeight(30)
        # self.listBtnsLayout = qtw.QVBoxLayout()
        # self.listBtnsLayout.setContentsMargins(5,0,0,0)
        # self.listBtnsLayout.addWidget(self.btnAdd)
        # self.listBtnsLayoutBox = qtw.QWidget()
        # self.listBtnsLayoutBox.setLayout(self.listBtnsLayout)
        # self.list.allFiltersLayout.addWidget(self.listBtnsLayoutBox,1,1)

    def setConnections(self):
        self.btnAdd.pressed.connect(self.displayAddForm)

        #g! FORM Connections
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.idWarehouse.textChanged.connect(lambda: self.formDirty(2,self.idWarehouse.getInfo()))
        self.type.true.toggled.connect(self.typeAfterUpdate)
        self.no_.textChanged.connect(self.no_AfterUpdate)
        self.appointment.dateTimeChanged.connect(self.appointmentAfterUpdate)
        self.po.textChanged.connect(self.poAfterUpdate)
        self.notes.textChanged.connect(self.notesAfterUpdate)
        
    def no_AfterUpdate(self):
        text = self.no_.getInfo()
        self.formDirty(4, text)
        self.screenshotItems.no_.setText(text)

    def typeAfterUpdate(self):
        text = self.type.getInfo()
        self.formDirty(3, text)
        self.screenshotItems.type.setText(text)

    def appointmentAfterUpdate(self):
        text = self.appointment.getInfo()
        self.formDirty(5, text)
        self.screenshotItems.appointment.setText(text)

    def poAfterUpdate(self):
        text = self.po.getInfo()
        self.formDirty(6, text)
        self.screenshotItems.po.setText(text)

    def notesAfterUpdate(self):
        text = self.notes.getInfo()
        self.formDirty(7, text)
        self.screenshotItems.notes.setText(text)

    def removeAllFilters(self):
        self.list.filtros.txt.reSet()
 
    def displayAddForm(self):
        if not self.addForm:
            #Create instance of add form
            self.addForm = warehouses()
            # set the id values esential for requery
            self.addForm.idLoad = self.idLoad
            # set all form elements for this load
            self.addForm.requery()
            #place on splitter
            self.splitter.insertWidget(1, self.addForm)
            #set connections to this item
            self.addForm.btnAdd.pressed.connect(self.addStopLoad)
            self.addForm.btnEditStop.pressed.connect(self.btnEditStopPressed)
            self.addForm.btn_cerrar.pressed.connect(self.closeAddForm)
            #set the widget sizes for the splitter
            # totalWidgets = self.splitter.count()
            # pass_ = 0
            # while pass_ < totalWidgets:
            #     print(self.splitter.widget(pass_))
            #     pass_+=1
            self.splitter.setSizes([500,600,0])
            self.splitter.setStretchFactor(0,1)
            self.splitter.setStretchFactor(1,2)

    def closeAddForm(self):
        """To avoid error when trying to requery form main loads form, set to false - from close code is set in class"""
        self.addForm = False
        self.splitter.setSizes([500,0,500])
        self.splitter.setStretchFactor(0,self.listWidth)
        self.splitter.setStretchFactor(2,self.formWidth)

    def addStopLoad(self):
        self.btnAddPressed()
        self.requery()

    def btnAddPressed(self):
        if self.idLoad:
            if self.addForm.list.treeview.selectionModel().hasSelection():
                indexes = self.addForm.list.treeview.selectionModel().selectedIndexes()
                idVar = indexes[0].data()
                #get the max value for this load and add 1
                sql = f'''SELECT 
                            MAX(no_) + 1
                            FROM loads_stops
                            WHERE idLoad = {self.idLoad}
                        ;'''
                number = self.db.get_records(sql)[0][0]
                # number = number
                if not number:
                    number=1
                # get the date of the load to start with it
                sql = f'''SELECT 
                            contractDate
                            FROM loads
                            WHERE id = {self.idLoad}
                        ;'''
                date = self.db.get_records(sql)[0][0]
                dateTime = str(date) + " 12:00"
                # date = date
                if idVar:
                    record = ("", self.idLoad, idVar, 1, number, dateTime, "", "")
                    self.insertNewRecord(record)
                   

    def btnEditStopPressed(self):
        if self.idLoad and self.list.treeview.selectionModel().hasSelection() and self.addForm.list.treeview.selectionModel().hasSelection:
            indexes = self.addForm.list.treeview.selectionModel().selectedIndexes()
            idVar = indexes[0].data()
            google = indexes[9].data()
            phone = functions.formatPhoneNo(indexes[8].data())
            warehouse = f'''{indexes[1].data()}
{indexes[4].data()}
{indexes[5].data()} {indexes[6].data()} {indexes[7].data()}
{phone}'''
            north = indexes[2].data()
            west = indexes[3].data()
            
            self.idWarehouse.populate(idVar)
            self.google.populate(google)
            self.screenshotItems.bodega.populate(warehouse)
            self.screenshotItems.north.populate(north)
            self.screenshotItems.west.populate(west)

    
    # name_ AS "Name", 1
        # address_ AS "Address", 4
    # city AS "City", 5
    # state_ AS "State", 6
    # zip AS "Zip", 7
    # phone AS "Phone", 8
    # google AS "Google Maps",
    # notes AS "Notes"

    def updateListRecord(self, record, selectionChanged):
        self.requery()
        #selection is lost on requery, select correct item!!
        if selectionChanged:
            # find the last i
            item = self.list.findItem(0, self.newSelectionId)
            index = self.list.proxyModel.index(item,0)
            self.list.treeview.setCurrentIndex(index)
        else:
            item = self.list.findItem(0, record[0])
            index = self.list.proxyModel.index(item,0)
            self.list.treeview.setCurrentIndex(index)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec()) 