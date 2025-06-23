"""Need to fill out later"""

import json
from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
import logging
from pydantic import BaseModel, Field
from utilities.ExtractFields import extract_map
from utilities.ProcessPatient import process_patient
from utilities.FillOutPdfs import prepare_interactive_pdfs, prepare_static_pdfs
from utilities.WriteMarkdown import dict_to_markdown


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
        # if cur_patient != "Amy":
        #     continue
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
        num, structured_data = asyncio.run(
            process_patient(
                patient=cur_patient, pa_path=pa_path, referral_path=referral_path
            )
        )
        if type(structured_data) == list:
            structured_data = structured_data.pop()
        if "response_dict" in structured_data:
            structured_data = structured_data["response_dict"]
        print("...Writting PDFs and Markdown...")
        with open(f"{output_folder}/{cur_patient}/{cur_patient}_filled_pa.json", "w") as f:
            json.dump(structured_data, f, indent=4)
        fields = structured_data["fields"]
        left_blank = structured_data["left_blank"]
        with open(f"{output_folder}/{cur_patient}/{cur_patient}_filled_pa.json", 'r') as f:
            structured_data = json.load(f)
        if num == 2:
            prepare_static_pdfs(
                filled_out_map=fields,
                out_path=f"{output_folder}/{cur_patient}/{cur_patient}_filled_pa.pdf",
                pa_path=pa_path,
            )
        else:
            prepare_interactive_pdfs(
                filled_out_map=fields,
                out_path=f"{output_folder}/{cur_patient}/{cur_patient}_filled_pa.pdf",
                pa_path=pa_path,
            )

        dict_to_markdown(
            left_blank=left_blank,
            md_path=f"{output_folder}/{cur_patient}/{cur_patient}_left_blank.md",
        )


if __name__ == "__main__":
    if INPUT_FOLDER is None:
        print("Input not found")
        exit(0)
    if OUTPUT_FOLDER is None:
        print("Output not found")
        exit(0)
    controller(INPUT_FOLDER, OUTPUT_FOLDER)
