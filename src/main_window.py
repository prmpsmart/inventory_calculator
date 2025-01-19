from .history_dialog import *
from .table_widget import TableWidget
from .field import Field


class MainWindow(QWidget):
    instances = []

    def __init__(self, parent: "MainWindow" = None, file: str = ""):
        super().__init__()

        self.setMinimumSize(700, 500)

        self._parent = parent
        self.saved = True

        self.inventory: Inventory = Inventories.open_inventory(file)

        main_window_layout = QVBoxLayout(self)
        main_window_layout.setSpacing(10)

        inventory_actions_layout = QHBoxLayout()
        main_window_layout.addLayout(inventory_actions_layout)

        recent_inventories_button = QPushButton("Recents")
        recent_inventories_button.setToolTip("Recent Inventories")
        recent_inventories_button.clicked.connect(self.on_recent_inventories)
        inventory_actions_layout.addWidget(recent_inventories_button)

        new_inventory_button = QPushButton("New")
        new_inventory_button.setToolTip("New Inventory")
        new_inventory_button.clicked.connect(self.on_new_inventory)
        inventory_actions_layout.addWidget(new_inventory_button)

        open_inventory_button = QPushButton("Open")
        open_inventory_button.setToolTip("Open Inventory")
        open_inventory_button.clicked.connect(self.on_open_inventory)
        inventory_actions_layout.addWidget(open_inventory_button)

        save_inventory_button = QPushButton("Save")
        save_inventory_button.setToolTip("Save Inventory")
        save_inventory_button.clicked.connect(self.on_save_inventory)
        inventory_actions_layout.addWidget(save_inventory_button)

        form_layout = QFormLayout()
        main_window_layout.addLayout(form_layout)

        self.inventory_name_line_edit = QLineEdit()
        form_layout.addRow("Inventory Name:", self.inventory_name_line_edit)
        self.inventory_name_line_edit.textChanged.connect(self.on_edit)


        totals_layout = QHBoxLayout()
        main_window_layout.addLayout(totals_layout)

        totals_layout.setSpacing(30)
        totals_layout.addStretch()

        self.total_items_field = Field("Items")
        totals_layout.addWidget(self.total_items_field)

        self.total_amount_field = Field("Amount")
        totals_layout.addWidget(self.total_amount_field)


        items_layout = QHBoxLayout()
        main_window_layout.addLayout(items_layout)

        items_actions_layout = QVBoxLayout()
        items_layout.addLayout(items_actions_layout)

        add_item_button = QPushButton("Add")
        add_item_button.setToolTip("Add Item")
        add_item_button.clicked.connect(self.on_add_item)
        items_actions_layout.addWidget(add_item_button)

        insert_item_button = QPushButton("Insert")
        insert_item_button.setToolTip("Insert Item")
        insert_item_button.clicked.connect(self.on_insert_item)
        items_actions_layout.addWidget(insert_item_button)

        remove_item_button = QPushButton("Remove")
        remove_item_button.setToolTip("Remove Item")
        remove_item_button.clicked.connect(self.on_remove_item)
        items_actions_layout.addWidget(remove_item_button)

        move_item_up_button = QPushButton("Move Up")
        move_item_up_button.setToolTip("Move Item Up")
        move_item_up_button.clicked.connect(self.on_move_item_up)
        items_actions_layout.addWidget(move_item_up_button)

        move_item_down_button = QPushButton("Move Down")
        move_item_down_button.setToolTip("Move Item Down")
        move_item_down_button.clicked.connect(self.on_move_item_down)
        items_actions_layout.addWidget(move_item_down_button)

        items_actions_layout.addStretch()

        items_table = TableWidget(self.inventory)
        items_layout.addWidget(items_table, 1)

    def on_recent_inventories(self):
        history = os.listdir(".")

        if history:
            self.history_dialog = HistoryDialog(self, history)
            self.history_dialog.list_widget.itemClicked.connect(
                self.recent_inventory_selected
            )
            self.history_dialog.show()
        else:
            QMessageBox.information("No recents", "There is no recent inventories.")

    def recent_inventory_selected(self, item: QListWidgetItem):
        self.history_dialog.close()
        self.on_new_inventory(item.text())

    def on_new_inventory(self, file: str = ""):
        try:
            main_window = MainWindow(self, file)
            main_window.show()
            MainWindow.instances.append(main_window)

        except Exception as e:
            print(e)
            QMessageBox.warning(
                self,
                "Invalid inventory file",
                "Choose a valid inventory file.",
            )

    def on_open_inventory(self):
        file, _ = QFileDialog.getOpenFileName(self, *FILE_DIALOG_PARAMS)
        if file:
            self.on_new_inventory(file)

    def on_save_inventory(self):
        if not self.inventory.file:
            file, _ = QFileDialog.getSaveFileName(self, *FILE_DIALOG_PARAMS)
            self.inventory.file = file

        self.save_inventory()

    def on_add_item(self): ...

    def on_insert_item(self): ...

    def on_remove_item(self): ...

    def on_move_item_up(self): ...

    def on_move_item_down(self): ...

    def mouseDoubleClickEvent(self, _):
        self.close()

    @property
    def app(self):
        return QApplication.instance()

    def save_inventory(self):
        self.inventory.save()
        self.saved = True
        self.setTitle()

    def on_edit(self):
        self.saved = False
        self.setTitle()

    def setTitle(self):
        file = ""
        if self.inventory:
            file += " ("
            if not (self.inventory.file and self.saved):
                file += "*"
            else:
                file += self.inventory.file

            file += ")"

        self.setWindowTitle(f"Inventory Calculator{file}")

    def showEvent(self, _):
        if self._parent:
            parent_main_window_geometry: QRect = self._parent.geometry()
            new_main_window_geometry = parent_main_window_geometry.adjusted(
                10, 30, 0, 0
            )
            self.setGeometry(new_main_window_geometry)

        self.setTitle()
