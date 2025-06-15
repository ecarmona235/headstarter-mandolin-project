import json
from pypdf import PdfReader



def fill_out_pdfs(pdf_file: str, pa_filled_form: str):
    reader = PdfReader(pdf_file)
    fields = reader.get_fields()
    with open(pa_filled_form, "r") as file:
        data_dict = json.load(file)
    count = 0
    print(pa_filled_form.split("_")[0])
    print("/n")
    # print(fields)
    # if fields:
    #     for field_name, field_info in fields.items():
    #         print(field_name)
    #         for key, value in field_info.items():
    #             if key == '/TU':
    #                 print(value, " ")
            #     # here is where you have the fields 
            #     if key in data_dict or field_name in data_dict:
            #         count += 1
        # fillpdfs.write_fillable_pdf(pdf_file, f"{pa_filled_form.split("_")[0]}_filled.pdf", data_dict)
        # print(data_dict)
        # print(count)
        # return "predefined"
    # elif any("/Annots" in page for page in reader.pages):
    #     return "existing"
    # else:
    #     return "static"


if __name__ == "__main__":
    pass
