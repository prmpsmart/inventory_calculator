from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from .inventory import *

FILE_DIALOG_TITLE = "Select inventory file"
JSON_FILE_FORMAT = "JSON (*.json *.JSON)"
FILE_DIALOG_PARAMS = (FILE_DIALOG_TITLE, "", JSON_FILE_FORMAT)

COLUMNS = ["Name", "Count", "Price", "Amount", "Flow"]
COLUMNS_L = [column.lower() for column in COLUMNS]
COLUMNS_TYPE: list[type] = [str, int, float, float]
COLUMNS_NULL = ["", 0, 0.0, 0.0]
