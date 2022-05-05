from globalElements.setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)
from personal.accounts import main as accounts
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = accounts.main()
    mw.show()
    sys.exit(app.exec())