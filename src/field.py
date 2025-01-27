from .commons import *


class Field(QFrame):
    def __init__(self, label: str):
        super().__init__()

        layout = QHBoxLayout(self)

        qlabel = QLabel(f"Total {label}:")
        qlabel.setStyleSheet("font-size: 15px; font-weight: 600;")
        layout.addWidget(qlabel)

        self.field = QLabel("0")
        self.field.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.field)

    def setField(self, value):
        self.field.setText(str(value))
