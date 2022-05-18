#!/usr/bin/python3

from abc import abstractmethod
import sys
from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QSizePolicy,
    QVBoxLayout, QFrame, QApplication, QLabel, QSplitter, QFormLayout, QScrollArea,
    QSpacerItem, QMessageBox)
from PyQt6.QtGui import QPixmap, QIcon, QCloseEvent
from PyQt6.QtCore import Qt
from globalElements.treeview import treeviewSearchBox, filesTree
from globalElements.widgets import (buttonWidget, titleBox, spacer, 
    labelWidget,  deleteWarningBox, tabWidget, checkBox)
import html2text
from globalElements import DB, constants, functions as gf

 

class main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.iconAVD = QIcon(f'{constants.rootDb}oth/icons/enlace.png')#o!modify
        self.newSelectionId = ""
        self.initUi()
        
    def initUi(self):
        self.setConstants()
        self.setGlobalVariables()
        # self.sqlFolder = f"oth/sql/{self.sqlFolderName}"
        
        if self.size_ == "h2":
            self.setH2Settings()
        else: 
            self.setH1Settings()
        
        self.initList()
        self.initForm()
        self.initMain()
        self.set_connections()

#G!GLOBAL CONFIGURATION --------------------------------
    @abstractmethod
    def setGlobalVariables(self):
        '''set all variables as needed, including costants'''
        # DB INFO
        self.titleText = ""
        self.idColumn = ''#o! 
        self.tableVar = ''#o! 
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]#list, form - sizes
        
        self.listHiddenItems = ()
        self.listColumnWidth = ()
        self.listTableValuesIndexes = []
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.newRecordSql = '''
        
        '''
        self.selectSql = '''
        
        '''
    

    
    def createButtons(self):
        self.btnNew = buttonWidget(text=" Nuevo", 
            icon=constants.iconAdd, size=self.mainSize)
        self.btnDelete = buttonWidget(text=" Eliminar", 
            icon=constants.iconDelete, size=self.mainSize)
        self.btn_cerrar = buttonWidget(text=" Cerrar", 
            icon=constants.iconClose, size=self.mainSize)

        self.listOpt = checkBox('List   ',fontSize=self.fontSize, size=self.mainSize)
        self.listOpt.setChecked(True)
        self.formOpt = checkBox('Form',fontSize=self.fontSize, size=self.mainSize)
        self.formOpt.setChecked(True)
        self.widgetsOpt = [self.listOpt, self.formOpt]


    def setH2Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 10
        self.filterSize = 10

        self.mainSize = "h2"
        self.formSize = "h3"
        self.fontSize = 12

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=20,
            fontColor="White",
            align="center",
            backColor="#134A4D") 

        self.createButtons()

        self.spacerLeft = spacer('    ','h2')
        self.spacer1 = spacer(' ','h2')
        self.spacer2 = spacer('      ','h2')
        self.spacerRight = spacer(' ','h2')
        # self.titleLayout = QHBoxLayout()
        # self.titleLayout.setSpacing(0)
        # self.titleLayout.setContentsMargins(0,0,0,0)
        # # self.titleLayout.addWidget(self.spacerLeft)
        # # self.titleLayout.addWidget(self.logo)
        # self.titleLayout.addWidget(self.title,1)
        # self.titleLayout.addWidget(self.btnNew)
        # self.titleLayout.addWidget(self.spacer2)
        # self.titleLayout.addWidget(self.btnDelete)
        # self.titleLayout.addWidget(self.spacer1,1)
        # self.titleLayout.addWidget(self.btn_cerrar)
        # self.titleLayout.addWidget(self.spacerRight)
        
        # self.titleLayoutBox = titleBox('h2')
        # self.titleLayoutBox.setLayout(self.titleLayout)
        self.configureTitleLayout()

    def setH1Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 12
        self.filterSize = 11

        self.mainSize = "h1"
        self.formSize = "h2_"
        self.fontSize = 13
        

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=26,
            fontColor="White",
            align="center",
            #backColor="#002142"
            ) 
        
        self.createButtons()
        self.spacerLeft = spacer('    ')
        self.spacer1 = spacer(' ')
        self.spacer2 = spacer('      ')
        self.spacerRight = spacer(' ')
        self.configureTitleLayout()
        
    def configureTitleLayout(self):
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setSpacing(0)
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.addWidget(self.spacerLeft)
        # if self.mainSize == 'h1':
        #     self.titleLayout.addWidget(self.logo)
        self.titleLayout.addWidget(self.listOpt)
        self.titleLayout.addWidget(self.formOpt)
        self.titleLayout.addWidget(self.title,1)
        self.titleLayout.addWidget(self.btnNew)
        self.titleLayout.addWidget(self.spacer2)
        self.titleLayout.addWidget(self.btnDelete)
        self.titleLayout.addWidget(self.spacer1,1)
        self.titleLayout.addWidget(self.btn_cerrar)
        self.titleLayout.addWidget(self.spacerRight)
        
        self.titleLayoutBox = titleBox(self.mainSize)
        self.titleLayoutBox.setLayout(self.titleLayout)

    def setConstants(self):
        self.evaluateSaveIndex = (1,)
        self.andOr = "and"
        self.size_ = "h1"
        self.onNewFocusWidget = 1
        self.formItems = []
        self.formToDBItems = 0
        self.sortColumn = 1
        self.sortOrder = Qt.SortOrder.AscendingOrder
        self.listTableValues = [] 
        self.formTableValues = []
        self.horizontalLabels = ["Id"]
        
    def set_connections(self):
        #G! Connections
        self.list.treeview.selectionModel().selectionChanged.connect(self.listadoSelectionChanged)
        self.btn_cerrar.pressed.connect(self.btn_cerrar_pressed)
        self.btnSave.pressed.connect(self.btn_save_pressed)
        self.btnCancel.pressed.connect(self.btn_cancelar_pressed)
        self.btnDelete.clicked.connect(self.btn_delete_pressed) 
        self.btnNew.pressed.connect(self.btn_nuevo_pressed)
        # self.btn_folder.clicked.connect(self.btn_folder_pressed) 
        
        self.list.actRefresh.triggered.connect(self.requery)
        self.list.actClearFilters.triggered.connect(self.clearAllFilters)
        self.listOpt.toggled.connect(self.configureWidth)
        self.formOpt.toggled.connect(self.configureWidth)

    def initMain(self):
        
        self.setWindowIcon(self.iconAVD)
        self.setWindowTitle("ENLACE LLC")
        self.windowTitle().center(50)
        # self.configureMainBtns()
        self.setMainLayout()
        self.configureWidth

    def configureWidth(self):
        #dbInfor will give you a 1 if checked and a 0 if not checked
        widgetsOpt = list(map(lambda x: int(x.getDbInfo()), self.widgetsOpt))
        # widthSizes = []
        # index = 0
        if any(widgetsOpt):
            #for all the checked items, we will set the with size to its value, else to 0
            widthSizes  = []
            index = 0
            for i in widgetsOpt:
                if i:
                    widthSizes.append(self.widgetsOptSizes[index])
                else:
                    widthSizes.append(0)
                index +=1
        else:
            widthSizes = self.widgetsOptSizes

        totalExpand = sum(widthSizes)
        totalWidth = self.width()
        widthFraction = totalWidth//totalExpand
        
        widthSizes = list(map(lambda x: x * widthFraction, widthSizes)) 
        self.splitter.setSizes(widthSizes)


    def setMainLayout(self):
        #g! LAYOUT ---- **** Box container for details items
        #o! CONSIDER THE SPLITTER OPTION FOR THE SIDE TO SIDE FORM
        self.detailsLayout = QVBoxLayout()
        self.detailsLayout.setSpacing(0)
        self.detailsLayout.setContentsMargins(0,0,0,0)
        # self.splitter_details.addWidget(self.titleLayoutBox)
        # self.splitter_details.addWidget(self.layout_buttons_box)
        self.detailsLayout.addWidget(self.form)
        self.detailsLayout.addWidget(self.layoutFormSaveBtnBox)
        self.detailsBox = QWidget()
        # self.detailsBox.setFrameShape(QFrame.Shape.Box)
        # self.detailsBox.setFrameShadow(QFrame.Shadow.Raised)
        self.detailsBox.setLayout(self.detailsLayout)

        #g!LAYOUT LIST
        self.listLayout = QVBoxLayout()
        self.listLayout.setContentsMargins(0,0,0,0)
        self.listLayout.addWidget(self.list)
        self.listLayoutBox = QWidget()
        self.listLayoutBox.setLayout(self.listLayout)

        #g! MAIN SPLITTER
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.listLayoutBox)
        self.splitter.addWidget(self.detailsBox)
        

        self.layoutmain = QVBoxLayout()
        self.layoutmain.setSpacing(0)
        self.layoutmain.setContentsMargins(0,0,0,0)
        self.layoutmain.addWidget(self.titleLayoutBox,0)
        self.layoutmain.addWidget(self.splitter,1)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layoutmain)
        
        self.setCentralWidget(self.mainWidget)


    def initList(self):
        self.list = treeviewSearchBox() 
    
    def configureColumns(self):
        if self.listColumnWidth:
            self.list.setColumnsWith(self.listColumnWidth)
        if self.listHiddenItems:
            self.list.setHiddenColums(self.listHiddenItems)
        self.list.standardModel.setHorizontalHeaderLabels(self.horizontalLabels) 

    def listadoSelectionChanged(self):
        if self.list.treeview.selectionModel().hasSelection():
            self.newSelectionId = self.list.treeview.selectionModel().selectedIndexes()[0].data()
        self.save_record_main(True, True)#(update list, changed record)
        if self.list.treeview.selectionModel().hasSelection():
            # get all values from main list
            # This will get all the values of the list in place
            self.listTableValues = self.get_list_db_values()# self.mainList.getCurrentValues()
            # Populate details
            self.populateForm(self.listTableValues)
            # self.details.phone.format(self.details.phone.text())
            # set the forms value = list values
            self.formTableValues = self.listTableValues.copy()
        else:
            if self.listTableValues:
                for i in self.listTableValues:
                    i = ''
                self.clearForm()
        
        # try:
        self.setFilesFolder()

    @abstractmethod    
    def requery(self):
        return

    def clearAllFilters(self):
        if self.list.filtros.txt.getInfo():
            self.list.filtros.txt.clear()

  
    def initForm(self):
        self.form = QWidget()
        self.formButtons()
        self.formLayout()
        # self.formLayoutStraight()#o!delete -- only for testing
        
    def formButtons(self):
        self.btnSave = buttonWidget("  Guardar", self.formSize, constants.iconSave)
        self.btnCancel = buttonWidget("  Cancelar", self.formSize, constants.iconCancel)

       #G! Botones
        self.layoutFormSaveBtn = QHBoxLayout()
        
        self.layoutFormSaveBtn.addStretch()
        self.layoutFormSaveBtn.addWidget(self.btnSave)
        self.layoutFormSaveBtn.addWidget(self.btnCancel)
        self.layoutFormSaveBtn.addStretch()
        self.layoutFormSaveBtnBox = QWidget()
        self.layoutFormSaveBtnBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed )
        self.layoutFormSaveBtnBox.setLayout(self.layoutFormSaveBtn)
        self.layoutFormSaveBtn.setContentsMargins(15,5,15,5)

    def initFilesFolder(self):
        self.filesFolder = filesTree()
        self.filesFolder.setMinimumHeight(600)
        self.filesFolder.setMaximumHeight(900)
        self.filesFolder.root = constants.oneDrive
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
    
    def formLayout(self):
        self.layoutForm = QFormLayout()
        self.layoutForm.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layoutForm.setContentsMargins(0,0,0,0)
 
        self.layoutFormBox = QWidget()
        self.layoutFormBox.setContentsMargins(0,10,50,10)
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setLayout(self.layoutForm)
        self.layoutFormBox.setMaximumWidth(600)
        self.scrollBox = QScrollArea()
        self.scrollBox.setWidgetResizable(True)
        # self.scrollBox.setMinimumHeight(500)
        self.scrollBox.setStyleSheet(('''QScrollArea {border-style: none;};'''))
        self.scrollBox.setWidget(self.layoutFormBox)
        self.scrollBox.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    

    
