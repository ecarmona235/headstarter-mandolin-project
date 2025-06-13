"""Need to fill out later"""

import json
import os
from extract_fields import extract_map
from fill_pa_json import fill_pa_json_from_referral
from map_pa_form import map_pa_form

# import time
# import extract_pa_form
# import fill_pa_json
# import extract_form


def controller():
    for subfolder in os.listdir("Input Data"):
        cur_patient = ""
        pa_form = ""
        referral_pdf = ""
        extract_fields = ""
        pa_form_map = {}
        first_response = {}
        subfolder_path = os.path.join("Input Data", subfolder)

        if os.path.isdir(subfolder_path):  # Ensure it's a subfolder
            cur_patient = subfolder
            print(cur_patient)
            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)
                if os.path.isfile(file_path):  # Ensure it's a file
                    if "PA_Copy" in file_name:
                        pa_form = file_name
                    elif "referral" in file_name:
                        referral_pdf = file_name
        print(pa_form)
        extract_fields = extract_map(pa_form)
        if len(extract_fields) > 0:
            first_response = map_pa_form(
                pdf_file=pa_form, extracted_fields=extract_fields
            )
            filled_input_fields = fill_pa_json_from_referral(
                pdf_file=referral_pdf,
                pa_map=extract_fields,
                first_response=first_response,
            )
            with open(
                f"Output Data/{cur_patient}_finalForm.json", "w", encoding="UTF-8"
            ) as json_file:
                json.dump(filled_input_fields, json_file)  # type: ignore

        else:
            first_response = None  # Static form


if __name__ == "__main__":
    controller()
