from setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)

from globalElements import treeview
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = treeview.treeviewSearchBox()
    mw.show()
    sys.exit(app.exec())