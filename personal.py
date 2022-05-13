from globalElements.setup import load
load()
from globalElements import constants, accounts
from globalElements.widgets import labelWidget,cboFilterGroup
# from globalElements.accounts import accounts as accounts
import os
import sys
import pathlib
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QApplication

class main(accounts.main):
    def __init__(self):
        super().__init__()
        # self.listExpand = 1
        # self.formExpand = 1
        self.widgetsOptSizes = [1,1]
        # self.btn_cerrar.deleteLater()
        self.setProgramDetails()
        self.family = []
        self.root = f'{constants.oneDrive}\Personal'
        self.filesFolder.root = self.root
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        self.configure_list()
        self.title.setText('Personal Accounts')
        self.showMaximized()
        self.requery() 
    
    def setProgramDetails(self):
        self.setWindowTitle('FAMILY DOCS')
        self.iconEnlace = QIcon( f'{constants.othFolder}\icons\\family.png')
        self.setWindowIcon(self.iconEnlace)

    def requery(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        member = self.familyFilter.getInfo()
        if member:
            self.db.dbFolder = f'{self.root}\{member}\db'
            try:
                records = self.selectAll()
            except:
                # sql = self.db.getSQL('createTable.sql')
                folder = pathlib.Path(self.db.dbFolder)
                if not folder.exists():
                    os.mkdir(self.db.dbFolder)
                self.db.executeQuery(self.db.createTableSql)
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
            refreshable = True)

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
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())