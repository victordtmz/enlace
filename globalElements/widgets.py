#!/usr/bin/python3

from globalElements import constants
from globalElements.functions import formatPhoneNo
# from datetime import time
import re
import webbrowser
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QSizePolicy,
    QComboBox, QCompleter, QHBoxLayout, QGroupBox, QGridLayout, QRadioButton,
    QDateEdit, QDateTimeEdit, QLineEdit, QMainWindow, QToolBar, QCheckBox,
    QMessageBox, QTabWidget, QTextEdit, QSpinBox)

from PyQt6.QtCore import (Qt, QSize, QDate, QDateTime)
from PyQt6.QtGui import (QWheelEvent, QFont, QIcon, QCursor, QGuiApplication,
    QTextDocument, QStandardItem, QColor)
from PyQt6 import QtGui as qtg
from datetime import datetime, time
import locale
locale.setlocale(locale.LC_ALL,"")
globalFontStyle = "Calibri"
globalFontSize = 13
globalFont_ = QFont(globalFontStyle, globalFontSize)
#w! START ---------------------------- LABELS
def printContants():
    print(constants.ROOT_DB)

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

class labelWidget(QLabel):
    def __init__(self, text="", fontSize=13, fontBolt = False, fontColor = "" , align = "", backColor = "", padding="0px" ): 
        super().__init__() 
        
        self.font_ = globalFont_
        self.setText(text)
        self.font_.setPointSize(fontSize)
        if fontBolt:
            self.font_.setBold(True)
            self.setFont(self.font_)
            self.font_.setBold(False)
        else:
            self.setFont(self.font_)

        if fontColor and backColor:
            self.setStyleSheet('''
                QLabel {
                color:%s;
                background-color:%s;
                padding: %s;
                };''' % (fontColor, backColor, padding))
        elif fontColor and not backColor:
            self.setStyleSheet('''
                QLabel {
                color:%s;
                padding: %s;
                };''' % (fontColor, padding))
        elif not fontColor and backColor:
            self.setStyleSheet('''
                QLabel {
                background-color:%s;
                padding: %s;
                };''' % (backColor, padding))

        if align:
            if align == "center":
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif align == "right":
                self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def populate(self,text):    
        self.setText(text)

    def reSet(self):
        self.setText("")

    def getInfo(self):
        return self.text()
#w! START ---------------------------- BUTTONS
class buttonWidget(QPushButton):
    def __init__(self, text="", size="h1", icon=""):
        super().__init__()
        cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(cursor)
        
        if icon:
            icon = QIcon(icon)
            self.setIcon(icon)
        if text:
            self.setText(text)

        if size == "main":
            globalFont_.setPointSize(18)
            iconSize_ = QSize(50, 32)
            # self.setContentsMargins(50,50,50,50)
            self.setIconSize(iconSize_)
            # font_.setBold(True)
            self.setFont(globalFont_)
            self.reSetFont()
            self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            # self.setMinimumHeight(133)
            # self.setFixedSize(130,35)
            self.setMaximumHeight(110)
            self.setMaximumWidth(330)
            css = self.getCSS("main.css")
            self.setStyleSheet(css)


        if size == "h1":
            globalFont_.setPointSize(13)
            # font_.setBold(True)
            self.setFont(globalFont_)
            self.reSetFont()
            # self.setMinimumHeight(35)
            # self.setFixedSize(130,35)
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            css = self.getCSS("h1.css")
            self.setStyleSheet(css)

        elif size == "h1Warning":
            globalFont_.setPointSize(13)
            # font_.setBold(True)
            self.setFont(globalFont_)
            self.reSetFont()
            # self.setMinimumHeight(35)
            # self.setFixedSize(130,35)
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            css = self.getCSS("h1Warning.css")
            self.setStyleSheet(css)

        elif size == "h2":
            globalFont_.setPointSize(12)
            self.setFont(globalFont_)
            self.reSetFont()
            # self.setFixedSize(120,30)
            # self.setMinimumHeight(30)
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            css = self.getCSS("h2.css")
            self.setStyleSheet(css)

        elif size == "h2_":
            globalFont_.setPointSize(12)
            self.setFont(globalFont_)
            self.reSetFont()
            # self.setFixedSize(120,30)
            self.setMinimumHeight(30)
            # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            css = self.getCSS("h2_.css")
            self.setStyleSheet(css)

        elif size == "h3":
            globalFont_.setPointSize(11)
            self.setFont(globalFont_)
            self.reSetFont()
            # self.setFixedSize(120,30)
            self.setMinimumHeight(28)
            # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            css = self.getCSS("h3.css")
            self.setStyleSheet(css)
        
        elif size == "icon":
            self.setFixedSize(27,27)
    
    def getCSS(self, file):
        root = constants.othFolder
        filePath = f"{root}/css/buttons/{file}"
        sqlFile = open(filePath, "r")
        sqlFileText = sqlFile.read()
        sqlFile.close()
        return sqlFileText
    
    def reSetFont(self):
        globalFont_.setPointSize(globalFontSize)
        globalFont_.setBold(False)


