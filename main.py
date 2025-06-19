"""Need to fill out later"""

import json
from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
import logging
from pydantic import BaseModel, Field
from utilities.extract_fields import extract_map


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
        subfolder_path = os.path.join(input_folder, subfolder)
        cur_patient = subfolder
        if cur_patient != "Akshay":
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
        pa_path = f"{input_folder}/{cur_patient}/{pa_form}"
        referral_path = f"{input_folder}/{cur_patient}/{referral_pdf}"
        extracted_map = extract_map(pa_path)
        # call async task loop
        # will call get prompt in order
        # call gemini and mistral
        #   extract to fill and left blank
        #   write pdf
        #   Write text or mark up
        # complete after every patient
        print(extracted_map)
        # if len(extracted_map) > 0:
        #     format_map(pdf_file=pa_path, prompt="prompt")

    # write MarkDown


if __name__ == "__main__":
    if INPUT_FOLDER is None:
        print("Input not found")
        exit(0)
    if OUTPUT_FOLDER is None:
        print("Output not found")
        exit(0)
    controller(INPUT_FOLDER, OUTPUT_FOLDER)
