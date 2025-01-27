import xlsxwriter, os
import xlsxwriter.format
import xlsxwriter.worksheet
from src.commons import COLUMNS
from src.inventory import Inventory


def inventoryToExcel(file: str) -> str:
    basename = os.path.splitext(file)[0]
    path = f"{basename}.xlsx"

    inventory = Inventory(file=file)

    wb = xlsxwriter.Workbook(path)
    sheet = wb.add_worksheet("Inventory")

    for index, header in enumerate(COLUMNS):
        sheet.write(0, index, header)

    flow = 0
    for row, item in enumerate(inventory.items):
        flow += item.amount
        row += 1

        if "___" in item.name:
            sheet.merge_range(row, 0, row, 4, item.name)

        else:
            for column, value in enumerate(
                [
                    item.name,
                    item.count or "",
                    item.price or "",
                    item.amount or "",
                    flow if item.amount else "",
                ]
            ):
                sheet.write(row, column, value)

    print(f"Inventory JSON: {file}\nInventory Excel: {path}")

    wb.close()

    return path


file = r"C:\Users\USER\Desktop\Workspace\PRMPSmart\inventory_calculator\cash_flow_2025copy.json"

excel_file = inventoryToExcel(file)

os.system(excel_file)
