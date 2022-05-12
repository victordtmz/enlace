#!/usr/bin/python3
from decimal import Decimal
import re
from avdt import bookkeeping_
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from globalElements.widgets import checkBox, spacer

class addForm(bookkeeping_.main):
    def __init__(self):
        super().__init__()
        self.detailsBox.deleteLater()
        self.listOpt.deleteLater()
        self.formOpt.deleteLater()
        self.btnDelete.deleteLater()
        self.title.deleteLater()
        self.btn_cerrar.deleteLater()
        self.titleLayoutBox.setMinimumHeight(50)
        self.btnNew.setText('Agregar a este viaje')

    def listadoSelectionChanged(self):
        # if self.list.treeview.selectionModel().hasSelection():
        return

    def setSizes(self):
        self.size_ = "h2"

    def btn_nuevo_pressed(self):
        pass
    
    def carrierFilterAfterUpdate(self):
        pass


class main(bookkeeping_.main):
    def __init__(self):
        super().__init__()
        self.btnNew.deleteLater()
        self.list.layoutFilter.removeRow(0)
        self.list.layoutFilter.removeRow(0)
        # self.carrierFilter.deleteLater()
        # self.yearFilter.deleteLater()

        self.addForm = False
        self.filesFolder.setMaximumHeight(300)
        self.filesFolder.setMinimumHeight(300)
        self.layoutForm.addRow(self.filesFolder)

        self.addFormOpt = checkBox('Agregar Elementos',fontSize=self.fontSize, size=self.mainSize)
        self.widgetsOpt.append(self.addFormOpt)
        self.addFormOpt.toggled.connect(self.displayAddForm)
        # self.titleLayout.addWidget(self.addFormOpt)

        
        self.widgetsOptSizes.append(1)#size proportion
        self.spacer3 = spacer('     ', self.formSize)
        self.titleLayout.insertWidget(3, self.spacer3)
        self.titleLayout.insertWidget(4, self.addFormOpt)

    

    def setSizes(self):
        self.size_ = "h2"
    
    def mutableVariables(self):
       # DB INFO
        self.idLoad = 0
        self.idCarrier = 0
        
        
        # self.mainSize = 'h2'
        self.layoutVar = self.formLayoutStraightFilesTree
        # self.titleText = "BOOKKEEPING"
        # self.widgetsOptSizes = [1,1]
        # self.listHiddenItems = (4,5,6,7,8,9,10)
        # self.listColumnWidth = ((1,100),(2,100),(3,300) )
        # self.sortColumn = 1
        # self.onNewFocusWidget = 1
        # self.evaluateSaveIndex = (1,3,5)
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
                JOIN loads_bookkeeping ON loads_bookkeeping.idBookkeeping = bookkeeping.id
                WHERE bookkeeping.idCarrier = %s
                AND loads_bookkeeping.idLoads = %s
                ;'''

    def requery(self): 
        if self.idCarrier and self.idLoad:
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
            records = self.selectAll((self.idCarrier, self.idLoad))# will pass the cbo value - should be 
            self.list.requeryColorAccounting(records, 
                isIncomeColumn=10,isBusinessColumn= 8, sizeVar=self.listFontSize, rowHeight= self.rowHeight)
            while QApplication.overrideCursor() is not None:
                QApplication.restoreOverrideCursor()
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
            # self.monthFilterApply()
        else:
            self.list.removeAllRows()
        self.configureColumns()

    def displayAddForm(self):
        if not self.addForm:
            #Create instance of add form
            self.addForm = addForm()
            self.addForm.btnNew.pressed.connect(self.btnAddPressed)
            # set the id values esential for requery
            # self.addForm.idLoad = self.idLoad
            # set all form elements for this load
            # self.addForm.requery()
            #place on splitter
            self.splitter.addWidget(self.addForm)
            #set connections to this item
            # self.addForm.btnAdd.pressed.connect(self.addMilesLoad)
            self.configureWidth()
        else:
            self.addForm.deleteLater()
            self.addForm = False


    
    def btnAddPressed(self):
        if self.idLoad:
            if self.addForm.list.treeview.selectionModel().hasSelection():
                indexes = self.addForm.list.treeview.selectionModel().selectedIndexes()
                idBookkeeping = indexes[0].data()#
                if idBookkeeping:
                    sql = f'''INSERT IGNORE INTO 
                    loads_bookkeeping (idBookkeeping, idLoads) 
                    VALUES ({idBookkeeping}, {self.idLoad})'''
                    self.db.run_sql_commit(sql)
                    self.requery()
                    if self.setTotalsOpt.isChecked():
                        self.setTotals()
                    
    def btn_delete_pressed(self):
        if self.idLoad:
            if self.list.treeview.selectionModel().hasSelection():
                indexes = self.list.treeview.selectionModel().selectedIndexes()
                idBookkeeping = indexes[0].data()#
                if idBookkeeping:
                    sql = f'''DELETE FROM loads_bookkeeping 
                    WHERE idBookkeeping = {idBookkeeping}
                    AND idLoads = {self.idLoad};'''
                    self.db.run_sql_commit(sql)
                    self.requery()
                    if self.setTotalsOpt.isChecked():
                        self.setTotals() 

            else:
                self.clearForm()

    def calculateTotals(self):
        amounts = self.list.getColumnValues((2,10,8))#8 is business True/False
        # total = Decimal('0.00') 
        incomes = Decimal('0.00') 
        expenses = Decimal('0.00') 
        if amounts:
            for i in amounts:
                if i[2] == 'True':
                    if i[1] == "Expense":
                        expenses += Decimal(re.sub(r"[^\d.]","", i[0]))
                    elif i[1] == "Income":
                        incomes += Decimal(re.sub(r"[^\d.]","", i[0]))
                
            return incomes, expenses
        