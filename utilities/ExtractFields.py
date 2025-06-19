import fitz


def extract_map(pdf_file: str) -> dict:
    """Extracts input fields from PA form

    Args:
        pdf_file (str): Path to PA form
    """
    print(pdf_file)
    doc = fitz.open(pdf_file)
    fields = []
    for page_num, page in enumerate(doc, start=1):
        for w in page.widgets() or []:
            field = {
                "name": w.field_name,
                "value": w.field_value,
                "field_type_string": w.field_type_string,
                "field_label": w.field_label,
                "page": page_num,
            }
            fields.append(field)

        # flatted by page
    fields_by_page = {}
    for field in fields:
        page_num = field["page"]
        if page_num not in fields_by_page:
            fields_by_page[page_num] = []
        fields_by_page[page_num].append(field)

    return fields_by_page
