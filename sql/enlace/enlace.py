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
        self.initUi()
        self.setGridLayout()
        self.setCentralWidget(self.layoutMainBox)
        self.show()
    

    def initUi(self):
        self.createItemsEnlace()
        self.layoutMainBox = QWidget()
        self.setStyleSheet('''
            QMainWindow {
                background-color:#BEBEBE;
                };

            ''')
        
    def createItemsEnlace(self):
        self.title = labelWidget(
            text="ENLACE LLC", 
            fontSize=45,
            fontColor="White",
            align="center",
            backColor="#002142") 
        self.logo = labelWidget(
            align="center",
            backColor="#002142", 
            padding="6px") 
        self.imageAVD = QPixmap(f'{constants.othFolder}\icons\enlace.png')
        self.imageAVD = self.imageAVD.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(self.imageAVD)

        self.btnJuicios =buttonWidget("    Juicios y Trámites", "main", icon=constants.iconJuicios)
        self.btnTranslate =buttonWidget("    Traducciones", "main", icon=constants.iconTranslate)
        # self.btnAccounting =buttonWidget("    Accounting", "main", icon=constants.iconAccounting)
        self.btnServicios =buttonWidget("    Servicios", "main", icon=constants.iconCustomer)
        self.btnAccounts = buttonWidget("    Accounts", "main", icon=constants.iconAccounts)

        self.layoutTitleBox= QWidget()
        self.layoutTitleBox.setMaximumHeight(100)
        self.layoutTitle = QHBoxLayout() 
        self.layoutTitle.setSpacing(0)
        self.layoutTitle.setContentsMargins(0,0,0,0)
        self.layoutTitle.addWidget(self.logo,1)
        self.layoutTitle.addWidget(self.title,10)
        self.layoutTitleBox.setLayout(self.layoutTitle)

    def setGridLayout(self):
        self.layoutMainGrid = QGridLayout()
        # self.layoutMainGrid.setHorizontalSpacing(50)
        # self.layoutMainGrid.setVerticalSpacing(100)
        # self.layoutMainGrid.setContentsMargins(0,0,0,0)
        # self.layoutMainGrid.addWidget(self.layoutTitleBox,0,0,1,4)
        # self.layoutMainGrid.setAlignment(self.layoutTitleBox,qtc.Qt.AlignmentFlag.AlignJustify)
        self.layoutMainGrid.addWidget(self.btnJuicios,1,0)
        self.layoutMainGrid.addWidget(self.btnTranslate,1,1)
        self.layoutMainGrid.addWidget(self.btnServicios,1,2)
        self.layoutMainGrid.addWidget(self.btnAccounts,1,3)


        self.layoutItemsWidget = QWidget()
        self.layoutItemsWidget.setLayout(self.layoutMainGrid)

        self.layoutMainGridTitle = QVBoxLayout()
        self.layoutMainGridTitle.setContentsMargins(0,0,0,0)
        self.layoutMainGridTitle.addWidget(self.layoutTitleBox)
        self.layoutMainGridTitle.addWidget(self.layoutItemsWidget)


        self.layoutMainBox.setLayout(self.layoutMainGridTitle)
        

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    sys.exit(app.exec())
