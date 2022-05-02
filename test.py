from globalElements.setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)

from globalElements import (mainModel, treeview, functions,
    zipsWidget)
# from avdt.bookkeeping import main, cloneDb
from localDB.bAccounts import main 
from localDB.zipCodes import zipsSqlite 

 
if __name__ == '__main__':
    db = main.DB()
    db.createDB()
    app = QApplication(sys.argv)
    mw = main.main()
    mw.show()
    sys.exit(app.exec())
    # app = cloneDb.Clone()
    # app.cloneDB() 
    #o! SQLITE TESTING
    db = main.DB()
    db.createDB()