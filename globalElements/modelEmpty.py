#!/usr/bin/python3

from abc import abstractmethod
import sys
from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QApplication, QVBoxLayout, QWidget)
from PyQt6.QtGui import  QIcon
from globalElements.widgets import (buttonWidget, titleBox, spacer, 
    labelWidget, QSizePolicy)
from globalElements import  constants

class main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.iconAVD = QIcon(f'{constants.ROOT_DB}oth/icons/enlace.png')
        
        self.initUi()
        
    def initUi(self):
        self.setGlobalVariables()
        # self.sqlFolder = f"oth/sql/{self.sqlFolderName}"
        
        if self.size_ == "h2":
            self.setH2Settings()
        else: 
            self.setH1Settings()
        
        self.initMain()
        # self.set_connections()
        self.setMainLayout()

#G!GLOBAL CONFIGURATION --------------------------------
    @abstractmethod
    def setGlobalVariables(self):
        self.titleText = ""
        self.size_ = 'h1'
        
    # def createButtons(self):
    #     self.btn_cerrar = buttonWidget(text=" Cerrar", 
    #         icon=constants.iconClose, size=self.mainSize)

    def setH2Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 10
        self.filterSize = 10

        self.mainSize = "h2"
        self.formSize = "h3"
        self.fontSize = 12

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=20,
            fontColor="White",
            align="center",
            backColor="#134A4D") 

        # self.createButtons()

        self.spacerLeft = spacer('    ','h2')
        self.spacer1 = spacer(' ','h2')
        self.spacer2 = spacer('      ','h2')
        self.spacerRight = spacer(' ','h2')
        self.configureTitleLayout()

    def setH1Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 12
        self.filterSize = 11

        self.mainSize = "h1"
        self.formSize = "h2_"
        self.fontSize = 13
        

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=26,
            fontColor="White",
            align="center",
            #backColor="#002142"
            ) 
        
        # self.createButtons()
        # self.spacer1 = spacer(' ')
        # self.spacerRight = spacer(' ')
        self.configureTitleLayout()
        
    def configureTitleLayout(self):
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setSpacing(0)
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.addWidget(self.title,1)
        # self.titleLayout.addWidget(self.spacer1,1)
        # self.titleLayout.addWidget(self.btn_cerrar)
        # self.titleLayout.addWidget(self.spacerRight)
        
        self.titleLayoutBox = titleBox(self.mainSize)
        self.titleLayoutBox.setLayout(self.titleLayout)
        self.titleLayoutBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    # def set_connections(self):
    #     self.btn_cerrar.pressed.connect(self.btn_cerrar_pressed)
        

    def initMain(self):
        self.setWindowIcon(self.iconAVD)
        self.setWindowTitle("ENLACE LLC")
        self.windowTitle().center(50)

    # def btn_cerrar_pressed(self):
    #     self.deleteLater()
    
    def setMainLayout(self):
        self.layoutmain = QVBoxLayout()
        self.layoutmain.setSpacing(0)
        self.layoutmain.setContentsMargins(0,0,0,0)
        self.layoutmain.addWidget(self.titleLayoutBox,0)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layoutmain)
        
        self.setCentralWidget(self.mainWidget)


             
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())