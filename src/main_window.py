from .commons import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Inventory Calculator')

    def mouseDoubleClickEvent(self, _):
        self.close()
