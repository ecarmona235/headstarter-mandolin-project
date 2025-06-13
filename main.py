"""Need to fill out later"""

import json
import os
# import time
# import extract_pa_form
# import fill_pa_json 
# import extract_form
from fillpdf import fillpdfs


def fill_pdf_form(pdf_file: str, json_filled_form: str):
    """_summary_

    Args:
        pdf_file (str): _description_
        json_filled_form (str): _description_
    """
    # Load JSON data
    with open(json_filled_form, "r") as json_file:
        data_dict = json.load(json_file)  # JSON keys should match PDF field names

    # Fill the PDF form
    fillpdfs.write_fillable_pdf(pdf_file, "1_filled_form.pdf", data_dict)

    # Optional: Flatten the PDF to make fields non-editable
    fillpdfs.write_fillable_pdf("form.pdf", "flattened_form.pdf", data_dict, flatten=True)
    











if __name__ == "__main__":

    PA_list = [
        "Input Data/Adbulla/PA.pdf",
        "Input Data/Akshay/pa.pdf",
        "Input Data/Amy/PA.pdf",
    ]
    referral__packages = [
        "Input Data/Adbulla/referral_package.pdf",
        "Input Data/Akshay/referral_package.pdf",
        "Input Data/Amy/referral_package.pdf",
    ]

    # for pa_path in PA_list:
    #     cur_patient = pa_path.split("/")[1]
    #     CUR_FORM = "PA"
    #     json_response = extract_pa_form(pdf_file=pa_path)
    #     time.sleep(2)
    #     # # Save to a JSON file
    #     print("Saving PA form for: ", cur_patient)
    #     with open(f"{cur_patient}{CUR_FORM}.json", "w", encoding="UTF-8") as json_file:
    #         json.dump(json_response, json_file)  # type: ignore
    # for referral_package in referral__packages:
    #     cur_patient = referral_package.split("/")[1]
    #     CUR_FORM = "First_attempt"
    #     json_response = fill_pa_json_from_referral(
    #         pdf_file=referral_package, pa_json=f"{cur_patient}PA.json"
    #     )
    #     time.sleep(2)
    #     # Save to a JSON file
    #     print("Saving first try at input fields filled out for: ", cur_patient)
    #     with open(f"{cur_patient}_{CUR_FORM}.json", "w", encoding="UTF-8") as json_file:
    #         json.dump(json_response, json_file, indent=4)  # type: ignore
    #
    #
    # extract_form("Adbulla_First_attempt.json")
    # extract_form("Akshay_First_attempt.json")
    # extract_form("Amy_First_attempt.json")
    
    
    