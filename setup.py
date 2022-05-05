#!/usr/bin/python3

#python libraries
import sys
import os
import pathlib
def load():
    # ge = 'globalElements'
    paths = ['globalElements']
    for p in paths:
        if p not in sys.path:
            sys.path.insert(0,p)
load()
#PyQt libraries
# ----------------------------------------------------
from PyQt6.QtWidgets import (QWidget,QMainWindow,QHBoxLayout,
    QVBoxLayout,  QApplication)
from PyQt6.QtGui import  (QIcon, QCursor)
from PyQt6.QtCore import Qt

# avd libraries
#-----------------------------------------------
from globalElements import constants, DB, mainModel
from globalElements.widgets import (tabWidget, labelWidget, 
    textEdit, lineEdit, cboFilterGroup)
from enlace import enlace
from enlace.accounts import main as enlaceAccounts

from avdt import avdt
from avdt.loads import loads
from avdt.accounts import main as accounts
from avdt.drivers import main as drivers
from avdt.trucks import main as trucks

    
    