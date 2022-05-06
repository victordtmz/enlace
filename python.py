from pydoc import doc
import sys
from PyQt6.QtWidgets import (QApplication, QCheckBox, QWidget)

class main(QWidget):
    def __init__(self):
        super().__init__()
        print(doc(QCheckBox))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())