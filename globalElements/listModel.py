#!/usr/bin/python3
from abc import abstractmethod
import sys 
from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QSizePolicy,
    QVBoxLayout, QFrame, QApplication, QLabel)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from treeview import treeviewSearchBox
from globalElements import DB, functions as gf, constants
from globalElements.widgets import buttonWidget, labelWidget


class spacer(QLabel):
    def __init__(self, text='', size="h1"):
        super().__init__(text)
        
        if size.lower() == "h1".lower():
            self.setStyleSheet('''
            QWidget {
                background-color:#002142;
                color: 
                }
            ''')
        else:
            self.setStyleSheet('''
            QWidget {background-color:#134A4D}
            ''')
class titleBox(QWidget):
    def __init__(self, size="h1"):
        super().__init__()
        if size.lower() == "h1".lower():
            self.setStyleSheet('''
            QWidget {
                background-color:#002142;
                color: 
                }
            ''')
        else:
            self.setStyleSheet('''
            QWidget {background-color:#134A4D}
            ''')


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.iconAVD = qtg.QIcon('oth/icons/LOGO_WORLD.png')
        self.initUi()
        

    def initUi(self):
        self.setConstants()
        self.setGlobalVariables() 
        # self.setTitleProperties()
        
        self.initList()
        self.initMain()
        self.set_connections()

