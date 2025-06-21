import json
import fitz
from io import BytesIO

from utilities.ExtractFields import extract_map


def prepare_filled_pdf_fields(filled_out_map, out_path, pa_path):
    # Write new function using fitz to fill interactive pdfs
    extracted_map = extract_map(pa_path)

    answer_map = {(ans["page"], ans["name"]): ans["answer"] for ans in filled_out_map}
    for page_fields in extracted_map.values():
        for fld in page_fields:
            ans = answer_map.get((fld["page"], fld["name"]))

            if ans is None:
                continue
            fld["value"] = ans

    flat_fields = {}
    for page_fields in extracted_map.values():
        for field in page_fields:
            flat_fields[field["name"]] = field
    doc = fitz.open(pa_path)
    for page in doc:
        for w in page.widgets() or []:
            data = flat_fields.get(w.field_name)
            if data is None:
                continue
            val = data["value"]
            if w.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:  # if  check box
                checked = bool(val) and str(val).lower() not in {
                    "off",
                    "0",
                    "false",
                    "no",
                }
                w.field_value = "Yes" if checked else "Off"
            else:  # if text
                w.field_value = str(val)
            w.update()

    if out_path:
        doc.save(out_path, deflate=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    else:  # if not saving pdf and sending it back
        buf = BytesIO()
        doc.save(buf, deflate=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        buf.seek(0)
        return buf
    doc.close()


if __name__ == "__main__":
    pass