# FORM LAYOUT OPTIONS 
# -------------------------------------------------------------------------------------------------
    def formLayoutStraight(self):
        '''
        Layout in a scrollBox just the form items with no files tree
        '''
        #this is the layout where the top buttons, form/files folder and bottom buttons go
        self.layoutFormStraight = QVBoxLayout()
        self.layoutFormStraight.setSpacing(15)
        self.layoutFormStraight.setContentsMargins(10,0,10,0)
        # self.main_layout.addWidget(self.lbl_Main)
        self.layoutFormStraight.addWidget(self.scrollBox) 
        self.form.setLayout(self.layoutFormStraight)
        
    def formLayoutStraightFilesTree(self):
        '''
        Includes the files tree in the current layout - Adds it to the top
        '''
        self.formLayoutStraight()
        self.initFilesFolder()
        self.spacerLeft = QSpacerItem(0,20)
        self.layoutForm.insertRow(0,self.filesFolder)

    def formLayoutSideFilesTree(self):
        self.initFilesFolder()
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0,0,0,0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.addWidget(self.scrollBox)
        self.hBoxLayout.addWidget(self.filesFolder)
        self.hBoxLayout.setAlignment(self.filesFolder,Qt.AlignmentFlag.AlignTop)
        self.form.setLayout(self.hBoxLayout)

    def formLayoutTabsFilesTree(self):
        self.initFilesFolder()
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0,0,0,0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.addWidget(self.scrollBox,2)
        self.hBoxLayout.addWidget(self.filesFolder,1)
        self.hBoxLayout.setAlignment(self.filesFolder,Qt.AlignmentFlag.AlignTop)
        self.hbox = QWidget()
        self.hbox.setLayout(self.hBoxLayout)

        self.tabsWidget = tabWidget("h2")
        self.tabsWidget.addTab(self.hbox, '    MAIN     ')

        self.formMainLayout = QHBoxLayout()
        self.formMainLayout.setContentsMargins(0,0,0,0)
        self.formMainLayout.setSpacing(0)
        self.formMainLayout.addWidget(self.tabsWidget)

        self.form.setLayout(self.formMainLayout)
        
        # self.layoutHBoxBox = qtw.QWidget()
        # self.layoutHBoxBox.setLayout(self.layoutHBox)
        

        # # self.scrollBox.setWidget(self.layoutHBoxBox)
        # self.setCentralWidget(self.layoutHBoxBox)
    
    #Y! FORM FUNCTIONS >>>>>>>>> FORM  FUNCTIONS >>>>>>>>>> FORM  FUNCTIONS >>>>>>>>>>> FORM FUNCTIONS 
    def formDirty(self, index, newValue):
        if self.formTableValues:
            self.formTableValues[index] = newValue

    def setFilesFolder(self):
        return

    def populateForm(self, record):#record 
        c = 0
        for i in self.formItems:
            # if i:
            if record[c]: 
                try:
                    i.populate(record[c])
                except Exception as e: 
                    print(str(e))
            else:
                i.reSet()
            c+=1
    
    #sets the form values compared at saving to empty string
    def setEmptyFormValues(self):
        #o! update record
        for i in self.formItems:
            self.formTableValues.append('')

    def clearForm(self):
        for i in self.formItems:
            i.reSet()
        self.formTableValues.clear()


    def closeEvent(self, a0: QCloseEvent) -> None:
        self.save_record_main(False, False)#updateList, changedSelection
        return super().closeEvent(a0)

    def btn_cerrar_pressed(self):
        self.deleteLater()
        # self.parentWidget().parentWidget().currentWidget().deleteLater()

    def btn_nuevo_pressed(self):
        # self.newRecord = True
        self.save_record_main(True, False)#updateList, changedSelection
        self.list.treeview.clearSelection()
        #before setting to New, save shoud happen with above code
        # self.listValues = ['New','']
        self.clearForm()
        # if hasattr(self.form, 'setFilesFolder'):
        self.setFilesFolder()
        self.formItems[self.onNewFocusWidget].setFocus()

    @abstractmethod
    def btn_delete_pressed(self):
        return
        # self.deleteRecord()

    def btn_cancelar_pressed(self):
        #w!when canceling, always make sure there is a selection set, to avoid and empty or 'New' 
        if self.list.treeview.selectionModel().hasSelection:
            #If there is already a selection, return list values and populate to selection
            self.listTableValues  = self.get_list_db_values()# self.mainList.getCurrentValues()
            self.populateForm(self.listTableValues)
        else:
            self.listTableValues.clear()
            #First set the listValues so when it tries to save, 
            self.list.selectFirstItem()
        self.setFilesFolder()

    def btn_save_pressed(self):
        self.save_record_main(True, False)