#G!GLOBAL CONFIGURATION --------------------------------
    @abstractmethod
    def setGlobalVariables(self):
        self.sqlFolderName = "AVDT_accounting"
        self.mainSize = "h1"
        self.titleText = "TITLE"
        self.sqlFolderName = "AVDT_accounting"
        self.listHiddenItems = ()
        self.listColumnWidth = ()
        dbLogin = constants.avdtDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        self.newRecordSql = '''
        
        '''
        self.selectSql = '''
        
        '''
        

    def setConstants(self):
        # self.sqlFolder = f"oth/sql/{self.thisFileName}"
        self.horizontalLabels = ["Id"]
        self.sortOrder = Qt.SortOrder.AscendingOrder
        self.sortColumn = 1
        self.rowHeight = 42
        self.listFontSize = 12
        self.filterSize = 11
        self.listExpand = 4
        self.size_ = "h1"

    def createButtons(self):
        self.btn_cerrar = buttonWidget(text=" Cerrar", 
            icon=constants.iconClose, size=self.mainSize)

    def setH2Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 10
        self.filterSize = 10

        self.mainSize = "h2"
        self.formSize = "h3"
        self.fontSize = 11
        

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=20,
            fontColor="White",
            align="center",
            backColor="#134A4D") 
        
        self.createButtons()
        

        self.spacerLeft = spacer('    ','h2')
        self.spacer1 = spacer(' ','h2')
        self.spacer2 = spacer('      ','h2')
        self.spacerRight = spacer(' ','h2')
        self.configureTitleLayout()

    def configureTitleLayout(self):
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setSpacing(0)
        self.titleLayout.setContentsMargins(0,0,0,0)
        # self.titleLayout.addWidget(self.spacerLeft)
        # self.titleLayout.addWidget(self.logo)
        self.titleLayout.addWidget(self.title,1)
        self.titleLayout.addWidget(self.spacer1,1)
        self.titleLayout.addWidget(self.btn_cerrar)
        self.titleLayout.addWidget(self.spacerRight)
        
        self.titleLayoutBox = titleBox(self.mainSize)
        self.titleLayoutBox.setLayout(self.titleLayout)

    def setH1Settings(self):
        # LIST INFO
        self.rowHeight = 42
        self.listFontSize = 12
        self.filterSize = 11

        self.mainSize = "h1"
        self.formSize = "h2"
        self.fontSize = 13
        

        self.title = labelWidget(
            text=self.titleText, 
            fontSize=26,
            fontColor="White",
            align="center",
            #backColor="#002142"
            ) 
        
        self.logo = labelWidget(
            align="center",
            #backColor="#002142", 
            padding="6px")
        logo = f'{constants.iconsFolder}enlace.png'
        self.imageAVD = QPixmap(logo)
        self.imageAVD = self.imageAVD.scaled(30,30,Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(self.imageAVD)
        self.createButtons()

        # self.titleLayout = QHBoxLayout()
        # self.titleLayout.setSpacing(0)
        # self.titleLayout.setContentsMargins(0,0,0,0)
        # self.titleLayout.addWidget(self.logo)
        # self.titleLayout.addWidget(self.title,1)
        # self.titleLayoutBox = QWidget()
        # self.titleLayoutBox.setLayout(self.titleLayout)

        self.spacerLeft = spacer('    ')
        self.spacer1 = spacer(' ')
        self.spacer2 = spacer('      ')
        self.spacerRight = spacer(' ')

        self.configureTitleLayout()
        # self.titleLayout = QHBoxLayout()
        # self.titleLayout.setSpacing(0)
        # self.titleLayout.setContentsMargins(0,0,0,0)
        # self.titleLayout.addWidget(self.spacerLeft)
        # self.titleLayout.addWidget(self.logo)
        # self.titleLayout.addWidget(self.title,1)
        # # self.titleLayout.addWidget(self.btnNew)
        # # self.titleLayout.addWidget(self.spacer2)
        # # self.titleLayout.addWidget(self.btnDelete)
        # self.titleLayout.addWidget(self.spacer1,1)
        # self.titleLayout.addWidget(self.btn_cerrar)
        # self.titleLayout.addWidget(self.spacerRight)
        
        # self.titleLayoutBox = titleBox('h1')
        # self.titleLayoutBox.setLayout(self.titleLayout)
    
    def set_connections(self):
        #G! Connections
        # self.list.treeview.selectionModel().selectionChanged.connect(self.listadoSelectionChanged)
        self.btn_cerrar.pressed.connect(self.btn_cerrar_pressed)
        self.list.actRefresh.triggered.connect(self.requery)
        self.list.actClearFilters.triggered.connect(self.clearAllFilters)

    
    def initMain(self):
        # constants its calle first so values can be changed if needed by global
        self.setConstants()
        self.setGlobalVariables()
        # self.sqlFolder = f"oth/sql/{self.sqlFolderName}"
        if self.size_ == "h2":
            self.setH2Settings()
        else: 
            self.setH1Settings()

        # self.setWindowIcon(self.iconAVD)
        # self.setWindowTitle("ENLACE LLC")
        # self.windowTitle().center(50)
        # self.configureMainBtns()
        self.setMainLayout()
        
    # def configureMainBtns(self):
        # self.btn_cerrar = buttonWidget(text="   Cerrar", icon=constants.iconClose, size=self.mainSize)

        # self.layout_buttons = QHBoxLayout() 
        # self.layout_buttons.setSpacing(10)
        # self.layout_buttons.setContentsMargins(15,5,15,5)
        # self.layout_buttons.addStretch()
        # self.layout_buttons.addWidget(self.btn_cerrar)
        
        # self.layout_buttons_box = QWidget()
        # self.layout_buttons_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.layout_buttons_box.setLayout(self.layout_buttons)

    def setMainLayout(self):
        #g! LAYOUT ---- **** Box container for details items
        #o! CONSIDER THE SPLITTER OPTION FOR THE SIDE TO SIDE FORM
        self.splitter_details = QVBoxLayout()
        self.splitter_details.setSpacing(0)
        self.splitter_details.setContentsMargins(0,0,0,0)
        self.splitter_details.addWidget(self.titleLayoutBox)
        # self.splitter_details.addWidget(self.layout_buttons_box)
        self.splitter_details.addWidget(self.list,1)
        self.splitter_details_box = QFrame()
        self.splitter_details_box.setFrameShape(QFrame.Shape.Box)
        self.splitter_details_box.setFrameShadow(QFrame.Shadow.Raised)
        self.splitter_details_box.setLayout(self.splitter_details)

        #g! MAIN SPLITTER
        # self.splitter = QSplitter(qtc.Qt.Orientation.Vertical)
        
        # self.splitter.addWidget(self.splitter_details_box)
        # self.splitter.addWidget(self.list)
        # # self.splitter.setStretchFactor(0,self.formExpand)
        # self.splitter.setStretchFactor(1,self.listExpand)
        
        self.setCentralWidget(self.splitter_details_box)

    def initList(self):
        self.list = treeviewSearchBox()
        self.list.treeview.setWordWrap(True)
    
    def configureColumns(self):
        if self.listColumnWidth:
            self.list.setColumnsWith(self.listColumnWidth)
        if self.listHiddenItems:
            self.list.setHiddenColums(self.listHiddenItems)
        self.list.standardModel.setHorizontalHeaderLabels(self.horizontalLabels) 

    @abstractmethod    
    def requery(self):
        return

    def clearAllFilters(self):
        if self.list.filtros.txt.getInfo():
            self.list.filtros.txt.clear()

    def btn_cerrar_pressed(self):
        #this widget shoud be used withn another widget
        self.parentWidget().parentWidget().currentWidget().deleteLater()

    def selectAll(self, parameters=0):
        # sql = self.getSQL("selectAll.sql")#make sure sql has no ending statement
        parameters = parameters
        records = self.db.get_records_clearNull(self.selectSql, parameters)
        self.horizontalLabels = self.db.cursor.column_names
        return records
    
    def insertNewRecord(self, record):
        r = gf.insertNewRecord(record)
        # sql = self.getSQL("insertNewRecord.sql")
        sql = f"{self.newRecordSql} ({r});"
        # print(sql)
        idVar = self.db.insertNewRecord(sql)
        return idVar
    
    # def getSQL(self, file):
    #     filePath = f"{self.sqlFolder}/{file}"
    #     sqlFile = open(filePath, "r")
    #     sqlFileText = sqlFile.read()
    #     sqlFile.close()
    #     return sqlFileText

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())