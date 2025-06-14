"""Need to fill out later"""

import json
from dotenv import load_dotenv
import os
from utilities.extract_fields import extract_map
from utilities.extract_form import extract_form
from utilities.fill_pa_json import fill_pa_json_from_referral
from utilities.map_pa_form import map_pa_form
from utilities.map_static_pa_form import map_static_pa_form
import time


load_dotenv()
INPUT_FOLDER = os.getenv("INPUT_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")


def controller(input_folder, output_folder):
    input_folder = input_folder
    output_folder = output_folder
    for subfolder in os.listdir("Input Data"):
        pa_form = ""
        referral_pdf = ""
        extract_fields = ""
        first_response = {}
        subfolder_path = os.path.join(input_folder, subfolder)
        cur_patient = subfolder
        print(cur_patient)

        if os.path.isdir(subfolder_path):  # Ensure it's a subfolder
            cur_patient = subfolder
            if cur_patient == "Adbulla":
                continue
            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)
                if os.path.isfile(file_path):  # Ensure it's a file
                    if "PA_Copy" in file_name:
                        pa_form = file_name
                    elif "referral" in file_name:
                        referral_pdf = file_name

        #     extract_fields = extract_map(f"{input_folder}/{cur_patient}/{pa_form}")
        #     if len(extract_fields) > 0: # Predefined and Exisiting PDF types
        #         with open(
        #             f"temp_files/{cur_patient}_extracted.json", "w", encoding="UTF-8"
        #         ) as json_file:
        #             json.dump(extract_fields, json_file, default=str)  # type: ignore   # Formats mishapened
        #         first_response = map_pa_form(
        #             pdf_file=f"{input_folder}/{cur_patient}/{pa_form}",
        #             extracted_fields=f"temp_files/{cur_patient}_extracted.json",
        #         )
        #         time.sleep(1)
        #         if os.path.exists(f"temp_files/{cur_patient}_extracted.json"):
        #             os.remove(f"temp_files/{cur_patient}_extracted.json")
        #         filled_input_fields = fill_pa_json_from_referral(
        #             pdf_file=f"{input_folder}/{cur_patient}/{referral_pdf}",
        #             first_response=first_response,
        #         )
        #         with open(
        #             f"{output_folder}/{cur_patient}_finalForm.json", "w", encoding="UTF-8"
        #         ) as json_file:
        #             json.dump(filled_input_fields, json_file)  # type: ignore

        #     else:  # static pdfs
        #         first_response = map_static_pa_form(
        #             pdf_file=f"{input_folder}/{cur_patient}/{pa_form}"
        #         )
        #         time.sleep(1)
        #         filled_input_fields = fill_pa_json_from_referral(
        #             pdf_file=f"{input_folder}/{cur_patient}/{referral_pdf}",
        #             pa_map=extract_fields,
        #             first_response=first_response,
        #         )

        #         with open(
        #             f"{output_folder}/{cur_patient}_finalForm.json", "w", encoding="UTF-8"
        #         ) as json_file:
        #             json.dump(filled_input_fields, json_file)  # type: ignore

        # time.sleep(2)
        # extract pdf
        # extract_form(f"{output_folder}/{cur_patient}_finalForm.json")

    # write pdfs
        
    # write MarkDown


if __name__ == "__main__":
    if INPUT_FOLDER is None:
        print("Input not found")
        exit(0)
    if OUTPUT_FOLDER is None:
        print("Output not found")
        exit(0)
    controller(INPUT_FOLDER, OUTPUT_FOLDER)
