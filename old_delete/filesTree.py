#!/usr/bin/python3
import constants
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
import os
from globalElements.widgets import labelWidget, lineEdit, lineEditFilterGroup, buttonWidget
class filesTree(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        #g! ICONS
        # self.fontSize = fontSize
        self.iconOpenFile = qtg.QIcon('oth/icons/google-docs.png')
        self.iconOpenFolder = qtg.QIcon('oth/icons/openFolder.png')
        self.iconNewFolder = qtg.QIcon('oth/icons/folderAdd.png')
        self.iconAVD= qtg.QIcon('oth/icons/LOGO_WORLD.png')
        self.iconDelete= qtg.QIcon('oth/icons/delete.png')
        self.iconClearSelection= qtg.QIcon('oth/icons/removeSelection.png')
        self.iconCopy = qtg.QIcon('oth/icons/link.png')


        self.filesModel = qtg.QFileSystemModel() #data item model
        self.filesModel.setReadOnly(False)
        self.root = os.path.expanduser('~\OneDrive')
        self.filesDir = self.root # this variable will be changing to addapt to the box location and record selected
        self.filesModel.setRootPath(self.filesDir) #assignment that will be changing. 
        self.filesTree = qtw.QTreeView() # Tree item
        self.filesTree.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.CustomContextMenu)
        self.filesTree.setDragEnabled(True)
        self.filesTree.setAcceptDrops(True)
        self.filesTree.setDropIndicatorShown(True)
        
        # self.filesTree.
        self.filesTree.setModel(self.filesModel)
        self.filesTree.setRootIndex(self.filesModel.index(self.filesDir))
        self.filesTree.hideColumn(1)
        self.filesTree.hideColumn(2)
        self.filesTree.hideColumn(3)

        #p! Tool Bar
        self.toolBar = qtw.QToolBar('File')
        self.toolBar.setToolButtonStyle(qtc.Qt.ToolButtonStyle.ToolButtonIconOnly)
        # self.toolBar.addAction('Crear Archivo')
        
        #g! Actions
        self.action_open = qtg.QAction('Abrir archivo')
        self.action_open.setIcon(self.iconOpenFile)
        self.action_open.triggered.connect(self.file_open)
        # Delete file action
        self.action_delete = qtg.QAction('Eliminar')
        self.action_delete.setIcon(self.iconDelete)
        self.action_delete.triggered.connect(self.file_delete)
        # New Folder file action
        self.action_newFolder = qtg.QAction('Crear carpeta')
        self.action_newFolder.setIcon(self.iconNewFolder)
        self.action_newFolder.triggered.connect(self.new_folder)
        # Delete file action
        self.action_copyPath = qtg.QAction('Copiar vinculo')
        self.action_copyPath.setIcon(self.iconCopy)
        self.action_copyPath.triggered.connect(self.copyPath) 
        # Delete file action
        self.action_ClearSelection = qtg.QAction('Eliminar selección')
        self.action_ClearSelection.setIcon(self.iconClearSelection)
        self.action_ClearSelection.triggered.connect(self.selection_clear)
        # Open Folder action
        self.actionOpenFolder = qtg.QAction('Abrir folder')
        self.actionOpenFolder.setIcon(self.iconOpenFolder)
        self.actionOpenFolder.triggered.connect(self.folderOpen)

        self.toolBar.addAction(self.actionOpenFolder)
        self.toolBar.addAction(self.action_open)
        self.toolBar.addAction(self.action_delete)
        self.toolBar.addAction(self.action_newFolder)
        self.toolBar.addAction(self.action_copyPath)
        self.toolBar.addAction(self.action_ClearSelection)
        iconSize = qtc.QSize(35,20)
        self.toolBar.setIconSize(iconSize)
        
        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        self.filesLabel = labelWidget('Folder:',10)
        self.txtFilePath = lineEdit(8)
        self.txtFilePath.setReadOnly(True)
        # self.copyBtn = gw.btn_copyIcon()
        self.layout_files = qtw.QGridLayout()
        self.layout_files.setSpacing(0)
        # self.layout_files.addWidget(self.filesLabel,0,0)
        # self.layout_files.addWidget(self.txtFilePath,0,1)
        # self.layout_files.addWidget(self.copyBtn,0,2)
        self.layout_files.addWidget(self.filesTree,1,0,1,3)
        self.layout_files_box = qtw.QWidget()
        self.layout_files_box.setLayout(self.layout_files)
        self.setCentralWidget(self.layout_files_box)

        # self.copyBtn.pressed.connect(self.copyPath)
        self.txtFilePath.textChanged.connect(self.setPath)
        self.txtFilePath.setText(self.root)
        self.filesTree.customContextMenuRequested.connect(self.contextMenu)
        self.filesTree.doubleClicked.connect(self.file_open)

    def setLineEditFileBox(self, fontSize=13):
        self.lineEditItems = lineEditFilterGroup(fontSize,"Archivo:", clearFilter=False)
        # self.lineEditItems.lbl.deleteLater()
        self.btnOpen =  buttonWidget(text="Abrir archivo", size="h2", icon=constants.iconFolderOpen)
        self.btnOpen.setSizePolicy(qtw.QSizePolicy.Policy.Expanding,qtw.QSizePolicy.Policy.Fixed)
        # self.btnOpen.setMinimumWidth(130)
        self.btnLinkFile = buttonWidget(text="Vincular archivo", size="h2", icon=constants.iconLink)
        self.btnLinkFile.setSizePolicy(qtw.QSizePolicy.Policy.Expanding,qtw.QSizePolicy.Policy.Fixed)
        
        self.layoutLineEditFile = qtw.QGridLayout()
        self.layoutLineEditFile.setSpacing(1)
        self.layoutLineEditFile.addWidget(self.lineEditItems,0,0,1,2)
        self.layoutLineEditFile.addWidget(self.btnOpen,1,0)
        self.layoutLineEditFile.addWidget(self.btnLinkFile,1,1)
        self.layoutLineEditFileBox = qtw.QWidget()
        self.layoutLineEditFileBox.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Fixed)
        self.layoutLineEditFileBox.setLayout(self.layoutLineEditFile)

        # self.setLayout(self.layout_)

        self.btnLinkFile.pressed.connect(self.setFile)
        self.btnOpen.pressed.connect(self.openFile)

    def populate(self, text):
        self.lineEditItems.txt.setText(text)
    
    def reSet(self):
        self.lineEditItems.txt.clear()

    def getInfo(self):
        return self.lineEditItems.txt.text()

    def setFile(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                filePath = self.filesModel.filePath(index)
                folderPath = f'{self.txtFilePath.text()}\\'
                folderPath = folderPath.replace('\\','/')
                fileName = filePath.replace(folderPath,'')
                self.lineEditItems.txt.setText(fileName)  

    def openFile(self):
        fileName = self.lineEditItems.txt.text()
        if fileName:
            folderPath = self.txtFilePath.text()
            filePath = f'{folderPath}/{fileName}'
            try:
                os.startfile(filePath)
            except:
                print('Archivo no existe')
    
    def contextMenu(self):
        # add items to menu
        menu = qtw.QMenu()
        menu.addAction(self.actionOpenFolder)
        menu.addAction(self.action_open)
        menu.addAction(self.action_delete)
        menu.addAction(self.action_newFolder)
        menu.addAction(self.action_copyPath)
        menu.addAction(self.action_ClearSelection)
        cursor = qtg.QCursor()
        menu.exec(cursor.pos())
    
    def setPath(self, path):
        self.filesDir = path
        self.filesModel.setRootPath(self.filesDir)
        self.filesTree.setRootIndex(self.filesModel.index(self.filesDir))
        self.filesTree.clearSelection()
    
    def copyPath(self):
        cb = qtg.QGuiApplication.clipboard()
        cb.clear(cb.Mode.Clipboard)
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                if self.filesModel.isDir(index):
                    filePath = self.filesModel.filePath(index)
                    cb.setText(filePath)
                else:
                    cb.setText(self.txtFilePath.text()) 
            else:
                cb.setText(self.txtFilePath.text())
        else:
            cb.setText(self.txtFilePath.text())
    
    def wheelEvent(self, e: qtg.QWheelEvent) -> None:
        e.ignore()
    
    # def document_copy(self):
    #     if self.filesTree.selectionModel().hasSelection():
    #         index = self.filesTree.selectionModel().selectedIndexes()[0]
    #         if index:
    #             filePath = self.filesModel.filePath(index)
    #             cb = qtg.QGuiApplication.clipboard()
    #             cb.clear(cb.Mode.Clipboard)
    #             cb.setObjectName(filePath)
    
    def selection_clear(self):
        self.filesTree.clearSelection()
    
    
    def folderOpen(self):
        try:
            os.startfile(self.filesDir)
        except FileNotFoundError:
            os.startfile(self.root)
        except:
            print('Folder not found')

    def file_open(self):
        self.filesModel.setReadOnly(True)
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if index:
                filePath = self.filesModel.filePath(index)
                try:
                    os.startfile(filePath)
                except FileNotFoundError:
                    print('File not found')   
        else: 
            try:
                os.startfile(self.filesDir)
            except FileNotFoundError:
                os.startfile(self.root)
            except:
                print('File not found')
        self.filesModel.setReadOnly(False)

    def new_folder(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            if self.filesModel.isDir(index):
                self.filesModel.mkdir(index,'New Folder') 
            else:
                index = self.filesModel.index(self.filesDir)
                if index:
                    self.filesModel.mkdir(index,'New Folder') 
        
        else: 
            index = self.filesModel.index(self.filesDir)
            if index:
                self.filesModel.mkdir(index,'New Folder') 

    def file_delete(self):
        if self.filesTree.selectionModel().hasSelection():
            index = self.filesTree.selectionModel().selectedIndexes()[0]
            fileName = index.data()
        
            warning_box = qtw.QMessageBox()
            warning_box.setWindowTitle('Elmininar archivo')
            warning_box.setWindowIcon(self.iconAVD)
            warning_box.setText(f'''Advertencia, está a punto de eliminar el archivo: {fileName}''')
            warning_box.setInformativeText('Desea continuar?')
            
            warning_box.setStandardButtons(qtw.QMessageBox.StandardButton.Yes|qtw.QMessageBox.StandardButton.No)
            warning_box.setIcon(qtw.QMessageBox.Icon.Warning)
            button = warning_box.exec()

            if button == qtw.QMessageBox.StandardButton.Yes:
                self.filesModel.remove(index)