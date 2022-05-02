from globalElements.setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)

from globalElements import (mainModel, treeview, functions,
    zipsWidget)
from avdt.bookkeeping import main, cloneDb
from sqlite.scheduleC import main as schedulec
from sqlite.zipCodes import zipsSqlite 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main.main()
    mw.show()
    sys.exit(app.exec())
    # app = cloneDb.Clone()
    # app.cloneDB() 
    #o! SQLITE TESTING
    # db = schedulec.DB()
    # db.selectAll()