#!/usr/bin/python3
from globalElements import constants
from globalElements.widgets import buttonWidget, labelWidget
import sys
from PyQt6.QtWidgets import (QWidget,QMainWindow,QHBoxLayout,
    QVBoxLayout, QGridLayout, QApplication, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class blackSquare(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
            QWidget {
                background-color:#003365;
                };

            ''')#142,170,219 #84ABBE


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle('ENLACE LLC')
        
        self.initUi()
        self.setGridLayout()
        self.setCentralWidget(self.layoutMainBox)
        self.show()
    
    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     currWidth = self.width()
    #     currHeigh = self.height()
    #     # newWidth = 10
    #     if currWidth < 1100:
    #         newWidth = 10
    #     elif currWidth > 1101 and currWidth <1500:
    #         newWidth = 30
    #     else:
    #         newWidth = 50

    #     if currHeigh < 500:
    #         newHeight = 10
    #     elif currHeigh > 501 and currHeigh <1500:
    #         newHeight = 30
    #     else:
    #         newHeight = 50
        
    #     # print(f' Current width: {currWidth}')
    #     # print(f' Current Spacing: {newWidth}')

    #     # print(f' Current Height: {currHeigh}')
    #     # print(f' Current H Spacing: {newWidth}')
    #     self.layoutMainGrid.setHorizontalSpacing(newWidth)
    #     self.layoutMainGrid.setVerticalSpacing(newHeight)
    #     return super().resizeEvent(a0)

    def initUi(self):
        self.createAvdtItems()
        self.layoutMainBox = QWidget()
        self.setStyleSheet('''
            QMainWindow {
                background-color:#BEBEBE;
                };

            ''')
        
    def createAvdtItems(self):
        self.avdtTitle = labelWidget(
            text="TRUCKING DB", 
            fontSize=35,
            fontColor="white",
            align="center",
            backColor="#002142") 
        
        self.avdtLogo = labelWidget(
            align="center",
            backColor="#002142", 
            padding="6px") 
        self.imageSemi = QPixmap(f'{constants.othFolder}\icons\semi.png')
        self.imageSemi = self.imageSemi.scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio)
        self.avdtLogo.setPixmap(self.imageSemi)

        self.btnAvdtLoads = buttonWidget("    Loads", "main", icon=constants.iconTruck)
        self.btnAvdtLoadPayments = buttonWidget("    Load payments", "main", icon=constants.iconMoneyBag)
        self.btnAvdtClients = buttonWidget("    Clients", "main", icon=constants.iconClient)
        self.btnAvdtAccounts = buttonWidget("    Accounts", "main", icon=constants.iconAccounts)

        self.btnAvdtBookkeeping = buttonWidget("    Accounting", "main", icon=constants.iconAccounting)
        self.btnAvdtBookkeepingTotals = buttonWidget("    Accounting Totals", "main", icon=constants.iconMoneyBag)
        self.btnAvdtBookkeepingCategories = buttonWidget("    Categories", "main", icon=constants.iconCategories)
        self.btnAvdtDiesel = buttonWidget("    Diesel", "main", icon=constants.iconFuel)
        
        self.btnAvdtMiles = buttonWidget("    Miles", "main", icon=constants.iconRoad)
        self.btnAvdtStops = buttonWidget("    Warehouses", "main", icon=constants.iconWarehouse)
        self.btnAvdtIfta = buttonWidget("    IFTA", "main", icon=constants.iconIfta)

        self.btnAvdtCarriers = buttonWidget("    Carriers", "main", icon=constants.iconCarrier)
        self.btnAvdtDrivers = buttonWidget("    Drivers", "main", icon=constants.iconDriver)
        self.btnAvdtTrucks = buttonWidget("    Trucks", "main", icon=constants.iconTruck)
        self.btnAvdtTrailers = buttonWidget("    Trailers", "main", icon=constants.iconTrailer)

        # self.layoutTitleBox= QWidget()
        # self.layoutTitleBox.setMaximumHeight(100)
        # self.layoutTitle = QHBoxLayout() 
        # self.layoutTitle.setSpacing(0)
        # self.layoutTitle.setContentsMargins(0,0,0,0)
        # self.layoutTitle.addWidget(self.logo,1)
        # self.layoutTitle.addWidget(self.title,10)
        # self.layoutTitleBox.setLayout(self.layoutTitle)

        self.layoutAvdtTitleBox= QWidget()
        self.layoutAvdtTitleBox.setMaximumHeight(80)
        self.layoutAvdtTitle = QHBoxLayout()
        
        self.layoutAvdtTitle.setSpacing(0)
        self.layoutAvdtTitle.setContentsMargins(0,0,0,0)
        self.layoutAvdtTitle.addWidget(self.avdtLogo,1)
        self.layoutAvdtTitle.addWidget(self.avdtTitle,10)
        self.layoutAvdtTitleBox.setLayout(self.layoutAvdtTitle)
        self.layoutAvdtTitleBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def setGridLayout(self):
        self.layoutMainGrid =QGridLayout()
        # self.layoutMainGrid.setSpacing(50)

        # self.layoutMainGrid.addWidget(self.layoutAvdtTitleBox,2,0,1,4)

        self.layoutMainGrid.addWidget(self.btnAvdtLoads,3,0)
        self.layoutMainGrid.addWidget(self.btnAvdtLoadPayments,3,1)
        self.layoutMainGrid.addWidget(self.btnAvdtClients,3,2)
        self.layoutMainGrid.addWidget(self.btnAvdtAccounts,3,3)

        self.layoutMainGrid.addWidget(self.btnAvdtBookkeeping,4,0)
        self.layoutMainGrid.addWidget(self.btnAvdtBookkeepingTotals,4,1)
        self.layoutMainGrid.addWidget(self.btnAvdtBookkeepingCategories,4,2)
        self.layoutMainGrid.addWidget(self.btnAvdtDiesel,4,3)

        
        self.layoutMainGrid.addWidget(self.btnAvdtMiles,5,0)
        self.layoutMainGrid.addWidget(self.btnAvdtStops,5,1)
        self.layoutMainGrid.addWidget(self.btnAvdtIfta,5,2)

        self.layoutMainGrid.addWidget(self.btnAvdtCarriers,6,0)
        self.layoutMainGrid.addWidget(self.btnAvdtDrivers,6,1)
        self.layoutMainGrid.addWidget(self.btnAvdtTrucks,6,2)
        self.layoutMainGrid.addWidget(self.btnAvdtTrailers,6,3)

        self.layoutItemsWidget = QWidget()
        self.layoutItemsWidget.setLayout(self.layoutMainGrid)

        self.layoutMainGridTitle = QVBoxLayout()
        self.layoutMainGridTitle.setContentsMargins(0,0,0,0)
        self.layoutMainGridTitle.addWidget(self.layoutAvdtTitleBox)
        self.layoutMainGridTitle.addWidget(self.layoutItemsWidget)


        self.layoutMainBox.setLayout(self.layoutMainGridTitle)
        

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    sys.exit(app.exec())
