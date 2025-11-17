
from pathlib import Path
from datetime import date
import pypdftk
from PyPDF2 import PdfMerger
import pandas as pd

CSV_PATH = "./data/Inventory.csv"
PDF_TMP_DIR = Path("./tmp")
PDF_TMP_DIR.mkdir(exist_ok=True)
MAX_CATEGORIES_PER_PAGE = 16

def find_serial_number_by_object(object_code, df):
    serial = df.loc[df["object_code"] == object_code, "serial_number"]
    return serial.values[0] if not serial.empty else ""

def get_inventory_items(project_name):
    df = pd.read_csv(CSV_PATH, dtype=str)
    return [row for _, row in df[(df["inventoried"] == "TRUE")].iterrows()]

def prepare_page_data(category_groups, page_type="first"):
    data = {}

    if page_type == "first" and category_groups:
        first_category = category_groups[0]["items"][0]["category_name"]
        data["form1[0].Page1[0].TO[0]"] = first_category
        data["form1[0].Page1[0].PUBDATE[0]"] = date.today().strftime("%Y-%m-%d")

    index = 0
    for group in category_groups:
        category = group["category"]
        print(category)
        items_in_category = group["items"]

        # Collect all serial numbers for this category
        serial_numbers = [
            item["serial_number"] for item in items_in_category
            if item.get("serial_number")
        ]
        serial_numbers_str = ", ".join(serial_numbers) if serial_numbers else ""

        # Quantity is the number of items in the category
        qty = len(items_in_category)

        if page_type == "first":
            data[f"form1[0].Page1[0].STOCKNRA{f'_{index}' if index != 0 else ''}[0]"] = serial_numbers_str
            data[f"form1[0].Page1[0].ITEMDESA{f'_{index}' if index != 0 else ''}[0]"] = category
            data[f"form1[0].Page1[0].QTYAUTHA{f'_{index}' if index != 0 else ''}[0]"] = qty
        else:
            data[f"form1[0].Page2[0].STOCKNRB{f'_{index}' if index != 0 else ''}[0]"] = serial_numbers_str
            data[f"form1[0].Page2[0].ITEMDESB{f'_{index}' if index != 0 else ''}[0]"] = category
            data[f"form1[0].Page2[0].QTYAUTHB{f'_{index}' if index != 0 else ''}[0]"] = qty

        index += 1

    return data

def generate_and_combine_pdfs(project_name, page_data):
    input_first_page = Path("pdfs/AnnexE.pdf")
    input_continuation_page = Path("pdfs/AnnexE_ContinuationPage.pdf")
    output_pdfs = []

    for i, data in enumerate(page_data):
        output_pdf_path = PDF_TMP_DIR / f"FilledAnnexE_{project_name}_page_{i+1}.pdf"
        input_pdf = input_first_page if i == 0 else input_continuation_page
        pypdftk.fill_form(str(input_pdf), data, str(output_pdf_path), flatten=True)
        output_pdfs.append(output_pdf_path)

    final_pdf = PDF_TMP_DIR / f"FilledAnnexE_{project_name}.pdf"
    merger = PdfMerger()
    for pdf in output_pdfs:
        merger.append(str(pdf))
    merger.write(str(final_pdf))
    merger.close()
    return final_pdf

def generate_pdf(project_name):
    df = pd.read_csv(CSV_PATH, dtype=str)
    inventory_items = df[(df["inventoried"] == "TRUE")]

    # Group by category
    grouped = inventory_items.groupby("category_name")
    print(grouped)
    category_groups = [{"category": cat, "items": items.to_dict("records")} for cat, items in grouped]
    print(category_groups)
    # Pagination
    pages = []
    current_page = []
    serial_no_count = 0
    non_serial_count = 0

    for group in category_groups:
        serial_in_category = [find_serial_number_by_object(x["object_code"], df) for x in group["items"]]
        is_serial = any(s for s in serial_in_category)
        serial_no_count += (len(serial_in_category) - 1) if is_serial and len(serial_in_category) > 1 else 0
        non_serial_count += 1 if not is_serial and len(serial_in_category) == 1 else 0

        if len(current_page) + serial_no_count + non_serial_count - 1 <= MAX_CATEGORIES_PER_PAGE:
            current_page.append(group)
        else:
            pages.append(current_page)
            current_page = [group]
            serial_no_count = 0
            non_serial_count = 0
    if current_page:
        pages.append(current_page)

    # Prepare page data
    page_data = [prepare_page_data(pg, page_type="first" if i == 0 else "continuation") for i, pg in enumerate(pages)]
    final_pdf = generate_and_combine_pdfs(project_name, page_data)


    return final_pdf