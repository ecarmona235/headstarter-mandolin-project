import json
import fitz
from io import BytesIO

from utilities.ExtractFields import extract_map


def prepare_interactive_pdfs(filled_out_map, out_path, pa_path):
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


def prepare_static_pdfs(filled_out_map, out_path, pa_path):
    # Write new function using fitz to fill interactive pdfs

    doc = fitz.open(pa_path)

    for annotation in filled_out_map:
        print(annotation)
        if annotation["answer"] != "":
            page = doc[(annotation["page"] - 1)]
            x0, y0, x1, y1 = annotation["bbox"]
            field_type = annotation["field_type"]
            answer = annotation["answer"]
            print(x0  < x1 and y0 < y1)

            if field_type == "checkbox":
                if ((type(answer) == bool
                    and answer is not None)
                    or answer.lower() in ["yes", "true", "checked", "1", "x"]
                ):
                    # Draw an X in the box
                    page.draw_line((x0, y0), (x1, y1), color=(0, 0, 0))
                    page.draw_line((x0, y1), (x1, y0), color=(0, 0, 0))
            else:
                # Use insert_textbox to place text inside the box
                # page_height = page.rect.height
                # Convert from top-left origin system to bottom-left:
                # converted_y0 = page_height - y1
                page.insert_text(
                    fitz.Point(x=x0, y=y0),
                    answer,
                    fontsize=10,
                    fontname="helv",
                    color=(0, 0, 0),
                )  # align=0: left

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