#g! FORM DATA MANIPULATION -----------------------------------------------------------------------
    #FORM - Colects the data - as needed to be saved in DB
    def getDBInfo(self):
        '''
        Goes through the form values and collects the neccesary data
        to save to the db
        '''
        evaluateItems = []
        if self.formToDBItems:
            for i in range(self.formToDBItems):
                widget = self.formItems[i]
                evaluateItems.append(widget)
        else: 
            evaluateItems = self.formItems.copy()
        infoList = []
        for i in evaluateItems:
            if hasattr(i, "getDbInfo"):
                info = i.getDbInfo()
            else: 
                info = i.getInfo()
            infoList.append(info)
        return infoList
    
    #Collects all information to update the values on the corresponding list record - including filter values not on form
    def getListInfo(self):
        '''
        Collects all information to update the values on the corresponding list record - including filter values not on form
        This is the general use function, to be used, table db values and form items must match by index exactly
        any discrepancies wont work and the method must be modified when an instance is created. 
        '''
        evaluateItems = []
        #this is used when not all items in the form match to the list
        if self.formToDBItems:
            for i in range(self.formToDBItems):
                widget = self.formItems[i]
                evaluateItems.append(widget)
        else: 
            evaluateItems = self.formItems.copy()
        infoList = []
        for i in evaluateItems:
            info = i.getInfo()
            infoList.append(info)
        return infoList
 
    #updates the values on all list used for evaluation 
    def updateListFormValues(self):
        record = self.getListInfo()
        self.listTableValues = record.copy()# record.copy()
        self.formTableValues = record.copy()# record.copy()
        return record
 
