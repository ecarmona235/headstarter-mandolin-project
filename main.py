"""Need to fill out later"""

import json
from pathlib import Path
from dotenv import load_dotenv
import os
from google import genai
import asyncio
import logging
from pydantic import BaseModel, Field
from utilities.extract_fields import extract_map

# from utilities.fill_pa_static_json import fill_pa_static_json_from_referral
# from utilities.fill_out_pdfs import prepare_filled_pdf_fields

# from utilities.extract_form import extract_form
# from utilities.map_pa_form import map_pa_form
# from utilities.map_static_pa_form import map_static_pa_form
# import time


load_dotenv()
INPUT_FOLDER = os.getenv("INPUT_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s -%(message)s"
)
logger = logging.getLogger(__name__)


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
        if cur_patient == "Amy":
            continue
        if not os.path.exists(f"{output_folder}/{cur_patient}"):
            os.makedirs(f"{output_folder}/{cur_patient}")
        if os.path.isdir(subfolder_path):  # Ensure it's a subfolder
            cur_patient = subfolder
            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)
                if os.path.isfile(file_path):  # Ensure it's a file
                    if "PA_Copy" in file_name:
                        pa_form = file_name
                    elif "referral" in file_name:
                        referral_pdf = file_name
        print(extract_map(f"{input_folder}/{cur_patient}/{pa_form}"))

    # write MarkDown


if __name__ == "__main__":
    if INPUT_FOLDER is None:
        print("Input not found")
        exit(0)
    if OUTPUT_FOLDER is None:
        print("Output not found")
        exit(0)
    controller(INPUT_FOLDER, OUTPUT_FOLDER)
