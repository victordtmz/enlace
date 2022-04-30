from globalElements.setup import load
load()
import sys
from PyQt6.QtWidgets import (QApplication)

from globalElements import mainModel, treeview
from avdt.carriers import carriers


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = carriers.main()
    mw.show()
    sys.exit(app.exec())