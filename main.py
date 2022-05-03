#!/usr/bin/python3
from globalElements.setup import load
load()
import sys
from PyQt6.QtWidgets import (QWidget,QMainWindow,QHBoxLayout,
    QVBoxLayout, QGridLayout, QApplication)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from globalElements import constants
from globalElements.widgets import tabWidget
from avdt import avdt
from avdt.loads import loads
from avdt.accounts import main as accounts

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.initUi()
        self.layoutConfig()
        self.configureAVDT()
        


    def initUi(self):
        self.setWindowTitle('ENLACE LLC')
        self.iconEnlace = QIcon( f'{constants.othFolder}\icons\enlace.png')
        self.setWindowIcon(self.iconEnlace)

    def layoutConfig(self):
        self.mainMenu = QWidget()
        self.mainMenuLayout = QVBoxLayout()
        self.mainMenuLayout.setContentsMargins(0,0,0,0)
        self.mainMenu.setLayout(self.mainMenuLayout)

        self.tabWidget = tabWidget("h1")
        self.tabWidget.addTab(self.mainMenu, 'Main Menu')
        
        self.setCentralWidget(self.tabWidget)

    def configureAVDT(self):
        self.avdtMenu = avdt.main()
        self.mainMenuLayout.addWidget(self.avdtMenu)
        self.configAVDTConnections()

    def configAVDTConnections(self):
        self.avdtMenu.btnAvdtLoads.pressed.connect(self.avdtLoadsOpen)
        self.avdtMenu.btnAvdtAccounts.pressed.connect(self.avdtAccountsOpen)
#AVDT 
#------------------------------------------------------------------------
    def avdtLoadsOpen(self):
        self.avdtLoads = loads.main()
        self.tabWidget.addTab(self.avdtLoads,'       AVDT LOADS      ')
        self.tabWidget.setCurrentWidget(self.avdtLoads)

    def avdtAccountsOpen(self):
        self.avdtAccounts = accounts.main()
        self.tabWidget.addTab(self.avdtAccounts,'    AVDT ACCOUNTS   ')
        self.tabWidget.setCurrentWidget(self.avdtAccounts)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())