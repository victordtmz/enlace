#!/usr/bin/python3
from avdt.loads import loads
from globalElements import setup 
# setup.load()  
import sys 
from globalElements import constants
from enlace.accounts import main as enlaceAccounts
from avdt import (avdt, bookkeeping_, carriers, clients_, drivers, trucks, trailers, stops, accounts, diesel,
    bookkeeping_categories, miles, IFTA, loads_payments, bookkeeping_totals)
from enlace import enlace, juicios, servicios, traducciones
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
        self.configureEnlace()
        self.configureAVDT() 
        self.showMaximized()
        # self.otherConnections()


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
        self.enlaceMenu.btnJuicios.pressed.connect(self.openJuicios)
        self.enlaceMenu.btnServicios.pressed.connect(self.openServicios)
        self.enlaceMenu.btnTranslate.pressed.connect(self.openTraducciones)

    def enlaceOpenAccounts(self):
        self.enlaceAccounts = enlaceAccounts.main()
        self.tabWidget.addTab(self.enlaceAccounts,'    ENLACE ACCOUNTS   ')
        self.tabWidget.setCurrentWidget(self.enlaceAccounts)

    def openJuicios(self):
        self.juicios = juicios.main()
        self.tabWidget.addTab(self.juicios,'    JUICIOS   ')
        self.tabWidget.setCurrentWidget(self.juicios)
        self.juicios.mainList.treeview.selectionModel().selectionChanged.connect(self.updateJuiciosTab)

    def openServicios(self):
        self.servicios = servicios.main()
        self.tabWidget.addTab(self.servicios,'    SERVICIOS   ')
        self.tabWidget.setCurrentWidget(self.servicios)
        self.servicios.mainList.treeview.selectionModel().selectionChanged.connect(self.updateServicosTab)

    def openTraducciones(self):
        self.traducciones = traducciones.main()
        self.tabWidget.addTab(self.traducciones,'    TRADUCCIONES   ')
        self.tabWidget.setCurrentWidget(self.traducciones)
    
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
        self.avdtMenu.btnAvdtTrailers.pressed.connect(self.avdtOpenTrailers)
        self.avdtMenu.btnAvdtCarriers.pressed.connect(self.avdtOpenCarriers)
        self.avdtMenu.btnAvdtClients.pressed.connect(self.avdtOpenClients)
        self.avdtMenu.btnAvdtStops.pressed.connect(self.avdtOpenStops)
        self.avdtMenu.btnAvdtBookkeeping.pressed.connect(self.avdtOpenBookkeeping)
        self.avdtMenu.btnAvdtBookkeepingCategories.pressed.connect(self.avdtOpenBookkeepingCat)
        self.avdtMenu.btnAvdtDiesel.pressed.connect(self.avdtOpenDiesel)
        self.avdtMenu.btnAvdtMiles.pressed.connect(self.avdtOpenMiles)
        self.avdtMenu.btnAvdtIfta.pressed.connect(self.avdtOpenIfta)
        self.avdtMenu.btnAvdtLoadPayments.pressed.connect(self.avdtOpenLoadsPayments)
        self.avdtMenu.btnAvdtBookkeepingTotals.pressed.connect(self.avdtOpenBookkeepingTotals)

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

    def avdtOpenTrailers(self):
        self.avdtTrailers = trailers.main()
        self.tabWidget.addTab(self.avdtTrailers,'    AVDT TRAILERS   ')
        self.tabWidget.setCurrentWidget(self.avdtTrailers)

    def avdtOpenCarriers(self):
        self.avdtCarriers = carriers.main()
        self.tabWidget.addTab(self.avdtCarriers,'    AVDT CARRIERS   ')
        self.tabWidget.setCurrentWidget(self.avdtCarriers)

    def avdtOpenClients(self):
        self.avdtClients = clients_.main()
        self.tabWidget.addTab(self.avdtClients,'    AVDT CLIENTS   ')
        self.tabWidget.setCurrentWidget(self.avdtClients)

    def avdtOpenStops(self):
        self.avdtStops = stops.main()
        self.tabWidget.addTab(self.avdtStops,'    AVDT WAREHOUSES   ')
        self.tabWidget.setCurrentWidget(self.avdtStops)

    def avdtOpenBookkeeping(self): 
        self.avdtBookkeeping = bookkeeping_.main()
        self.tabWidget.addTab(self.avdtBookkeeping,'    AVDT BOOKKEEPING   ')
        self.tabWidget.setCurrentWidget(self.avdtBookkeeping) 

    def avdtOpenBookkeepingCat(self):
        self.avdtBookkeepingCat = bookkeeping_categories.main()
        self.tabWidget.addTab(self.avdtBookkeepingCat,'    AVDT BOOKKEEPING CATEGORIES   ')
        self.tabWidget.setCurrentWidget(self.avdtBookkeepingCat)

    def avdtOpenDiesel(self): 
        self.avdtDiesel = diesel.main()
        self.tabWidget.addTab(self.avdtDiesel,'    AVDT DIESEL   ')
        self.tabWidget.setCurrentWidget(self.avdtDiesel)

    def avdtOpenMiles(self):
        self.avdtMiles = miles.main()
        self.tabWidget.addTab(self.avdtMiles,'    AVDT MILES   ')
        self.tabWidget.setCurrentWidget(self.avdtMiles)

    def avdtOpenIfta(self):
        self.avdtIfta = IFTA.main()
        self.tabWidget.addTab(self.avdtIfta,'    AVDT IFTA   ')
        self.tabWidget.setCurrentWidget(self.avdtIfta)

    def avdtOpenLoadsPayments(self):
        self.avdtLoadsPayments = loads_payments.main()
        self.tabWidget.addTab(self.avdtLoadsPayments,'    AVDT LOADS PAYMENTS   ')
        self.tabWidget.setCurrentWidget(self.avdtLoadsPayments)

    def avdtOpenBookkeepingTotals(self):
        self.avdtBookkeepingTotals = bookkeeping_totals.main()
        self.tabWidget.addTab(self.avdtBookkeepingTotals,'    AVDT BOOKKEEPING TOTALS   ')
        self.tabWidget.setCurrentWidget(self.avdtBookkeepingTotals)

# OTHER FUNCTIONS
# _______________________________________________________________________________________
    # def otherConnections(self):
    #     self.juicios.mainList.treeview.selectionModel().selectionChanged.connect(self.updateJuiciosTab)

    def updateJuiciosTab(self):
        listIndex = self.juicios.mainList.treeview.selectionModel().selectedIndexes()
        expediente = listIndex[1].data()
        # self.juicios.title.text()
        tabIndex = self.tabWidget.currentIndex()
        # try:
        self.tabWidget.setTabText(tabIndex, expediente)
        # except:
        #     pass

    def updateServicosTab(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.setTabText(index, self.servicios.title.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec()) 