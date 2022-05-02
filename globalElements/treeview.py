#!/usr/bin/python3
from PyQt6.QtWidgets import (QMainWindow, QTreeView, 
    QFormLayout, QWidget, QSizePolicy, QGridLayout, QVBoxLayout,
    QToolBar, QFileDialog, QApplication, QMenu, QMessageBox)

from PyQt6.QtCore import (Qt, QSortFilterProxyModel,
    QSize,QRegularExpression)

from PyQt6.QtGui import (QIcon, QAction, QStandardItemModel, QCursor, 
    QFileSystemModel, QGuiApplication, QWheelEvent)

from globalElements.widgets import (labelWidget, lineEditFilterGroup, 
    standardItem, buttonWidget, lineEdit)

from globalElements import functions, constants

import os
import csv
import sys

iconRoot = f'{constants.othFolder}\icons'

class treeviewSearchBox(QMainWindow):
    def __init__(self, fontSize=13,sortColumn =1,sortOrder = Qt.SortOrder.AscendingOrder):
        super().__init__()
        # self.totalRecords = 0
        self.recordTotal = 0
        self.recordCurrent = 0

        
        self.iconClearSelection = QIcon(f'{iconRoot}\\removeSelection.png')
        self.iconRefresh = QIcon(f'{iconRoot}\\refresh.png')
        self.iconClearFilters = QIcon(f'{iconRoot}\clear-filter.png')
        self.iconShowFilters = QIcon(f'{iconRoot}\\filterShow.png')
        self.iconHideFilters = QIcon(f'{iconRoot}\\filterHide.png')
        self.iconExcel = QIcon(f'{iconRoot}\excel.png')
        

        self.actRefresh = QAction('Refresh')
        self.actRefresh.setIcon(self.iconRefresh)
        # self.actRefresh.triggered.connect
        # treeview.actRefresh.triggered.connect

        self.actClearSelect = QAction('Selection')
        self.actClearSelect.setIcon(self.iconClearSelection)
        self.actClearSelect.triggered.connect(self.selectionClear)

        self.actClearFilters = QAction('Clear')
        self.actClearFilters.setIcon(self.iconClearFilters)
        # treeview.actClearFilters.triggered.connect
        self.actShowFilters = QAction('Show')
        self.actShowFilters.setIcon(self.iconShowFilters)
        self.actShowFilters.triggered.connect(self.showFilters)

        self.actCSV = QAction("Exportar a excel")
        self.actCSV.setIcon(self.iconExcel)
        self.actCSV.triggered.connect(self.recordsToCSV)


        


        # self.currentSelection = []
        # self.lastSelection = []
        # self.sortColumn = sortColumn
        self.treeview = QTreeView()
        self.treeview.setUniformRowHeights(True)
        self.treeview.setSortingEnabled(True )
        self.standardModel = QStandardItemModel() 
        # self.standardModel.invisibleRootItem().setText("")
        self.proxyModel = QSortFilterProxyModel() #w! Create filtering model 
        self.proxyModel.setSourceModel(self.standardModel)
        self.treeview.setModel(self.proxyModel)#w! Assign object model to tree
        self.rootNode = self.standardModel.invisibleRootItem()
        self.treeview.setAlternatingRowColors(True)

        self.filtros = lineEditFilterGroup(fontSize)
        self.currRecordLabel = labelWidget('',11)

        self.layoutFilter = QFormLayout()
        self.layoutFilter.addRow(labelWidget("Busqueda: ", fontSize), self.filtros)
        # self.layoutFilter.addStretch()
        self.layoutFilter.setContentsMargins(0,0,0,3)
        self.layoutFilterBox = QWidget()
        self.layoutFilterBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.layoutFilterBox.setLayout(self.layoutFilter)

        #g!Hidde items Layout 
        self.layoutHiddenFilters = QFormLayout()
        self.layoutHiddenFilters.setContentsMargins(0,0,0,0)

        self.layoutHiddenFiltersBox = QWidget()
        self.layoutHiddenFiltersBox.setFixedHeight(0)
        self.layoutHiddenFiltersBox.setLayout(self.layoutHiddenFilters)
        self.layoutHiddenFiltersBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.allFiltersLayout = QGridLayout() 
        self.allFiltersLayout.setContentsMargins(0 ,0,0,0)
        self.allFiltersLayout.setSpacing(0)
        self.allFiltersLayout.addWidget(self.layoutHiddenFiltersBox, 0,0)
        self.allFiltersLayout.setAlignment(self.layoutHiddenFiltersBox,Qt.AlignmentFlag.AlignLeft)
        self.allFiltersLayout.addWidget(self.layoutFilterBox,1, 0)
        self.allFiltersLayout.setAlignment(self.layoutFilterBox,Qt.AlignmentFlag.AlignLeft)
        self.allFiltersLayoutBox = QWidget()
        self.allFiltersLayoutBox.setLayout(self.allFiltersLayout)

        self.layoutDetails = QFormLayout()
        self.layoutDetails.setContentsMargins(0,0,0,0)
        # self.layoutDetails.setAlignment()
        self.layoutDetails.addRow(labelWidget("Registro: ", 11), self.currRecordLabel)
        self.layoutDetailsBox = QWidget()
        self.layoutDetailsBox.setLayout(self.layoutDetails)
        
        #o! make sure size policy is working and item is not growing. 
        self.layoutDetailsBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layoutFiltersDetails = QVBoxLayout()
        self.layoutFiltersDetails.setSpacing(0)
        self.layoutFiltersDetails.setContentsMargins(5,0,0,0)

        self.layoutFiltersDetails.addWidget(self.allFiltersLayoutBox)
        self.layoutFiltersDetails.addWidget(self.layoutDetailsBox)
        self.layoutFiltersDetails.setAlignment(self.layoutDetailsBox, Qt.AlignmentFlag.AlignBottom)
        # self.layoutFiltersDetails.addStretch(1)
        self.layoutFiltersDetailsBox = QWidget()
        self.layoutFiltersDetailsBox.setLayout(self.layoutFiltersDetails)

        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(self.layoutFiltersDetailsBox)
        
        # self.layout_.addWidget(self.lblCountLayoutBox)
        self.layout_.addWidget(self.treeview)
        
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,5,0,0)
        self.layoutBox = QWidget()
        self.layoutBox.setLayout(self.layout_)

        # self.setLayout(self.layout_)
        self.setCentralWidget(self.layoutBox)
 
        self.filtros.txt.textChanged.connect(lambda: self.search_afterUpdate(sortColumn, sortOrder))
        self.filtros.btn.pressed.connect(self.clearFilter)
        self.treeview.selectionModel().selectionChanged.connect(self.main_list_selection)
        self.proxyModel.rowsInserted.connect(self.countRows)
        self.proxyModel.rowsRemoved.connect(self.countRows)
    
    #     if toolbar:
    #         self.configureToolbar(toolbar)
    # def configureToolbar(self, position):
         #p! Tool Bar
        self.toolBar = QToolBar('File')
        iconSize = QSize(18,40)
        
        self.toolBar.setIconSize(iconSize)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        # self.toolBar.addAction('Crear Archivo')
        self.toolBar.addAction(self.actRefresh)
        self.toolBar.addAction(self.actClearFilters)
        self.toolBar.addAction(self.actClearSelect)
        self.toolBar.addAction(self.actShowFilters)
        self.toolBar.addAction(self.actCSV)
        # if position  == "left":
        #     pass
        
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolBar)
    
    def recordsToCSV(self):
        # Get the number of rows and columns
        rows = self.proxyModel.rowCount()
        if not rows:
            return
        columns = self.proxyModel.columnCount()
        #Get a list of all the records.
        row = 0
        
        #o!codigo para cuando no hay registros
        records = []
        while row < rows:
            #pasa por cada fila
            column = 0
            rowValues = []
            while column < columns:
                #toma la informacion de cada columna
                index = self.proxyModel.index(row, column)
                cellValue = self.proxyModel.data(index)
                rowValues.append(cellValue)
                column += 1
            records.append(rowValues)
            row += 1
        
        #Get the Horizontal labels from the treeview to use as headers
        fileHeader = []
        column = 0
        while column < columns:
            columnNo = self.standardModel.horizontalHeaderItem(column)
            if columnNo:
                text = columnNo.text()
                fileHeader.append(text)
            column += 1
        #y! Write file to a csv
        #open a file dialog to choose file name and location
        filePathDialog = QFileDialog()
        filePathDialog.setMinimumSize(600,600)
        filePathDialog.setObjectName("archivo")
        filePath = filePathDialog.getSaveFileName(
            caption="Elegir carpeta para guardar archivo",
            directory = constants.oneDrive,
            filter="*.csv")[0]

        
        #if operation is not cancelled
        if filePath:
            # filePath = filePath[0]
            #verify if .csv was added or a file is to be replaced, if not, ad file extention name. 
            if not filePath[-4:] == ".csv":
                filePath = f"{filePath}.csv"
            #write csv file
            with open(filePath,'w', newline="") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(fileHeader)

                for row in records:
                    writer.writerow(row)
            #open csv file. 
            os.startfile(filePath)

    def countRows(self):
        #o! include code in source to add or subtract 
        #find the total rows and place it in label
        self.recordTotal = self.proxyModel.rowCount()
        self.updateLabelRecords()
    
    def updateLabelRecords(self):
        record = f'{str(self.recordCurrent)} de {str(self.recordTotal)}'    
        self.currRecordLabel.setText(record)
        
    def showFilters(self):
        currHeight = self.layoutHiddenFiltersBox.height()
        if currHeight == 0:
            items = self.layoutHiddenFilters.rowCount()
            # self.layoutHiddenFilters.rowCount
            
            if items:
                height = items * 29
                self.layoutHiddenFiltersBox.setFixedHeight(height)
                self.actShowFilters.setIcon(self.iconHideFilters)
                self.actShowFilters.setText('Hide')

        else: 
            self.layoutHiddenFiltersBox.setFixedHeight(0)
            self.actShowFilters.setIcon(self.iconShowFilters)
            self.actShowFilters.setText('Show')

    
    def selectionClear(self):
        self.treeview.clearSelection()
    
    def getColumnValues(self, searchColumns):
        # '''Input parameter must be a tuple or list '''
        if not isinstance(searchColumns, (list,tuple)):
            if isinstance(searchColumns, int):
                searchColumns = (searchColumns,)
            
        NoRecords = self.proxyModel.rowCount()
        row = 0
        data = []
        while row < NoRecords:
            # this list will hold the row values to be returned
            currValues = []
            for column in searchColumns:
                # i must be an integer - all provided values must be integers
                index = self.proxyModel.index(row,column)
                value = self.proxyModel.data(index)
                currValues.append(value)
            data.append(currValues)
            row += 1
        return data
 
    # def findItemFiltered(self, searchColumn, searchValue):
    #     '''this code will find the row at the main values before they are filtered
    #     even if there is a filter, it will find the correct row and return it'''
    #     NoRecords = self.proxyModel.rowCount()
    #     currRecord = 0
    #     while currRecord < NoRecords:
    #         index = self.proxyModel.index(currRecord,searchColumn)
    #         if str(searchValue) == self.proxyModel.data(index): # Esta ultima parte nos da el valor del texto en la lista
    #             #return row no.
    #             return currRecord, index
    #         currRecord += 1
    def findItemFiltered(self, searchColumn, searchValue, returnValue = "Row"):
        '''this code will find the row at the main values before they are filtered
        even if there is a filter, it will find the correct row and return it'''
        NoRecords = self.proxyModel.rowCount()
        currRecord = 0
        while currRecord < NoRecords:
            index = self.proxyModel.index(currRecord,searchColumn)
            if str(searchValue) == self.proxyModel.data(index): # Esta ultima parte nos da el valor del texto en la lista
                if returnValue == "Index":
                    return index
                elif returnValue == "Row":
                    return currRecord
            currRecord += 1

    def findItem(self, searchColumn, searchValue):
        '''this code will find the row at the main values before they are filtered
        even if there is a filter, it will find the correct row and return it'''
        NoRecords = self.standardModel.rowCount()
        currRow = 0
        searchValue = str(searchValue)
        while currRow < NoRecords:
            index = self.standardModel.index(currRow,searchColumn)
            treeValue = self.standardModel.data(index)
            if searchValue == treeValue: # Esta ultima parte nos da el valor del texto en la lista
                #return row no.
                return currRow
            currRow += 1
        # return itemRow
    
    def editItem(self, row, record): 
        
        if record:
            column = 0
            for i in record:
                self.standardModel.setData(self.standardModel.index(row,column), i)
                column +=1

    def removeAllRows(self):
        self.standardModel.removeRows(0, self.standardModel.rowCount())
    
    def addRecords(self, records, fontSize=13, rowHeight=42, colorVar ='#000000'):
        if records:
            for item in records: 
                
                stdItemItem = list(map(lambda x: standardItem(str(x),fontSize,rowHeight,colorVar),item))
                self.rootNode.insertRow(0, stdItemItem)
    
    def addRecordsCarriers(self, records,carrierColumn, fontSize, rowHeight, accounting = False):
        ungrouped = [] 
        avd = []
        dnp = []
        calvillo = []
        #iterate through all records and add to each hauling carrier their loads
        for i in records:
            # print(i)
            if i[carrierColumn] == "AVD TRUCKING LLC":#
                avd.append(i)
            elif i[carrierColumn] == "DNP FREIGHT LLC":#
                dnp.append(i)
            elif i[carrierColumn] == "T M CALVILLO TRANSPORT":#
                calvillo.append(i) 
            else:
                ungrouped.append(i)
        #add all the records, group by group
        if accounting:
            if avd:
                self.addRecordsAccounting(avd,5,7, fontSize, rowHeight, "Black")
            if dnp:
                self.addRecordsAccounting(dnp, 5,7,fontSize, rowHeight, "Blue")
            if calvillo:
                self.addRecordsAccounting(calvillo, 5,7,fontSize, rowHeight, "Green")
            if ungrouped:
                self.addRecordsAccounting(ungrouped,5,7, fontSize, rowHeight, "Red")
        else:
            if avd:
                self.addRecords(avd, fontSize, rowHeight, "Black")
            if dnp:
                self.addRecords(dnp, fontSize, rowHeight, "Blue")
            if calvillo:
                self.addRecords(calvillo, fontSize, rowHeight, "Green")
            if ungrouped:
                self.addRecords(ungrouped, fontSize, rowHeight, "Red")

    def addRecordsAccounting(self, records, amountRow, typeRow, fontSize=13, rowHeight=42, colorVar ='#000000'):
        if records:
            # stdItemsRecords = []
            for i in records: 
                #set the color to be used on amount 
                if i[typeRow] == "Expense":
                    amountColor = "Red"
                else:
                    amountColor = colorVar
                #Create the list of the standard items 
                stdItemsRow = []
                itemNo = 0
                for item in i:
                    if itemNo == amountRow:
                        stdItemsRow.append(standardItem(str(item), fontSize, rowHeight, amountColor))
                    else:
                        stdItemsRow.append(standardItem(str(item), fontSize, rowHeight, colorVar))
                    itemNo += 1
                self.rootNode.insertRow(0, stdItemsRow)

    def requery(self, records, sizeVar=13, rowHeight=42, colorVar ='#000000'):
        self.removeAllRows()
        self.addRecords(records, sizeVar, rowHeight, colorVar)

    def requeryColorAccounting(self, records, isIncomeColumn, isBusinessColumn,sizeVar=13, rowHeight=42):
        self.removeAllRows()
        BusinessIncome = []
        BusinessExpense = []
        income = []
        expense = []
        unclasified = []
        for i in records:
            if i[isBusinessColumn] == "0" or i[isBusinessColumn] == "False" or i[isBusinessColumn] == "":
                # Not business entries
                if i[isIncomeColumn] == "Income":
                    income.append(i)
                elif i[isIncomeColumn] == "Expense":
                    expense.append(i)
                else:
                    #Unclassified
                    unclasified.append(i)
            else: 
                #Business entries
                if i[isIncomeColumn] == "Income":
                    BusinessIncome.append(i)
                elif i[isIncomeColumn] == "Expense":
                    BusinessExpense.append(i)
                else:
                    #Unclassified
                    unclasified.append(i)
        self.addRecords(BusinessIncome, sizeVar, rowHeight)
        self.addRecords(BusinessExpense, sizeVar, rowHeight, "Red")
        self.addRecords(income, sizeVar, rowHeight, "#757575")
        self.addRecords(expense, sizeVar, rowHeight, "#FF7979")
        self.addRecords(unclasified, sizeVar, rowHeight, "Blue")


    def requeryColor(self, records, column, sizeVar=13, rowHeight=42):
        self.removeAllRows()
        groupedRecords = {}
        for i in records:
            #take te value to be used to group and create key on dict with empy list - there will be no repeats
            groupedRecords[i[column]] = []
            
        standardRecords = []
        for i in records:
            # see if record meets sort Criteria
            if i[column] in groupedRecords.keys():
                #append to dictionary values list if meet search critera
                groupNo = 0
                for k in groupedRecords.keys():
                    if k == i[column]:
                        groupedRecords[k].append(i)
                    groupNo += 1
            else:
                #All records that dont meet search critera are standard
                standardRecords.append(i)

        colorRow = 0
        for k in groupedRecords.keys():
            if k == '0' or k == 0:
                 self.addRecords(groupedRecords[k], sizeVar, rowHeight)
            else:
                colors = ["Black", "Red", 'Blue', 'Green','DarkOrange','DarkSalmon','DarkRed','DarkViolet','Crimson','Brown','DarkBlue','DarkMagenta','Orange','Purple', '#833C0B','#385623','#1F3864','#806000']
                limit = len(colors)
                if colorRow < limit:
                    self.addRecords(groupedRecords[k], sizeVar, rowHeight, colors[colorRow])
                else:
                    self.addRecords(groupedRecords[k], sizeVar, rowHeight)
                colorRow+=1
        self.addRecords(standardRecords, sizeVar, rowHeight)
        # self.lblCount.setText(self.proxyModel.rowCount())

    def getCurrentValues(self):
        if self.treeview.selectionModel().hasSelection():
            indexes = self.treeview.selectionModel().selectedIndexes()
            return list(map(lambda x: self.proxyModel.data(x),indexes))
    
    def main_list_selection(self): 
        selectionModel = self.treeview.selectionModel()
        if selectionModel.hasSelection():
            #if there is a selection, find the reow number
            index = selectionModel.selectedRows()[0]
            currRow = 0
            totalRows = self.proxyModel.rowCount()
            while currRow < totalRows:
                rowIndex = self.proxyModel.index(currRow, 0)
                if rowIndex == index:
                    self.recordCurrent =  currRow + 1
                    # self.updateLabelRecords()
                    # print(currRow)
                    break
                currRow += 1
        
        else:
            #if no selection is made set current record to 0
            self.recordCurrent = 0
        self.updateLabelRecords()
    
    def clearFilter(self):
        self.filtros.txt.clear()
        self.filtros.txt.setFocus()
 
    def selectFirstItem(self):
        firstItem = self.proxyModel.index(0,0)
        self.treeview.setCurrentIndex(firstItem)
        
    def search_afterUpdate(self, sortColumn=1, order = Qt.SortOrder.AscendingOrder,filter=True, sort=True):
        if filter:
            self.treeview.clearSelection()
            text = self.filtros.txt.text()
            self.search = functions.create_regEx(text)
            self.regEx_search = QRegularExpression(self.search,QRegularExpression.PatternOption.CaseInsensitiveOption)
            self.proxyModel.setFilterRegularExpression(self.regEx_search)
            self.proxyModel.setFilterKeyColumn(-1)
        if sort:
            self.proxyModel.sort(sortColumn, order)

    def setColumnsWith(self, columns):
        for i in columns:
            self.treeview.setColumnWidth(i[0],i[1])
    
    def setHiddenColums(self, columns):
        for i in columns:
            self.treeview.hideColumn(i)


