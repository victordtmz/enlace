
from globalElements.widgets import cbo, labelWidget, lineEdit
from sqlite.zipCodes import zipsSqlite
from PyQt6.QtWidgets import (QWidget, QFormLayout, QCompleter)
from PyQt6.QtCore import Qt

class mainUs(QWidget):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.fontSize = fontSize
        self.initUi()

    def initUi(self):
        self.db = zipsSqlite.DB()
        self.initElements()
        # self.populateState()

    def initElements(self):
        self.zip = lineEdit(self.fontSize)
        self.zip.editingFinished.connect(self.setCityAndState)
        states = self.db.selectStates()
        states.insert(0, "")
        self.state = cbo(self.fontSize, states)
        self.state.currentIndexChanged.connect(self.populateCity)
        self.city = cbo(self.fontSize)
    
    def setCityAndState(self):
        zipCode = self.zip.getInfo()
        if zipCode:
            zipLen = len(zipCode)
            if zipLen == 5:
                city, state = self.db.selectCityState(zipCode)
                self.city.setCurrentText(city)
                self.state.setCurrentText(state)
        
    def populateState(self):
        states = self.db.selectStates()
        states.insert(0, "")
        self.state.addItems(states)
        completer = QCompleter(states)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.state.setCompleter(completer)

    def populateCity(self):
        state = self.state.getInfo()
        if state:
            cities = self.db.selectCities(state)
            cities.insert(0, "")
            self.city.addItems(cities)
            completer = QCompleter(cities)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.city.setCompleter(completer)

    def initLayout(self):
        self.layout_ = QFormLayout()
        self.layout_.addRow(labelWidget('Zip:', self.fontSize), self.zip)
        self.layout_.addRow(labelWidget('State:', self.fontSize), self.state)
        self.layout_.addRow(labelWidget('City:', self.fontSize), self.city)
        self.setLayout(self.layout_)

        

        