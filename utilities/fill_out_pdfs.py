import json
from pypdf import PdfReader, PdfWriter


def fill_out_pdfs(pdf_file: str, pa_filled_form: str):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    fields = reader.get_fields()
    with open(pa_filled_form, "r") as file:
        data_dict = json.load(file)
    count = 0
    print(pa_filled_form.split("_")[0])
    if fields:
        index = 0
        print(data_dict.keys())
        print(fields.keys())
        # for field_name, field_info in fields.items():
        #     print(field_name)
        #     print(field_info)
        # count += 1
        # if count == 10:
        #     exit(0)
        # for key, value in field_info.items():
        #     if key in:
        #             print(value)
        #         count += 1
        #     index += 1
        #     if index == 20:
        #         exit(0)

        # print(data_dict)
        # return "predefined"
    # elif any("/Annots" in page for page in reader.pages):
    #     return "existing"
    # else:
    #     return "static"


if __name__ == "__main__":
    pass
