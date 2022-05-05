from globalElements import constants
from globalElements.widgets import labelWidget,cboFilterGroup
from globalElements.accounts import main as accounts
import os
import pathlib
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

class main(accounts.main):
    def __init__(self):
        super().__init__()
        # self.btn_cerrar.deleteLater()
        self.family = []
        self.root = f'{constants.oneDrive}\Personal'
        self.filesFolder.root = self.root
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.configure_list()
        self.title.setText('Personal Accounts')
        self.requery()

    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        member = self.familyFilter.getInfo()
        if member:
            self.db.dbFolder = f'{self.root}\{member}'
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

    
    def queryFamily(self):
        with os.scandir(self.root) as rootfolder:
            for member in rootfolder:
                if member.is_dir():
                    self.family.append(member.name)

    def configure_list(self):
        self.listFontSize = 13
        filterSize = 13
        self.queryFamily()
        self.familyFilter = cboFilterGroup(self.fontSize,
            items = self.family,
            requeryFunc = self.queryFamily,
            refreshable = False)

        self.list.layoutFilter.insertRow(0, labelWidget('Miembro:', filterSize), self.familyFilter)
        self.familyFilter.cbo.currentIndexChanged.connect(self.requery)
    
    def btn_cerrar_pressed(self):
        os._exit(0)

    def setFilesFolder(self):
        member = self.familyFilter.cbo.currentText()
        account = self.account.text()
        if member and account:
            folderPath = f'{self.filesFolder.root}\{member}\{account}'
            self.filesFolder.txtFilePath.setText(folderPath)
            folder = pathlib.Path(folderPath)
            if not folder.exists():
                os.mkdir(folderPath)
                self.filesFolder.txtFilePath.setText('folderPath')
                self.filesFolder.txtFilePath.setText(folderPath)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)
