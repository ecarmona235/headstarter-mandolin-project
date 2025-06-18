import json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import IndirectObject, NameObject, TextStringObject
from typing import Dict, List
from pypdf.generic import BooleanObject


def extract_interactive_fields(reader: PdfReader) -> List[dict]:
    """Recursively flattens all terminal interactive fields with /T and /FT"""
    flat_fields = []

    def recurse(obj):
        if isinstance(obj, IndirectObject):
            obj = obj.get_object()
        if "/Kids" in obj:
            for kid in obj["/Kids"]:
                recurse(kid)
        elif "/T" in obj and "/FT" in obj:
            flat_fields.append(obj)

    for field in reader.trailer["/Root"]["/AcroForm"]["/Fields"]:
        recurse(field)

    return flat_fields


def prepare_filled_pdf_fields(
    input_pdf_path: str,
    output_pdf_path: str,
    pa_filled_form: str,
) -> None:
    """
    Populates and flattens interactive fields in the input PDF using source_data.
    Writes the filled PDF to output_pdf_path.
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    with open(pa_filled_form, "r") as file:
        data_dict = json.load(file)

    field_objs = extract_interactive_fields(reader)
    write_data = {}

    for field in field_objs:
        t = field.get("/T")
        tu = field.get("/TU", "").strip(": ")
        ft = field.get("/FT")
        value = data_dict.get(tu) or data_dict.get(t)
        if value is not None and str(value).strip():
            if ft == "/Btn":
                if isinstance(value.get("/V"), str) and value.get("/V").strip():
                    field[NameObject("/V")] = NameObject(value.get("/V"))
                    field[NameObject("/AS")] = NameObject(value.get("/V"))
                else:
                    field[NameObject("/V")] = NameObject("/Off")
                    field[NameObject("/AS")] = NameObject("/Off")
            else:
                field[NameObject("/V")] = TextStringObject(value.get("/V"))
            write_data[t] = field[NameObject("/V")]

    # Apply values
    print(write_data)
    writer.update_page_form_field_values(writer.pages, write_data)

    # # Optional: ReadOnly & Printable flags for each widget
    #
    writer._root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(
        True
    )
    for page in writer.pages:
        if "/Annots" in page:
            for annot_ref in page["/Annots"]:
                annot = annot_ref.get_object()
                if annot.get("/FT") in ["/Tx", "/Btn"]:
                    annot.update({NameObject("/Ff"): 1})
                    annot.update({NameObject("/F"): 4})

    # Output
    with open(output_pdf_path, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    pass
