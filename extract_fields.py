from pypdf import PdfReader


def extract_map(pdf_file: str):
    """_summary_

    Args:
        pdf_file (str): _description_
        json_filled_form (str): _description_
    """
    reader = PdfReader(pdf_file)
    # writer = PdfWriter()
    fields = reader.get_fields()
    return fields