#g! LIST DATA MANIPULATION -----------------------------------------------------------------------
    #used the indexes provided, to get the values from the list 
    #Return only the values that need to be used for comparison and to populate the form
    # in the same order that they appear on the db table
    def get_list_db_values(self):
        record = self.list.getCurrentValues()
        values = []
        if record:
            for i in self.listTableValuesIndexes:
                values.append(record[i]) 
            return values

#G! CONFIGURE SQL ----------------------------------------------------------------------
    
    def updateRecord(self):
        return

    def selectAll(self, parameters=0): 
        # sql = self.getSQL(self.selectSql)#make sure sql has no ending statement
        parameters = parameters
        records = self.db.get_records_clearNull(self.selectSql, parameters) 
        self.horizontalLabels = self.db.cursor.column_names
        return records 
    
    def insertNewRecord(self, record):
        r = gf.insertNewRecord(record)
        # sql = self.getSQL(self.newRecordSql)
        sql = f"{self.newRecordSql} ({r});"
        idVar = self.db.insertNewRecord(sql)

        return idVar
    
    def getSQL(self, file):
        # filePath = f"{self.sqlFolder}/{file}"
        sqlFile = open(file, "r")
        sqlFileText = sqlFile.read()
        sqlFile.close()
        return sqlFileText

    def deleteRecord(self, text = ''): 
        if self.list.treeview.selectionModel().hasSelection():
            idVar = self.list.treeview.selectionModel().selectedIndexes()[0].data()
            warning_box = deleteWarningBox(text)
            button = warning_box.exec()

            if button == QMessageBox.StandardButton.Yes:
                
                self.save_record_main(True,False)
                # values_ = (IdVar,)
                self.db.deleteOne(self.tableVar, self.idColumn, idVar)
                #find row of standard model to delete regarldess of filter
                #clear list values to avoid saving after deletion because selection will change
                self.listTableValues.clear()
                #find row of standard model to delete regarldess of filter
                rowVar = self.list.findItem(0,idVar)
                self.list.standardModel.removeRow(rowVar)
            
