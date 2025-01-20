from .inventory import *
from .commons import *


class TableWidget(QTableWidget):
    item_updated = Signal()

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
        # self.setSortingEnabled(True)

        self.setColumnCount(len(COLUMNS))
        for index, column in enumerate(COLUMNS):
            item = QTableWidgetItem()
            item.setText(column)
            font = item.font()
            font.setBold(True)
            font.setPointSize(12)
            item.setFont(font)
            self.setHorizontalHeaderItem(index, item)

        self.itemChanged.connect(self.onItemChanged)

        self.updateItems()

    def onItemChanged(self, item: QTableWidgetItem):
        row = item.row()
        column = item.column()

        column_name = COLUMNS_L[column]
        type = COLUMNS_TYPE[column]
        null = COLUMNS_NULL[column]

        value = item.text()

        try:
            value = type(value)
            if type == str:
                value = value.strip()
        except:
            value = null

        self.saved_edited_item = item
        inventory_item = self.inventory.item(row)

        if not inventory_item:
            inventory_item = self.inventory.add()

        setattr(inventory_item, column_name, value)

        if inventory_item.is_empty:
            self.inventory.remove_item(inventory_item)
            inventory_item = None

        self.updateItems()

    def print(self, *_, **__):
        if self.isVisible():
            print(*_, **__)

    def updateItems(self):
        if not self.isVisible():
            return

        self.blockSignals(True)

        self.setRowCount(self.inventory.total_items + 5)
        lastColumn = self.columnCount() - 1
        rowCount = self.rowCount()

        # set amount uneditable
        for row in range(rowCount):
            values = self.inventory.item_values(row)

            for column, value in enumerate(values):
                table_item = self.item(row, column)

                if (value or (column == lastColumn)) and not table_item:
                    table_item = QTableWidgetItem()
                    self.setItem(row, column, table_item)

                if table_item:
                    table_item.setText(value)

                if column == lastColumn:
                    table_item.setFlags(Qt.ItemFlag.NoItemFlags)

        self.blockSignals(False)
        self.item_updated.emit()

    def showEvent(self, _):
        self.updateItems()
