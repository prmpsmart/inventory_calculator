from .inventory import *
from .commons import *


class TableWidget(QTableWidget):
    def __init__(self, inventory: Inventory):
        super().__init__()
        self.inventory = inventory

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.setAlternatingRowColors(True)
        self.setWordWrap(True)
        self.setShowGrid(True)
        self.setAutoScroll(False)
        self.setSortingEnabled(True)

        self.columns = ["Name", "Count", "Price", "Amount"]
        self.setColumnCount(len(self.columns))
        for index, column in enumerate(self.columns):
            item = QTableWidgetItem()
            item.setText(column)
            font = item.font()
            font.setBold(True)
            font.setPointSize(12)
            item.setFont(font)
            self.setHorizontalHeaderItem(index, item)

        self.setRowCount(10)

        self.cellDoubleClicked.connect(self.onCellDoubleClicked)
        self.itemChanged.connect(self.onItemChanged)

        self.edited_item: QTableWidgetItem = None
        self.saved_edited_item: QTableWidgetItem = None

        self.updateItems()

    def onCellDoubleClicked(self, row: int, column: int):
        self.edited_item = self.item(row, column)
        self.print("onCellDoubleClicked")

        # self.updateItems()

    def onItemChanged(self, item: QTableWidgetItem):
        self.saved_edited_item = item
        self.print("onItemChanged")

        # self.updateItems()

    def print(self, *_, **__):
        if self.isVisible():
            print(*_, **__)

    def updateItems(self):
        row = self.rowCount()
        column = self.columnCount()

        # set amount uneditable
        for r in range(row):
            for c in range(column):
                if c != len(self.columns) - 1:
                    continue

                if not (item := self.item(r, c)):
                    item = QTableWidgetItem()
                    self.setItem(r, c, item)
                item.setFlags(Qt.ItemFlag.NoItemFlags)