#g! SAVE PROCEDURES -----------------------------------------------------------------------START
    def save_record_main(self,updateList, changedSelection):
        #at this point, the selecte item might or might not be equal to the record being updated
        
        idVar = self.id_.text()
        
        if not idVar:#y! New Record
            #Before filling form, values of list and form were empty, therefore, list are empty and will cause problems on comparing. 
            #to avoid this problems, set both lists to form values when saving. 
            #Codigo especifico en form para evaluar si se han alterado o no los campos
            saveRecord = False
            if self.evaluateNewRcdSave(self.evaluateSaveIndex, self.andOr):
                self.save_record_toDb(True)#y! this will save the record, no return
                # get all values from form and make them the same for list and formValues
                if updateList:
                    record = self.updateListFormValues()
                    self.addListRecord(record, changedSelection)
                    # self.list.addRecords((record,))
                    # # find the row of the item with filters applied - 
                    # if not changedSelection:
                    #     itemRow = self.list.findItemFiltered(0,record[0])
                    #     if itemRow:
                    #         # set the index with the given row
                    #         itemIndex = self.list.proxyModel.index(itemRow,0)
                    #         # select the added item. 
                    #         self.list.treeview.setCurrentIndex(itemIndex)
                            #o! setting folder should not be necessary, it should set with new selection
                self.setFilesFolder()
                
        else:
            saveRecord = self.compareValues()#Returns Tru or False for Save or is New Record
        
        if saveRecord:
            #get the record with the new Id if saved as new
            self.save_record_toDb(False)
            #Keep going if list must be updated
            if updateList:
                #list will only be updated if form will remain open, now worth adding process when closing
                record = self.updateListFormValues()
                # find the row of the item with filters applied - 
                if changedSelection:
                    self.updateListRecord(record, True)
                else:
                    self.updateListRecord(record, False)
                    
    # When ID value if blank, it will evaluate it a new record is present and save it
    def addListRecord(self,record,changedSelection):
        self.list.addRecords((record,))
        # find the row of the item with filters applied - 
        if not changedSelection:
            itemRow = self.list.findItemFiltered(0,record[0])
            if itemRow:
                # set the index with the given row
                itemIndex = self.list.proxyModel.index(itemRow,0)
                # select the added item. 
                self.list.treeview.setCurrentIndex(itemIndex)
    def updateListRecord(self,record, selectionChanged):
        if selectionChanged:
            #c!Find and change the record 
            item = self.list.findItem(0, record[0])
            #update record on given row (parameters(row,record))
            self.list.editItem(item, record)
        else:
            indexes = self.list.treeview.selectionModel().selectedIndexes()
            c = 0
            items = len(record) - 1
            for i in indexes:
                if items >= c:
                    self.list.proxyModel.setData(i,record[c])
                c += 1
            self.setFilesFolder()

    def evaluateNewRcdSave(self, itemsIndex = (0,), andOr = "and"):
        if itemsIndex[0] == 0:
            return False
        #get the values of the items provided
        values = []
        for i in itemsIndex:
            iValue = self.formItems[i].getInfo()
            values.append(iValue)
        
        if andOr == "or":
            return any(values)

        elif andOr == "and":
            return all(values)

    
    def save_record_toDb(self, newRecord):
        #O! LIMPIAR TODOS LOS ELEMENTOS ANTES DE SUBIR A BASE DE DATOS
        record = self.getDBInfo()
        queryRecord = record.copy()
        queryRecord = gf.recordToSQL(queryRecord)

        if newRecord:
            idVar = self.insertNewRecord(queryRecord)
            # form item 0 should always hold the id value
            self.formItems[0].populate(str(idVar))
        else:
            self.updateRecord(queryRecord)

    #Compare the values on the form and the values form the list - if they are different, save the changes. 
    #listTableValues and formTableValues are compared
    def compareValues(self):
        #w! Comparison takes effect before changing values on list and details to new selection
        if self.listTableValues:
            #Check if there is any values in main list, #w!else, return false, false - when canceling a new record this will be the return
            #Compare values
            #list items
            listValues = self.listTableValues.copy()
            #make all html items plain text for better comparison
            richTextItems = self.htmlToPlain(listValues)
            for i in richTextItems:
                listValues[i[0]] = i[1]
            
            #form items
            formValues = self.formTableValues.copy()
            if not formValues:
                return False 
            richTextItems = self.htmlToPlain(formValues)
            for i in richTextItems:
                formValues[i[0]] = i[1]
            
            #compare the values in each items
            counter = 0
            for i in listValues:
                if i != formValues[counter]:
                    return True
                counter+=1
        #if no selection is made 
        else:
            return False

    #convert all html items to plain text for better comparison
    def htmlToPlain(self, list):
        richTextItems = []
        for i in list:
            if isinstance(i,str):
                compareValue = i[0:14]
                if compareValue == '<!DOCTYPE HTML':
                    index = list.index(i)
                    i = html2text.html2text(i).replace('\n','')
                    i = i.replace(' ','')
                    richTextItems.append((index,i))
        return richTextItems
             
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())