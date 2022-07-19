#!/usr/bin/python3
# setup.load()  
import sys 
from globalElements import constants

from personal import menu, accounts, bills
# from avdt.accounts import main as accounts
from globalElements.widgets import tabWidget
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt6.QtGui import QIcon
# from enlace.traducciones import procedencia


class MainWindow(QMainWindow): 
    def __init__(self):  
        super().__init__()
        self.initUi()
        self.layoutConfig()
        self.configureMenu()
        self.showMaximized()


    def initUi(self):
        self.setWindowTitle('ENLACE LLC')
        self.iconEnlace = QIcon( f'{constants.othFolder}\icons\enlace.png')
        self.setWindowIcon(self.iconEnlace)

    def layoutConfig(self):
        self.mainMenu = QWidget()
        self.mainMenuLayout = QVBoxLayout()
        self.mainMenuLayout.setSpacing(0)
        self.mainMenuLayout.setContentsMargins(0,0,0,0)
        self.mainMenu.setLayout(self.mainMenuLayout)

        self.tabWidget = tabWidget("h1")
        self.tabWidget.addTab(self.mainMenu, 'Main Menu')
        
        self.setCentralWidget(self.tabWidget)

# ENLACE 
#------------------------------------------------------------------------
    def configureMenu(self):
        self.menu = menu.main()
        self.mainMenuLayout.addWidget(self.menu, 1)
        self.configureConnections()

    def configureConnections(self):
        self.menu.btnAccounts.pressed.connect(self.openAccounts)
        self.menu.btnBills.pressed.connect(self.openBills)

    def openAccounts(self):
        self.accounts = accounts.main()
        self.tabWidget.addTab(self.accounts, '    ACCOUNTS    ')
        self.tabWidget.setCurrentWidget(self.accounts)

    def openBills(self):
        self.bills = bills.main()
        self.tabWidget.addTab(self.bills, '    BILLS    ')
        self.tabWidget.setCurrentWidget(self.bills)
    
   

# OTHER FUNCTIONS
# _______________________________________________________________________________________
    # def otherConnections(self):
    #     self.juicios.mainList.treeview.selectionModel().selectionChanged.connect(self.updateJuiciosTab)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec()) 