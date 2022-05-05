from setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)
from . import p_accounts as accounts
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = accounts.main()
    mw.show()
    sys.exit(app.exec())