class cbo(QComboBox):
    def __init__(self, 
            fontSize =13, 
            items = [], 
            completionMode=QCompleter.CompletionMode.PopupCompletion):
        super().__init__()
        self.setEditable(True)
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        
        self.sourceType = type(items)
        self.items = items
         
        if items:
            # if self.sourceType is dict:
            #     items = sorted(items, key = lambda i: i)
            # else:
            items = sorted(items)
            self.clear()
            self.addItems(items)
            self.completer_name = QCompleter(items)
            self.completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.completer_name.setCompletionMode(completionMode)
            self.setCompleter(self.completer_name) 
            
    def insertNewItems(self, items):
        self.clear()
        self.addItems(items)
        completer_name = QCompleter(items)
        completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # completer_name.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.setCompleter(completer_name)

    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def setConnection(self,e):
        self.currentTextChanged.connect(e)
    
    # def populate(self,text):    
    #     self.setCurrentText(text)

    def reSet(self):
        self.setCurrentIndex(0)

    def getInfo(self):
        return self.currentText()

    def populate(self,text):    
        if self.sourceType is dict:
            if text.isnumeric():
                for k, v in self.items.items():
                    if text == str(v):
                        # print(k)
                        text = k
                        break
        self.setCurrentText(text)

    def getDbInfo(self):
        currentText = self.currentText()
        if self.sourceType is list:
            text = currentText
        elif self.sourceType is dict:
            try: text = self.items[currentText]
            except KeyError: text = '' 
        else:
            text = self.sourceType
        return text

class cboFilterGroup(QWidget):
    def __init__(self, 
            fontSize =13, 
            label = "",
            refreshable = True, 
            items = [], 
            completionMode=QCompleter.CompletionMode.PopupCompletion,
            requeryFunc="", 
            clearFilter = True):

        super().__init__() #self,itemsList, fontSize, requeryFunc
        self.cbo = cbo(fontSize, items, completionMode)
        
        self.items = items
        
        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.addWidget(self.cbo,1)
        self.setLayout(self.layout_)
        
        
        if clearFilter:
            self.btn = buttonWidget(size="icon", icon=constants.iconClearFilter)
            self.layout_.addWidget(self.btn)
            self.btn.pressed.connect(self.btn_pressed)
        
        if label:
            self.lbl = labelWidget(label,fontSize)
            self.layout_.insertWidget(0, self.lbl)
 
        if refreshable and requeryFunc:
            self.btnRequery = buttonWidget(size="icon", icon=constants.iconRefresh)
            self.layout_.insertWidget(1,self.btnRequery)
            self.btnRequery.pressed.connect(self.requery)
            self.requeryFunct = requeryFunc
    
    def insertNewItems(self, items):
        self.cbo.insertNewItems(items)
        # self.cbo.addItems(items)
        # completer_name = QCompleter(items)
        # completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # completer_name.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        # self.cbo.setCompleter(completer_name)

    def requery(self):
        self.requeryFunct()
        self.cbo.clear()
        self.cbo.addItems(self.items)
        self.completer_name = QCompleter(self.items)
        self.completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # self.completer_name.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.cbo.setCompleter(self.completer_name)

    def btn_pressed(self):
        self.cbo.setCurrentText('')
        self.cbo.setFocus()

    def populate(self,text):    
        self.cbo.populate(text)

    def reSet(self):
        self.cbo.reSet()

    def getInfo(self):
        return self.cbo.currentText()

    def currentText(self):
        text = self.cbo.currentText()
        return text
    
    def getDbInfo(self):
        return self.cbo.getDbInfo()


