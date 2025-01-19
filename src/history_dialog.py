from .commons import *


class HistoryDialog(QFrame):
    selected_history_signal = Signal(str)

    def __init__(self, main_window: QWidget, history: list[str]):
        super().__init__()

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlags(Qt.WindowType.Popup)

        self.main_window = main_window

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(history)
        self.list_widget.setMinimumHeight(200)

    def showEvent(self, _):
        main_window_geometry: QRect = QApplication.instance().main_window.geometry()
        dialog_geometry = main_window_geometry.adjusted(10, 20, 0, 0)
        self.move(
            dialog_geometry.x(),
            dialog_geometry.y(),
        )
