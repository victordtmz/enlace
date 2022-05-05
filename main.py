#!/usr/bin/python3
from globalElements.setup import load
load()
import sys
 
#     tabWidget, enlace, enlaceAccounts, avdt, loads, accounts, drivers, trucks,
#     QApplication, sys)
from globalElements import constants
from enlace.accounts import main as enlaceAccounts
from avdt import avdt
from enlace import enlace
from avdt.loads import loads
from avdt.accounts import main as accounts
from avdt.drivers import main as drivers
from avdt.trucks import main as trucks
from globalElements.widgets import tabWidget
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
# from PyQt6.QtCore import Qicon
from PyQt6.QtGui import QIcon

  






class MainWindow(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.initUi()
        self.layoutConfig()
        self.configureEnlace()
        self.configureAVDT()
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
    def configureEnlace(self):
        self.enlaceMenu = enlace.main()
        self.mainMenuLayout.addWidget(self.enlaceMenu,1)
        self.configenlaceConnections()

    def configenlaceConnections(self):
        self.enlaceMenu.btnAccounts.pressed.connect(self.enlaceOpenAccounts)

    def enlaceOpenAccounts(self):
        self.enlaceAccounts = enlaceAccounts.main()
        self.tabWidget.addTab(self.enlaceAccounts,'    ENLACE ACCOUNTS   ')
        self.tabWidget.setCurrentWidget(self.enlaceAccounts)
    
#AVDT 
#------------------------------------------------------------------------
    def configureAVDT(self):
        self.avdtMenu = avdt.main()
        self.mainMenuLayout.addWidget(self.avdtMenu,2)
        self.configAVDTConnections()

    def configAVDTConnections(self):
        self.avdtMenu.btnAvdtLoads.pressed.connect(self.avdtOpenLoads)
        self.avdtMenu.btnAvdtAccounts.pressed.connect(self.avdtOpenAccounts)
        self.avdtMenu.btnAvdtDrivers.pressed.connect(self.avdtOpenDrivers)
        self.avdtMenu.btnAvdtTrucks.pressed.connect(self.avdtOpenTrucks)


    def avdtOpenLoads(self):
        self.avdtLoads = loads.main()
        self.tabWidget.addTab(self.avdtLoads,'       AVDT LOADS      ')
        self.tabWidget.setCurrentWidget(self.avdtLoads)

    def avdtOpenAccounts(self):
        self.avdtAccounts = accounts.main()
        self.tabWidget.addTab(self.avdtAccounts,'    AVDT ACCOUNTS   ')
        self.tabWidget.setCurrentWidget(self.avdtAccounts)

    def avdtOpenDrivers(self):
        self.avdtDrivers = drivers.main()
        self.tabWidget.addTab(self.avdtDrivers,'    AVDT DRIVERS   ')
        self.tabWidget.setCurrentWidget(self.avdtDrivers)

    def avdtOpenTrucks(self):
        self.avdtTrucks = trucks.main()
        self.tabWidget.addTab(self.avdtTrucks,'    AVDT TRUCKS   ')
        self.tabWidget.setCurrentWidget(self.avdtTrucks)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())