#!/usr/bin/python3
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
from globalElements import constants, DB, modelMain, modelList
from globalElements.widgets import labelWidget, lineEditCurrency, textEdit, lineEdit, cboFilterGroup, spinbox
import locale 
locale.setlocale(locale.LC_ALL,"")
from decimal import *

class main(modelMain.main):
    def __init__(self):
        super().__init__()
        
        # set addForm to False - this will be the widget to add records to the current load
        self.addForm = False
        self.initUi()
        self.configure_form()
        self.setConnections()
        # self.setTotalsElements()
        self.requery()
        
        # self.getIdLoad()

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h2"
        self.idLoad = 0
        self.idColumn = 'idLoad' 
        self.tableVar = 'AVDT_Loads_Invoice'
        self.sqlFolderName = "AVDT_loads_invoice"
        self.listTableValuesIndexes = (0,1,2,3,4,5)
        # self.formToDBItems = 4
        self.titleText = "Invoice Items"
        self.listWidth = 1
        self.formWidth = 1
        self.listHiddenItems = (0,1,5)
        self.listColumnWidth = ((2,40),(3,150),(4,110))
        self.sortColumn = 2
        self.onNewFocusWidget = 2

    def updateRecord(self, record): 
        '''record is passed as a tuple with id'''
        sql =f'''UPDATE {self.tableVar} SET 
                idLoad = '{record[1]}',
                no_ = '{record[2]}',
                item = '{record[3]}',
                amount = '{record[3]}',
                notes = '{record[3]}'
                WHERE id =  {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        # Query will execute where idCarrier = carrier, all other filters applied locally
        if self.idLoad:
            qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
            records = self.selectAll((self.idLoad,))# will pass the cbo value - should be 
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
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
            item = self.item.getInfo()

            text = f'''Eliminar el registro:
            id: {idVar} 
            No.: {no_}
            Item: {item}
            '''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutStraight()
        self.layoutFormBox.setMinimumWidth(350)
        self.layoutFormBox.setMaximumWidth(400)

        self.setFormElements()

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)

        self.idLoad_ = lineEdit(self.fontSize)
        self.idLoad_.setReadOnly(True)
 
        self.no_ = spinbox(self.fontSize)
        self.no_.setMinimum(1)

        self.item = cboFilterGroup(
            self.fontSize, 
            refreshable=False, 
            items= ["", "Line haul", "Detention", "Layover", "Lumper"],
            clearFilter=False
        )

        self.amount = lineEditCurrency(self.fontSize)
        self.notes = textEdit(self.fontSize)


        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [
            self.id_, 
            self.idLoad_,
            self.no_,
            self.item, 
            self.amount,
            self.notes]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('IdLoad:', self.fontSize), self.idLoad_)
        self.layoutForm.addRow(labelWidget('No.:', self.fontSize), self.no_)
        self.layoutForm.addRow(labelWidget('Item:', self.fontSize), self.item)
        self.layoutForm.addRow(labelWidget('Amount:', self.fontSize), self.amount)
        self.layoutForm.addRow(labelWidget("Notes", 14, fontColor="Blue", align="center"))
        self.layoutForm.addRow(self.notes)
        

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.idLoad_.textChanged.connect(lambda: self.formDirty(1,self.idLoad_.getInfo()))
        self.no_.textChanged.connect(lambda: self.formDirty(2, self.no_.getInfo))
        self.item.cbo.currentTextChanged.connect(lambda: self.formDirty(3, self.item.getInfo))
        self.amount.textChanged.connect(lambda: self.formDirty(4, self.amount.getInfo))
        self.notes.textChanged.connect(lambda: self.formDirty(5, self.notes.getInfo()))
        self.btnNew.pressed.connect(self.createNewRecord)

    def createNewRecord(self):
        if self.idLoad:
            self.idLoad_.setText(str(self.idLoad))


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())