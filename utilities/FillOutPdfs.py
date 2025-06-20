import json


def prepare_filled_pdf_fields(structured_data, out_path):
    # Write new function using fitz to fill interactive pdfs
    with open(out_path, "w") as f:
        json.dump(structured_data, f, indent=4)


if __name__ == "__main__":
    pass