#w! RADIO BUTTONS ------------------------- START
class radioButtons(QGroupBox): 
    def __init__(self, style = False):
        super().__init__()
        self.itemsList = []
        
        self.layout_ = QGridLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout_)
        
        if style:        
            self.setStyleSheet('''
                QGroupBox {
                    font-size: 15px;
                    color: #2F5496;
                    font-weight: 700;
                    border-color: #2F5496;
                }
                ''')
        else:
            self.setStyleSheet('''
                QGroupBox {
                    border: 0;
                }
                ''')


    def reSet(self):
        for i in self.itemsList:
            if i.text() == "All":
                i.setChecked(True)
                return
                
    def getInfo(self):
        filtered = False
        for i in self.itemsList:
            if i.isChecked():
                if i.text() == "All":
                    return ""
                else:
                    filtered = True
                    return i.text()
        if not filtered:
            return ""
 
    def populate(self, text):
        for i in self.itemsList:
            if i.text() == text:
                i.setChecked(True)
                return
            # if hasattr()
            if hasattr(self, "removeFilter"):
                self.removeFilter.setChecked(True)


class truFalseRadioButtons(radioButtons):
    def __init__(self,fontSize = 12, style = False, filter = False):
        super().__init__(style)
        self.layout_.setContentsMargins(0,0,0,0)
        self.true = QRadioButton("True")
        self.false = QRadioButton("False")
        self.itemsList.extend([self.true, self.false])

        #Row 0 
        self.layout_.addWidget(self.true,0,0)
        self.layout_.addWidget(self.false,0,1)
        
        if filter:
            self.removeFilter = QRadioButton("All")
            self.itemsList.append(self.removeFilter)
            self.layout_.addWidget(self.removeFilter,0,2)

        globalFont_.setPointSize(fontSize)
        for i in self.itemsList:
            i.setFont(globalFont_)
        globalFont_.setPointSize(globalFontSize)
    
    def getDbInfo(self):
        if self.true.isChecked():
            return "1"
        elif self.false.isChecked():
            return "0"
        else:
            return ""

class incomeExpenseRadioButtons(radioButtons):
    def __init__(self, fontSize = 12, style = False, filter = False):
        super().__init__(style)
        self.layout_.setContentsMargins(0,0,0,0)
        self.income = QRadioButton("Income")
        self.expense = QRadioButton("Expense")
        
        

        self.itemsList.extend([self.income, self.expense])
        #Row 0 
        self.layout_.addWidget(self.income,0,0)
        self.layout_.addWidget(self.expense,0,1)
        if filter:
            self.removeFilter = QRadioButton("All")
            self.itemsList.append(self.removeFilter)
            self.layout_.addWidget(self.removeFilter,0,2)

        globalFont_.setPointSize(fontSize)
        for i in self.itemsList:
            i.setFont(globalFont_)
        globalFont_.setPointSize(globalFontSize)

    def getDbInfo(self):
        if self.income.isChecked():
            return "1"
        else:
            return "0"

#w! RADIO BUTTONS ------------------------- END

