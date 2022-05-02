#!/usr/bin/python3

from globalElements import DB, constants, mainModel
from globalElements.widgets import checkBox, dateEdit, dateWidget, incomeExpenseRadioButtons, labelWidget,  lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox, lineEditPhone, truFalseRadioButtons
from globalElements.zipsWidget import mainUs as UsZipsWidget
import sys
import os
import pathlib
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 

locale.setlocale(locale.LC_ALL,"")
from decimal import *


class main(mainModel.main):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.configure_form()
        self.setConnections()
        self.requery()
        
    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'clients'
        self.listTableValuesIndexes = (0,4,8,10,1,2,11,3,5,9)
        # self.formToDBItems = 4
        self.titleText = "BOOKKEEPING"
        self.listWidth = 1
        self.formWidth = 1
        self.listHiddenItems = ()#(4,5,6,7,8,9,10,11,12)
        self.listColumnWidth = ((0,60),(1,280),(2,130),(3,130))
        self.sortColumn = 1
        self.onNewFocusWidget = 1
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        sqlFiles = 'avdt\\bookkeeping'
        self.selectFile = f'{sqlFiles}\selectAll.sql'
        self.newRecordSql = f'{sqlFiles}\insertNewRecord.sql'
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idCarrier = '{record[1]}', 
                idCategoriemc = '{record[2]}',
                account_ = '{record[3]}',
                date_ = '{record[4]}',
                amount = '{record[5]}',
                isIncome = '{record[6]}',
                description_ = '{record[7]}',
                anexo = '{record[8]}',
                isBusiness = '{record[9]}',
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
            name = self.name.getInfo()
            

            text = f'''Eliminar el registro:
            id: {idVar} 
            Cliente: {name}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutSideFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.setLineEditFileBox(self.fontSize)
        self.filesFolder.root = f'{constants.rootAVDT}\Carriers'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)

        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        if not constants.carriersList:
            constants.queryCarriers()
        self.carrier = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.carriersDict,
            requeryFunc=constants.queryCarriers,
            clearFilter=False) 
        
        if not constants.bookkeepingTruckingCategoriesList:
            constants.querybookkeepingTruckingCategories()
        self.categorie = cboFilterGroup(self.fontSize, 
            refreshable=True,
            items=constants.bookkeepingTruckingCategoriesDict,
            requeryFunc=constants.querybookkeepingTruckingCategories,
            clearFilter=False) 

        self.account = lineEdit(self.fontSize)

        self.date_ = dateWidget(self.fontSize)
        self.amount = lineEditCurrency(self.fontSize)
        self.isIncome = incomeExpenseRadioButtons(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.isBusiness = truFalseRadioButtons(self.fontSize)

        self.anexoBox = self.filesFolder.layoutLineEditFileBox
        self.anexo = self.filesFolder.lineEditItems.txt



        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, 
            self.carrier, 
            self.categorie, 
            self.account, 
            self.date_, 
            self.amount,
            self.isIncome, 
            self.description, 
            self.anexo, 
            self.isBusiness]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.insertRow(3,self.anexoBox)
        # self.layoutForm.addRow(self.isBusiness)
        self.layoutForm.addRow(labelWidget('Business?:', self.fontSize,True, "Blue"), self.isBusiness)
        
        self.layoutForm.addRow(labelWidget('Carrier:', self.fontSize), self.carrier)
        self.layoutForm.addRow(labelWidget('Account:', self.fontSize), self.account)
        self.layoutForm.addRow(labelWidget('Category:', self.fontSize), self.categorie)
        
        self.layoutForm.addRow(labelWidget('Date:', self.fontSize), self.date_)
        self.layoutForm.addRow(labelWidget('Amount:', self.fontSize), self.amount)
        self.layoutForm.addRow(labelWidget('Type:', self.fontSize), self.isIncome)
        
        self.layoutForm.addRow(labelWidget('Notes', 14,True, "Black", "center"))
        self.layoutForm.addRow(self.description)
        

    def setConnections(self):
        # self.carrierFilter.cbo.currentIndexChanged.connect(self.carrierFilterAfterUpdate)
        # self.list.proxyModel.dataChanged.connect(self.setTotals)
        # self.list.proxyModel.rowsInserted.connect(self.setTotals)
        # self.list.proxyModel.rowsRemoved.connect(self.setTotals) 
        # self.setTotalsOpt.stateChanged.connect(self.setTotals)
        #g! SET FILTER CONNECTIONS
        # self.yearFilter.cbo.currentTextChanged.connect(self.yearFilterApply)
        # self.monthFilter.cbo.currentTextChanged.connect(self.monthFilterApply)
        # self.categoriesFilter.cbo.currentTextChanged.connect(self.categorieFilterApply)
        # self.businessFilter.true.toggled.connect(self.businessFilterApply)
        # self.businessFilter.false.toggled.connect(self.businessFilterApply)
        # self.accountFilter.cbo.currentTextChanged.connect(self.accountFilterApply)
        # self.incomeExpenseFilter.income.toggled.connect(self.incomeExpenseFilterApply)
        # self.incomeExpenseFilter.expense.toggled.connect(self.incomeExpenseFilterApply)
         #g! FORM Connections
        #The values we need, are the ones corresponding to the table. 
        #first formDirty parameter is the index corresponding to the table value
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.carrier.cbo.currentIndexChanged.connect(lambda: self.formDirty(1,self.carrier.getDbInfo()))
        self.categorie.cbo.currentIndexChanged.connect(lambda: self.formDirty(2,self.categorie.getInfo())) 
        self.categorie.cbo.currentTextChanged.connect(lambda: self.formDirty(2,self.categorie.getInfo))
        # self.account.cbo.currentIndexChanged.connect(lambda: self.formDirty(3,self.account.cbo.getInfo()))
        self.date_.dateEdit.dateChanged.connect(lambda: self.formDirty(4, self.date_.getInfo()))
        self.amount.textChanged.connect(lambda:self.formDirty(5,self.amount.getInfo()))
        self.isIncome.income.toggled.connect(lambda: self.formDirty(6, self.isIncome.getInfo()))
        # self.isIncome.false.hitButton.connect(lambda: self.formDirty(6, self.isIncome.getInfo()))
        self.description.textChanged.connect(lambda: self.formDirty(7, self.description.getInfo()))
        self.anexo.textChanged.connect(lambda: self.formDirty(8,self.anexo.getInfo()))
        self.isBusiness.true.toggled.connect(lambda: self.formDirty(9,self.isBusiness.getInfo()))

    def getListInfo(self):
        i0 = self.id_.getInfo()
        i1 = self.date_.getInfo()
        i2 = self.amount.getInfo()
        i3 = self.description.getInfo()
        i4 = str(self.carrier.getDbInfo())
        i5 = self.anexo.getInfo()
        i6 = str(self.date_.dateEdit.date().year()) 
        i7 = str(self.date_.dateEdit.date().toString('MM'))
        i8 = self.categorie.getInfo()
        i9 = self.isBusiness.getInfo()
        i10 = self.account.getInfo()
        i11 = self.isIncome.getInfo()
        record = ([i0, i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11])
        return record
    
    
    def setFilesFolder(self):
        carrier = self.carrier.cbo.currentText()
        month = self.date_.dateEdit.date().toString('MM')
        year = self.date_.dateEdit.date().toString('yyyy')
        isIncome = self.isIncome.getInfo()
        
        folderPath = self.filesFolder.root
        if not carrier:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        else:
            folderPath = f'{self.filesFolder.root}\{carrier}\Accounting\{year}'
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
            if isIncome == "Income":
                folderPath = f'{folderPath}\Income'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
                folderPath = f'{folderPath}\{month}'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
                 
            else:
                folderPath = f'{folderPath}\Expenses'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
                folderPath = f'{folderPath}\{month}'
                folder = pathlib.Path(folderPath)
                if not folder.exists():
                    os.mkdir(folderPath)
        self.filesFolder.txtFilePath.setText(folderPath)

    


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())