class filesTree(QMainWindow):
    def __init__(self):
        super().__init__()
        #g! ICONS
        self.iconClearSelection = QIcon(f'{iconRoot}\\removeSelection.png')
        self.iconOpenFile = QIcon(f'{iconRoot}\\google-docs.png')
        self.iconOpenFolder = QIcon(f'{iconRoot}\\openFolder.png')
        self.iconNewFolder = QIcon(f'{iconRoot}\\folderAdd.png')
        self.iconAVD= QIcon(f'{iconRoot}\\LOGO_WORLD.png')
        self.iconDelete= QIcon(f'{iconRoot}\\delete.png')
        self.iconClearSelection= QIcon(f'{iconRoot}\\removeSelection.png')
        self.iconCopy = QIcon(f'{iconRoot}\\link.png')


        self.filesModel = QFileSystemModel() #data item model
        self.filesModel.setReadOnly(False)
        self.root = constants.oneDrive #os.path.expanduser('~\OneDrive')
        self.filesDir = self.root # this variable will be changing to addapt to the box location and record selected
        self.filesModel.setRootPath(self.filesDir) #assignment that will be changing. 
        self.filesTree = QTreeView() # Tree item
        self.filesTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.filesTree.setDragEnabled(True)
        self.filesTree.setAcceptDrops(True)
        self.filesTree.setDropIndicatorShown(True)
        
        # self.filesTree.
        self.filesTree.setModel(self.filesModel)
        self.filesTree.setRootIndex(self.filesModel.index(self.filesDir))
        self.filesTree.hideColumn(1)
        self.filesTree.hideColumn(2)
        self.filesTree.hideColumn(3)

        #p! Tool Bar
        self.toolBar = QToolBar('File')
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        # self.toolBar.addAction('Crear Archivo')
        
        #g! Actions
        self.action_open = QAction('Abrir archivo')
        self.action_open.setIcon(self.iconOpenFile)
        self.action_open.triggered.connect(self.file_open)
        # Delete file action
        self.action_delete = QAction('Eliminar')
        self.action_delete.setIcon(self.iconDelete)
        self.action_delete.triggered.connect(self.file_delete)
        # New Folder file action
        self.action_newFolder = QAction('Crear carpeta')
        self.action_newFolder.setIcon(self.iconNewFolder)
        self.action_newFolder.triggered.connect(self.new_folder)
        # Delete file action
        self.action_copyPath = QAction('Copiar vinculo')
        self.action_copyPath.setIcon(self.iconCopy)
        self.action_copyPath.triggered.connect(self.copyPath) 
        # Delete file action
        self.action_ClearSelection = QAction('Eliminar selección')
        self.action_ClearSelection.setIcon(self.iconClearSelection)
        self.action_ClearSelection.triggered.connect(self.selection_clear)
        # Open Folder action
        self.actionOpenFolder = QAction('Abrir folder')
        self.actionOpenFolder.setIcon(self.iconOpenFolder)
        self.actionOpenFolder.triggered.connect(self.folderOpen)

        self.toolBar.addAction(self.actionOpenFolder)
        self.toolBar.addAction(self.action_open)
        self.toolBar.addAction(self.action_delete)
        self.toolBar.addAction(self.action_newFolder)
        self.toolBar.addAction(self.action_copyPath)
        self.toolBar.addAction(self.action_ClearSelection)
        iconSize = QSize(35,20)
        self.toolBar.setIconSize(iconSize)
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        self.filesLabel = labelWidget('Folder:',10)
        self.txtFilePath = lineEdit(8)
        self.txtFilePath.setReadOnly(True)
        # self.copyBtn = gw.btn_copyIcon()
        self.layout_files = QGridLayout()
        self.layout_files.setSpacing(0)
        # self.layout_files.setContentsMargins(0,50,0,0)
        # self.layout_files.addWidget(self.filesLabel,0,0)
        # self.layout_files.addWidget(self.txtFilePath,0,1)
        # self.layout_files.addWidget(self.copyBtn,0,2)
        self.layout_files.addWidget(self.filesTree,1,0,1,3)
        self.layout_files_box = QWidget()
        self.layout_files_box.setLayout(self.layout_files)
        # self.layout().setContentsMargins(0,800,0,0)
        self.setCentralWidget(self.layout_files_box)

        # self.copyBtn.pressed.connect(self.copyPath)
        self.txtFilePath.textChanged.connect(self.setPath)
        self.txtFilePath.setText(self.root)
        self.filesTree.customContextMenuRequested.connect(self.contextMenu)
        self.filesTree.doubleClicked.connect(self.file_open)

    def setLineEditFileBox(self, fontSize=13):
        self.lineEditItems = lineEditFilterGroup(fontSize,"Archivo:", clearFilter=False)
        # self.lineEditItems.lbl.deleteLater()
        self.btnOpen =  buttonWidget(text="Abrir archivo", size="h2", icon=constants.iconFolderOpen)
        self.btnOpen.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        # self.btnOpen.setMinimumWidth(130)
        self.btnLinkFile = buttonWidget(text="Vincular archivo", size="h2", icon=constants.iconLink)
        self.btnLinkFile.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        
        self.layoutLineEditFile = QGridLayout()
        self.layoutLineEditFile.setSpacing(1)
        self.layoutLineEditFile.addWidget(self.lineEditItems,0,0,1,2)
        self.layoutLineEditFile.addWidget(self.btnOpen,1,0)
        self.layoutLineEditFile.addWidget(self.btnLinkFile,1,1)
        self.layoutLineEditFileBox = QWidget()
        self.layoutLineEditFileBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layoutLineEditFileBox.setLayout(self.layoutLineEditFile)

        # self.setLayout(self.layout_)

        self.btnLinkFile.pressed.connect(self.setFile)
        self.btnOpen.pressed.connect(self.openFile)

    def populate(self, text):
        self.lineEditItems.txt.setText(text)
    
    def reSet(self):
        self.lineEditItems.txt.clear()

    def getInfo(self):
        return self.lineEditItems.txt.text()

    def setFile(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                filePath = self.filesModel.filePath(index)
                folderPath = f'{self.txtFilePath.text()}\\'
                folderPath = folderPath.replace('\\','/')
                fileName = filePath.replace(folderPath,'')
                self.lineEditItems.txt.setText(fileName)  

    def openFile(self):
        fileName = self.lineEditItems.txt.text()
        if fileName:
            folderPath = self.txtFilePath.text()
            filePath = f'{folderPath}/{fileName}'
            try:
                os.startfile(filePath)
            except:
                print('Archivo no existe')
    
    def contextMenu(self):
        # add items to menu
        menu = QMenu()
        menu.addAction(self.actionOpenFolder)
        menu.addAction(self.action_open)
        menu.addAction(self.action_delete)
        menu.addAction(self.action_newFolder)
        menu.addAction(self.action_copyPath)
        menu.addAction(self.action_ClearSelection)
        cursor = QCursor()
        menu.exec(cursor.pos())
    
    def setPath(self, path):
        self.filesDir = path
        self.filesModel.setRootPath(self.filesDir)
        self.filesTree.setRootIndex(self.filesModel.index(self.filesDir))
        self.filesTree.clearSelection()
    
    def copyPath(self):
        cb = QGuiApplication.clipboard()
        cb.clear(cb.Mode.Clipboard)
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                if self.filesModel.isDir(index):
                    filePath = self.filesModel.filePath(index)
                    cb.setText(filePath)
                else:
                    cb.setText(self.txtFilePath.text()) 
            else:
                cb.setText(self.txtFilePath.text())
        else:
            cb.setText(self.txtFilePath.text())
    
    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()
    
    # def document_copy(self):
    #     if self.filesTree.selectionModel().hasSelection():
    #         index = self.filesTree.selectionModel().selectedIndexes()[0]
    #         if index:
    #             filePath = self.filesModel.filePath(index)
    #             cb = qtg.QGuiApplication.clipboard()
    #             cb.clear(cb.Mode.Clipboard)
    #             cb.setObjectName(filePath)
    
    def selection_clear(self):
        self.filesTree.clearSelection()
    
    
    def folderOpen(self):
        try:
            os.startfile(self.filesDir)
        except FileNotFoundError:
            os.startfile(self.root)
        except:
            print('Folder not found')

    def file_open(self):
        self.filesModel.setReadOnly(True)
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                filePath = self.filesModel.filePath(index)
                try:
                    os.startfile(filePath)
                except FileNotFoundError:
                    print('File not found')   
        else: 
            try:
                os.startfile(self.filesDir)
            except FileNotFoundError:
                os.startfile(self.root)
            except:
                print('File not found')
        self.filesModel.setReadOnly(False)

    def new_folder(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if self.filesModel.isDir(index):
                self.filesModel.mkdir(index,'New Folder') 
            else:
                index = self.filesModel.index(self.filesDir)
                if index:
                    self.filesModel.mkdir(index,'New Folder') 
        
        else: 
            index = self.filesModel.index(self.filesDir)
            if index:
                self.filesModel.mkdir(index,'New Folder') 

    def file_delete(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            fileName = index.data()
        
            warning_box = QMessageBox()
            warning_box.setWindowTitle('Elmininar archivo')
            warning_box.setWindowIcon(self.iconAVD)
            warning_box.setText(f'''Advertencia, está a punto de eliminar el archivo: {fileName}''')
            warning_box.setInformativeText('Desea continuar?')
            
            warning_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            warning_box.setIcon(QMessageBox.Icon.Warning)
            button = warning_box.exec()

            if button == QMessageBox.StandardButton.Yes:
                self.filesModel.remove(index)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = treeviewSearchBox()
    mw.show()
    sys.exit(app.exec())