#w! DATE  ------------------------- START
class dateEdit(QDateEdit):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy-MM-dd')
        # self.setDate(QDate.currentDate())
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
    
    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def populate(self, text):
        try:
            fecha = datetime.strptime(text, '%Y-%m-%d')
        except:
            fecha = datetime(2000,1,1)
        self.setDate(fecha)

    def reSet(self):
        fecha = datetime(2000,1,1)
        self.setDate(fecha)

    def getInfo(self):
        return self.text()

class dateWidget(QWidget):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.dateEdit = dateEdit(fontSize) 
        self.btnToday = buttonWidget(size="icon", icon=constants.iconToday)
        self.btnToday.setMinimumHeight(30)

        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        # self.layout_.addWidget(self.lbl)
        self.layout_.addWidget(self.dateEdit,1)
        self.layout_.addWidget(self.btnToday)
        self.setLayout(self.layout_)

        self.btnToday.pressed.connect(self.btnTodayPressed)
        
    def btnTodayPressed(self):
        self.dateEdit.setDate(QDate.currentDate())

    def populate(self, text):
        self.dateEdit.populate(text)
        
    def reSet(self):
        self.dateEdit.reSet()

    def getInfo(self):
        return self.dateEdit.getInfo()

class dateTimeEdit(QDateTimeEdit):
    def __init__(self, fontSize = 13):
        super().__init__()
        # self.setCalendarPopup(True)
        # self.setDisplayFormat('yyyy-MM-dd')
        # self.setDate(QDate.currentDate())
        self.setDisplayFormat("yyyy-MM-dd hh:mm")
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
    
    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def populate(self, text):
        try:
            dateTime =  datetime.strptime(text, '%Y-%m-%d %H:%M')
            # time_ = time_.time()
        except:
            date = QDateTime()
            dateTime = date.currentDateTime()
        self.setDateTime(dateTime)
        

    def reSet(self):
        date = QDateTime()
        dateTime = date.currentDateTime()
        self.setDateTime(dateTime)

    def getInfo(self):
        return self.text()
#w! DATE  ------------------------- END


#w! LINEEDIT  ------------------------- START
class lineEdit(QLineEdit):
    def __init__(self, fontSize = 13, hightLight=False):
        super().__init__()
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        if hightLight:
            self.setStyleSheet("QLineEdit"
                        "{"
                        "background : #ffeeda;"
                        "}")
        
    # def setConnection(self,e):
    #     self.textChanged.connect(e)
    def populate(self, text):
        self.setText(text)
    
    def reSet(self):
        self.clear()

    def getInfo(self):
        return self.text()

class lineEditPhone(lineEdit):
    def __init__(self, fontSize =13):
        super().__init__(fontSize)
        self.firstPass = ''
        self.textChanged.connect(self.format)
        
    
    def getInfo(self):
        currentNo = ''.join(re.findall(r'\d',self.text()))
        return currentNo
        

    def format(self):
        inputValue = self.text()
        inputLength = len(inputValue)
        if inputLength > 3:
            #only evauate if more than 3 elements. 
            currentNo = ''.join(re.findall(r'\d',inputValue))
            currentNoLength = len(currentNo)
            # only format if more than 3 digits
            if currentNoLength > 3:
                try:
                    formatedNo = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}',str(currentNo)))
                    if not formatedNo == inputValue:
                        self.changeValue(currentNo)
                except:
                    self.changeValue(currentNo)
            

    def changeValue(self,currentNo):
        PhoneNo = formatPhoneNo(currentNo)
        self.setText(PhoneNo)
class lineEditCurrency(lineEdit):
    def __init__(self, fontSize):
        super().__init__(fontSize)
    
    def getInfo(self):
        return self.text()
    
    def getDbInfo(self):
        info = self.text()
        if info:
            try:
                info = locale.atof(str(info).strip("$()"))
                return str(info)
            except:
                return ""
            # print(info)
            
    def populate(self, text):
        if text:
            text = str(text).strip("()")
            if "$" in text:
                self.setText(text)
            else:
                amount = float(text)
                amount = locale.currency(amount, grouping=True)
                self.setText(amount)

    
    def reSet(self):
        self.clear()


