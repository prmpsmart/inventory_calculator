import xlsxwriter, os, win32com.client, datetime
import xlsxwriter.format
import xlsxwriter.worksheet
from src.commons import COLUMNS
from src.inventory import Inventory

COLUMNS = ["Date", *COLUMNS]

naira = "$"
naira = "₦"


def inventory_to_excel(file: str) -> str:
    dirname = os.path.dirname(file)
    basename = os.path.splitext(os.path.basename(file))[0]

    dt = datetime.datetime.now().isoformat("T").replace(":", ".")
    date = dt.split("T")[0]

    os.makedirs(date, exist_ok=True)

    path = f"{dirname}/{date}/{basename}_{dt}.xlsx"

    inventory = Inventory(file=file)

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet("Inventory")

    worksheet.set_column("A:A", 10)
    worksheet.set_column("B:B", 33.57)
    worksheet.set_column("C:C", 6)
    worksheet.set_column("D:F", 15)
    if m := 0.25:
        worksheet.set_margins(m, m, m, m)
    worksheet.set_paper(9)

    # Define cell formats
    title_format = workbook.add_format(
        dict(
            bold=True,
            font_size=18,
            align="vcenter",
            bg_color="#a0a0a4",
        )
    )
    title_format.set_align("center")
    header_format = workbook.add_format(
        dict(
            bold=True,
            align="center",
            bg_color="#000000",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    section_header_format = workbook.add_format(
        dict(
            bg_color="#000080",
            has_fill=True,
            font_color="#ffffff",
            bold=True,
            align="center",
        )
    )
    date_format = workbook.add_format(
        dict(
            bg_color="#a0a0a4",
            has_fill=True,
        )
    )
    name_format = workbook.add_format(
        dict(
            bg_color="#a0a0a4",
            has_fill=True,
            text_wrap=True,
        )
    )
    red_name_format = workbook.add_format(
        dict(
            text_wrap=True,
            bg_color="#ff0000",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    count_format = workbook.add_format(
        dict(
            align="center",
            bg_color="#a0a0a4",
            has_fill=True,
        )
    )
    naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="#a0a0a4",
            has_fill=True,
        )
    )
    red_naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="#ff0000",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    green_naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="#008000",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    purple_naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="#800080",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    blue_naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="blue",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    darkRed_naira_format = workbook.add_format(
        dict(
            num_format=f"{naira} #,##0.00",
            bg_color="#800000",
            has_fill=True,
            font_color="#ffffff",
        )
    )
    formats = [
        header_format,
        section_header_format,
        date_format,
        name_format,
        red_name_format,
        count_format,
        naira_format,
        red_naira_format,
        green_naira_format,
        purple_naira_format,
        blue_naira_format,
        darkRed_naira_format,
    ]

    for format in formats:
        format.set_font_name("Times New Roman")
        format.set_font_size(11)
        format.set_border(1)
        format.set_align("vcenter")
        format.set_font_color("white")

    worksheet.merge_range(0, 0, 1, 5, f"{inventory.name}", title_format)

    for index, header in enumerate(COLUMNS):
        worksheet.write(2, index, header, header_format)

    flow = 0
    for row, item in enumerate(inventory.items):
        flow += item.amount
        row += 3

        if "___" in item.name:
            worksheet.merge_range(
                row,
                0,
                row,
                5,
                item.name,
                section_header_format,
            )

        else:
            date_name = item.name.split(" - ", 1)
            if len(date_name) == 1:
                date_name.insert(0, "")
            date, name = date_name
            count = item.count
            price = item.price
            amount = item.amount

            worksheet.write(row, 0, date, date_format)
            worksheet.write(row, 1, name, red_name_format if price < 0 else name_format)
            worksheet.write(row, 2, count, count_format)
            worksheet.write(
                row, 3, price, red_naira_format if price < 0 else naira_format
            )
            worksheet.write(
                row,
                4,
                amount,
                (
                    darkRed_naira_format
                    if amount <= -1 * 10e4
                    else (
                        red_naira_format
                        if amount < 0
                        else (blue_naira_format if amount > 1 * 10e4 else naira_format)
                    )
                ),
            )

            worksheet.write(
                row,
                5,
                flow,
                (
                    green_naira_format
                    if "\u2705" in name
                    else (
                        purple_naira_format
                        if flow > 100 * 10e3
                        else (
                            darkRed_naira_format
                            if 0 < flow <= 100 * 10e2
                            else naira_format
                        )
                    )
                ),
            )

    print(f"Inventory JSON: {file}\nInventory Excel: {path}")

    workbook.close()

    return path


def print_excel_to_pdf(excel_file_path: str) -> str:
    # Ensure the file exists
    if not os.path.exists(excel_file_path):
        print(f"The file {excel_file_path} does not exist.")
        return

    # Open Excel application
    excel = win32com.client.Dispatch("Excel.Application")

    # Open the workbook
    workbook = excel.Workbooks.Open(excel_file_path)

    pdf_output_path = os.path.splitext(excel_file_path)[0] + ".pdf"

    # Set the output PDF path
    try:
        # Export the workbook to PDF
        workbook.ExportAsFixedFormat(0, pdf_output_path)
        print(f"Inventory PDF: {pdf_output_path}")

        workbook.Close(False)
        excel.Quit()

        return pdf_output_path

    except Exception as e:
        print(f"An error occurred: {e}")


json_file = "./selfish_cash_flow.json"

excel_file = inventory_to_excel(json_file)
# os.system(excel_file)

jpdf_file = print_excel_to_pdf(os.path.abspath(excel_file))
# os.system(pdf_file)
