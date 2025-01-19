from .main_window import *


class Application(QApplication):
    def __init__(self):
        super().__init__([])

        self.main_window = MainWindow()
        self.main_window.show()
