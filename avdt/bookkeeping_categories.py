#!/usr/bin/python3

from globalElements import DB, constants, modelMain
from globalElements.widgets import labelWidget,   lineEdit, cboFilterGroup
import sys
from localDB.scheduleC.main import scheduleCbo
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 

locale.setlocale(locale.LC_ALL,"")
from decimal import *

class main(modelMain.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configure_form()
        self.setConnections()
        # self.setTotalsElements()
        self.requery()
        
    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'bookkeeping_categories'
        self.listTableValuesIndexes = (0,1,2,3)
        # self.formToDBItems = 4
        self.titleText = "BOOKKEEPING CATEGORIES"
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        self.listHiddenItems = (3,)
        self.listColumnWidth = ((0,60),(1,100),(2,260))
        self.sortColumn = 2
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.selectSql = '''
            SELECT 
                id, 
                scheduleC AS "Schedule C",
                categorie AS "Categorie",
                industry AS "Industry"
                FROM bookkeeping_categories;'''
        self.newRecordSql = '''
            INSERT INTO bookkeeping_categories (scheduleC, categorie, industry) VALUES'''
        
    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                scheduleC = '{record[1]}',
                categorie = '{record[2]}',
                industry = '{record[3]}'
                WHERE id =  {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        records = self.selectAll()
        if records:
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
        else:
            self.list.removeAllRows()
        
        self.configureColumns()
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        
    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.text()
            categorie = self.categorie.getInfo()
            text = f'''Eliminar el registro:
            id: {idVar} 
            Categorie: {categorie}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(550)
        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        self.scheduleC = scheduleCbo(self.fontSize)
        
        self.categorie = lineEdit(self.fontSize)
        
        if not constants.bookkeepingTruckingIndustries:
            constants.querybookkeepingTruckingIndustries()
        self.industry = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.bookkeepingTruckingIndustries,
            requeryFunc=constants.querybookkeepingTruckingIndustries,
            clearFilter=False) 

        self.formItems = [self.id_, self.scheduleC,self.categorie, self.industry]

        self.schedulCInfo = labelWidget('',self.fontSize)
        self.schedulCInfo.setWordWrap(True)
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Schedule C:', self.fontSize),self.scheduleC)
        self.layoutForm.addRow(labelWidget('Categorie:', self.fontSize),self.categorie)
        self.layoutForm.addRow(labelWidget('Industry:', self.fontSize), self.industry)
        self.layoutForm.addRow(self.schedulCInfo)
        
    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.scheduleC.currentIndexChanged.connect(self.setScheduleCLabel)
        self.categorie.textChanged.connect(lambda: self.formDirty(2,self.categorie.getInfo()))
        self.industry.cbo.currentTextChanged.connect(lambda: self.formDirty(3,self.industry.getInfo()))

    def setScheduleCLabel(self):
        self.scheduleC.populateCurrentValues()
        info = self.scheduleC.currentValues
        if info:
            txt = f'''
    Line: {info[0]}

    item: {info[1]}
        
    Español: {info[2]}
        
    Descripcion: {info[3]}
            '''
            self.schedulCInfo.setText(txt)
            self.formDirty(1,self.scheduleC.getInfo())

    def updateListRecord(self, record, selectionChanged):
        self.requery()
        #selection is lost on requery, select correct item!!
        if selectionChanged:
            # find the last i
            item = self.list.findItemFiltered(0, self.newSelectionId)
            index = self.list.proxyModel.index(item,0)
            self.list.treeview.setCurrentIndex(index)
        else:
            item = self.list.findItemFiltered(0, record[0])
            index = self.list.proxyModel.index(item,0)
            self.list.treeview.setCurrentIndex(index)

    def addListRecord(self,record,changedSelection):
        self.updateListRecord(record, changedSelection)# # self.list.addRecords((record,))
        

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())