from globalElements import constants
from globalElements.widgets import labelWidget,cboFilterGroup
from globalElements.accounts import main as accounts
# from localDB import mainModel
# from globalElements.widgets import (lineEditCopy, webWidget, dateWidget, 
#     labelWidget,  textEdit, lineEdit, cboFilterGroup)
# import pathlib
import os
import pathlib
# from localDB import sqliteDB
# from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
# from globalElements import DB as mysqlDb
from PyQt6.QtWidgets import QApplication
# from avdt.accounts import main  


class main(accounts.main):
    def __init__(self):
        super().__init__()
        self.filesFolder.root = f'{constants.rootEnlace}\Clients'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.configure_list()
        self.requery()

    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        client = self.clientFiltros.getInfo()
        if client:
            self.db.dbFolder = f'{constants.rootEnlace}\clients\{client}\Accounts'
            try:
                records = self.selectAll()
            except:
                sql = self.db.getSQL('createTable.sql')
                self.db.executeQuery(sql)
                records = self.selectAll()

            if records:
                self.list.requery(records, self.listFontSize, self.rowHeight, "Black")
                self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
            else:
                self.list.removeAllRows()
            self.configureColumns()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()

    def configure_list(self):
        self.listFontSize = 13
        filterSize = 13
        self.clientFiltros = cboFilterGroup(self.fontSize,
            refreshable=False)
        self.clientFiltros.cbo.addItem('Enlace')

        self.list.layoutFilter.insertRow(0, labelWidget('Client:', filterSize), self.clientFiltros)
        
        self.clientFiltros.cbo.currentIndexChanged.connect(self.requery)


    # def btn_delete_pressed(self):
    #     record = self.list.treeview.selectionModel().selectedIndexes()
    #     #Verificar si hay registro seleccionado
    #     if record:
    #         idVar = self.id_.text()
    #         carrier = self.clientFiltros.getInfo()
    #         account = self.account.getInfo()
    #         text = f'''Eliminar el registro:
    #         id: {idVar} 
    #         Carrier: {carrier}
    #         Account.: {account}
    #         '''
    #         self.deleteRecord(text)
    #     else:
    #         self.clearForm()
        
    # def configure_form(self): 
    #     self.formLayoutSideFilesTree()
    #     self.layoutFormBox.setMinimumWidth(450)
    #     self.layoutFormBox.setMaximumWidth(500)
    #     self.setFormElements()


    def setFilesFolder(self):
        client = self.clientFiltros.cbo.currentText()
        account = self.account.text()
        if client and account:
            folderPath = f'{self.filesFolder.root}/{client}/Accounts/{account}'
            self.filesFolder.txtFilePath.setText(folderPath)
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
                self.filesFolder.txtFilePath.setText('folderPath')
                self.filesFolder.txtFilePath.setText(folderPath)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