class lineEditFilterGroup(QWidget):
    def __init__(self, fontSize =13, label = "", clearFilter = True):
        '''Line edit with label and clear text button'''
        super().__init__()
        self.txt = lineEdit(fontSize)
        # self.txt.setMinimumWidth(180)
        # self.btn = buttonWidget(size="icon", icon=constants.iconClearFilter)
        
        self.btn = buttonWidget(size="icon", icon=constants.iconClearFilter)
        # else:
        #     self.btn = buttonWidget(size="icon", icon=self.btn.iconEraser)
        self.btn.setMaximumHeight(25)        
        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.addWidget(self.txt,1)
        if clearFilter:
            self.layout_.addWidget(self.btn)
        self.setLayout(self.layout_)
        if label:
            self.lbl = labelWidget(label,fontSize)
            self.layout_.insertWidget(0, self.lbl)

        self.btn.pressed.connect(self.btn_pressed)
    
    def btn_pressed(self):
        self.txt.clear()
        self.txt.setFocus()

    def populate(self,text):    
        self.txt.populate(text)

    def reSet(self):
        self.txt.reSet()

    def getInfo(self):
        return self.txt.text()

    def currentText(self):
        text = self.txt.text()
        return text
#w! LINEEDIT  ------------------------- START

class textEdit(QTextEdit):
    def __init__(self, fontSize=11):
        super().__init__()
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        self.setMinimumHeight(170)

    def populate(self, text):
        self.setText(text)
    
    def reSet(self):
        self.clear()

    def getInfo(self):
        return self.toPlainText()

    def toSQL(self):
        '''Set code for html SQL output'''
        notesText = self.toPlainText()
        # textVar = textVar.replace("\\",'\\\\')
        sqlText = notesText.replace("'",'\'\'')
        sqlText = sqlText.replace('"','\\\"')
        sqlText = sqlText.replace('%','\%')
        sqlText = sqlText.replace('_','\_')
        # sqlText = sqlText.replace('','\_')
        # sqlText = sqlText.replace('\\\\\'','\\\\\\\\')
        sqlText = sqlText.replace('\\','\\\\')
        # return [sqlText, htmlText]
        return sqlText

