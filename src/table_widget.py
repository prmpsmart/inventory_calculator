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
        self.setAutoScroll(True)
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

        value = item.text().strip()

        try:
            if type != str:
                value = value.strip().replace(",", "")
            value = type(value)
        except:
            value = null

        inventory_item = self.inventory.item(row)

        if not inventory_item:
            inventory_item = self.inventory.add()

        setattr(inventory_item, column_name, value)

        if inventory_item.is_empty:
            self.inventory.remove_item(inventory_item)
            inventory_item = None

        if (row > self.inventory.total_items + 2) or column:
            self.updateItems()

    def print(self, *_, **__):
        if self.isVisible():
            print(*_, **__)

    @property
    def currentItemIndex(self) -> int:
        currentRow = self.currentRow()

        if currentRow >= self.inventory.total_items:
            currentRow = self.inventory.total_items - 1

        if currentRow < 0:
            currentRow = 0

        return currentRow

    def moveItems(self, up: bool):
        old = self.currentItemIndex
        new = old + (-1 if up else 1)
        self.inventory.items[new], self.inventory.items[old] = (
            self.inventory.items[old],
            self.inventory.items[new],
        )
        self.updateItems()
        self.setCurrentCell(new, self.currentColumn())

    def onUpButton(self):
        if not (self.currentItemIndex and self.inventory.total_items):
            return
        self.moveItems(True)

    def onDownButton(self):
        total_items = self.inventory.total_items
        if (not total_items) or (total_items - 1 == self.currentItemIndex):
            return
        self.moveItems(False)

    def onCopyButton(self):
        row = self.currentRow()
        if row < 0 or (not self.inventory.total_items):
            return

        self.inventory.items.append(self.inventory.items[row].copy())
        self.updateItems()

    def onDeleteButton(self):
        row = self.currentRow()
        if row < 0 or (not self.inventory.total_items):
            return

        del self.inventory.items[row]
        self.updateItems()

    def updateItems(self):
        if not self.isVisible():
            return

        self.blockSignals(True)

        self.setRowCount(self.inventory.total_items + 5)
        lastColumn = self.columnCount() - 1
        amountColumn = lastColumn - 1
        rowCount = self.rowCount()

        flow = 0

        # set amount uneditable
        for row in range(rowCount):
            values = self.inventory.item_values(row, flow)

            for column, value in enumerate(values):
                if column > lastColumn:
                    continue

                if (column == lastColumn) and (_flow := value.replace(",", "").strip()):
                    flow = float(_flow)

                table_item = self.item(row, column)

                if not table_item:
                    table_item = QTableWidgetItem()
                    self.setItem(row, column, table_item)

                table_item.setFlags(
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
                )
                table_item.setBackground(Qt.GlobalColor.gray)
                table_item.setForeground(Qt.GlobalColor.white)

                if table_item:
                    table_item.setText(value)
                    if column == 1 or "___" in values[0]:
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    elif column > 1:
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                    elif len(values[0]) > 80:
                        table_item.setSizeHint(QSize(450, 60))

                    if value and (values[2].startswith("-") and column in [0, 2, 3]) or (
                        flow < 0 and column == lastColumn
                    ):
                        table_item.setBackground(Qt.GlobalColor.red)
                        table_item.setForeground(Qt.GlobalColor.white)

                    if column == lastColumn and value:
                        if 0 < flow < 100 * 10e2:
                            table_item.setBackground(Qt.GlobalColor.darkRed)
                            table_item.setForeground(Qt.GlobalColor.white)

                        elif flow > 100 * 10e3:
                            table_item.setBackground(Qt.GlobalColor.darkMagenta)
                            table_item.setForeground(Qt.GlobalColor.white)

                        if "\u2705" in values[0]:
                            table_item.setBackground(Qt.GlobalColor.darkGreen)
                            table_item.setForeground(Qt.GlobalColor.white)

                    if column >= amountColumn:
                        table_item.setFlags(Qt.ItemFlag.ItemIsEnabled)

                    if "___" in values[0]:
                        table_item.setBackground(Qt.GlobalColor.darkBlue)
                        table_item.setForeground(Qt.GlobalColor.white)

                        if column:
                            table_item.setFlags(Qt.ItemFlag.NoItemFlags)

        self.resizeRowsToContents()

        self.blockSignals(False)
        self.item_updated.emit()

    def showEvent(self, _):
        self.updateItems()