class textEditRich(QMainWindow):
    def __init__(self, fontSize = 11):
        '''MainWindow Constructor'''
        super().__init__()
        self.iconBold = QIcon('oth/icons/edit-bold.png')
        self.iconUnderline = QIcon('oth/icons/edit-underline.png')
        self.iconItalic = QIcon('oth/icons/edit-italic.png')
        self.iconHiglight = QIcon('oth/icons/highlighter-text.png')
        self.iconRed = QIcon('oth/icons/edit-red.png')
        self.iconP = QIcon('oth/icons/edit.png')
        self.iconH1 = QIcon('oth/icons/edit-heading-1.png')
        self.iconH2 = QIcon('oth/icons/edit-heading-2.png')
        self.iconH3 = QIcon('oth/icons/edit-heading-3.png')
        self.iconH4 = QIcon('oth/icons/edit-heading-4.png')
        self.iconH5 = QIcon('oth/icons/edit-heading-5.png')
        self.iconH6 = QIcon('oth/icons/edit-heading-6.png')
        self.cb = QGuiApplication.clipboard()
        self.textBox = textEdit(fontSize)
        self.format = QTextDocument(self.textBox)
        self.textBox.setDocument(self.format)
        
        css = open('oth/Program_Data/style.css','r')
        self.style_ = css.read()
        self.format.setDefaultStyleSheet(self.style_)

        #p! Tool Bar
        self.toolBar = QToolBar('File')
        self.toolBar.addAction(self.iconP, 'P',self.txtP)
        self.toolBar.addAction(self.iconBold, 'Bold',self.txtBold)
        self.toolBar.addAction(self.iconUnderline, 'Underline',self.txtUnderline)
        self.toolBar.addAction(self.iconItalic, 'Italic',self.txtItalic)
        self.toolBar.addAction(self.iconHiglight, 'Highlight',self.txtHighlight)
        self.toolBar.addAction(self.iconRed, 'Red',self.txtRed)
        
        self.toolBar.addAction(self.iconH1, 'H1',self.txtH1)
        self.toolBar.addAction(self.iconH2, 'H1',self.txtH2)
        self.toolBar.addAction(self.iconH3, 'H1',self.txtH3)
        self.toolBar.addAction(self.iconH4, 'H1',self.txtH4)
        self.toolBar.addAction(self.iconH5, 'H1',self.txtH5)
        self.toolBar.addAction(self.iconH6, 'H1',self.txtH6)
        # self.toolBar.addAction(self.iconH1, 'H1',self.toSQL)
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.setCentralWidget(self.textBox)
        #g! Connections

    def setConnection(self,e):
        self.textBox.textChanged.connect(e)

    def populate(self, text):
        self.textBox.setText(text)

    def reSet(self):
        self.textBox.setText('')

    def getInfo(self):
        return self.textBox.toHtml()

    def toSQL(self):
        sqlText = self.textBox.toSQL()
        return sqlText

    def copyText(self):
        self.textBox.copy()
        return self.cb.mimeData().text()
    
    def txtBold(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<strong>{inputText}</strong>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)
    
    def txtUnderline(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<u>{inputText}</u>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtItalic(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<i>{inputText}</i>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtHighlight(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<div class="highlight">{inputText}</div>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)
    
    def txtRed(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<div class="redText">{inputText}</div>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtP(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<p>{inputText}</p>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)


    def txtH1(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h1>{inputText}</h1>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtH2(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h2>{inputText}</h2>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtH3(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h3>{inputText}</h3>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtH4(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h4>{inputText}</h4>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)
        
    def txtH5(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h5>{inputText}</h5>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

    def txtH6(self):
        inputText = self.copyText()
        if inputText:
            outputText = f'''<h6>{inputText}</h6>'''
            self.textBox.insertHtml(outputText)
            self.cb.clear()
            self.format.setDefaultStyleSheet(self.style_)

class lineEditCopy(QWidget):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.lineEdit = lineEdit(fontSize) 
        self.btnCopyLink = buttonWidget(size="icon", icon=constants.iconCopy)
        self.btnCopyLink.setMinimumHeight(30)
        self.btnCopyLink.setText("")

        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        # self.layout_.addWidget(self.lbl)
        self.layout_.addWidget(self.lineEdit,1)
        self.layout_.addWidget(self.btnCopyLink)
        self.setLayout(self.layout_)

        self.btnCopyLink.pressed.connect(self.btnCopyLinkPressed)
        
    def btnCopyLinkPressed(self):
        cb = QGuiApplication.clipboard()
        cb.clear(cb.Mode.Clipboard)
        link = self.lineEdit.text()
        if link:
            cb.setText(link)

    def populate(self, text):
        self.lineEdit.populate(text)
        
    def reSet(self):
        self.lineEdit.reSet()

    def getInfo(self):
        return self.lineEdit.getInfo()
class webWidget(lineEditCopy):
    """Widget that contains 3 widgets:
    lineEdit => QlineEdit - with DB methods to populate, reset, getdata
        this widget may contain the link, if is shorter than 40 char, else
        the owrds 'V??nculo - P??gina Web' will appear
    btnCopyLink => Button - Copy lineEdit content to clipboard
    btnWeb => Button - Opens web link in browser.

    self.link element holds the link - when populated. 

    USE TE populate FUNCTION for propper operation. 

    Args:
        lineEditCopy (lineEdit witth copy button): Contains widgets of the 3 on self
        the lineEdit and btnCopyLink
    """
    def __init__(self, fontSize = 13):
        super().__init__(fontSize)
        self.link = ''
        self.btnWeb = buttonWidget(size="icon",icon= constants.iconWeb)
        self.setStyleSheet('''QLineEdit
                        {
                        color : blue;
                        text-decoration: underline;
                        }''')
        
        self.layout_.addWidget(self.btnWeb)

        self.btnWeb.pressed.connect(self.btnWebPressed)
        
    def __repr__(self) -> str:
        return "global webWidget"
    
    def populate(self, text):
        self.link = text
        print(self.link)
        print(len(self.link))
        if len(text) > 40:
             self.lineEdit.populate('V??nculo - P??gina Web')
        else: 
            self.lineEdit.populate(text)

    def btnWebPressed(self):
        """Opens link in web browser - link might be different than showing lineEdit
        """
        if not self.link:
            self.link = self.lineEdit.text()
        if self.link:
            webbrowser.open(self.link) 

class checkBox(QCheckBox):
    def __init__(self, text='', fontSize = 13, size=''):
        super().__init__()
        cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(cursor)
        if text:
            globalFont_.setPointSize(fontSize)
            self.setFont(globalFont_)
            self.setText(text)
        if size == 'h1' or size == 'h2':
            self.setStyleSheet('QCheckBox {color: white} ')
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        

    
    def populate(self, value):
        if value == '1' or value.lower() == "true":
            self.setChecked(True)
        else:
            self.setChecked(False)
    
    def reSet(self):
        self.setChecked(False)

    def getInfo(self):
        if self.isChecked():
            return 'True'
        else:
            return 'False'

    def getDbInfo(self):
        if self.isChecked():
            return "1"
        else:
            return "0"

class spinbox(QSpinBox):
    def __init__(self, fontSize=13):
        super().__init__()
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        # self.setMinimumHeight(170)
        # font_.setPointSize(fontSize)
        # self.setFont(font_)
        # self.setMaximum(500000)
        # self.setSingleStep(1)
    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def getInfo(self):
        return self.cleanText()
    
    def populate(self, text):
        try:
            self.setValue(int(text))
        except:
            self.reSet()
    
    def reSet(self):
        self.setValue(1)

class tabWidget(QTabWidget):
    def __init__(self, size="h1"):#self, fontSize=10, selectedSize=16
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setTabsClosable(True)
        self.setMinimumHeight(170)
        self.setTabBarAutoHide(True)
        css = self.getCSS(f'{size}.css')
        self.setStyleSheet(css)

        self.tabCloseRequested.connect(self.close_tab_requested)
    
    def getCSS(self, file):
        root = constants.othFolder
        filePath = f"{root}/css/tabWidgets/{file}"
        sqlFile = open(filePath, "r")
        sqlFileText = sqlFile.read()
        sqlFile.close()
        return sqlFileText

    def close_tab_requested(self, intVar):
        if intVar:
            self.removeTab(intVar)
            # self.widget(intVar).deleteLater()

class standardItem(QStandardItem):
    def __init__(self,  txt='',fontSize = 13, rowHeight=42, colorVar ='#000000'):
        super().__init__()
        self.setEditable(True)
        # constants.font_.setBold(False)
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        self.setText(str(txt))
        self.setForeground(QColor(colorVar))
        self.setSizeHint(QSize(20,rowHeight))


class deleteWarningBox(QMessageBox):
    def __init__(self, text='', fontSize=13):
        super().__init__()
        self.iconAVD = QIcon( f'{constants.othFolder}\icons\enlace.png')
        self.setWindowTitle('Eliminar registro')
        self.setWindowIcon(QIcon(f'{constants.othFolder}\icons\enlace.png'))
        self.setText(text)
        # self.setStyleSheet("QLabel{min-width: 200px;}")
        self.setInformativeText('Continue?')
        globalFont_.setPointSize(fontSize)
        self.setFont(globalFont_)
        self.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        self.setIcon(QMessageBox.Icon.Warning)