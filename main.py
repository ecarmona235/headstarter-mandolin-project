"""Need to fill out later"""

import json
import os
# import time
from mistralai import Mistral


MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def fill_pa_json_from_referral(pdf_file: str)-> json:
    """_summary_

    Args:
        pdf_file (str): _description_

    Returns:
        json: _description_
    """
    return pdf_file


def extract_pa_form(pdf_file: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_): _description_

    Returns:
        json: _description_
    """
    print("Uploading pdf")
    uploaded_pdf = CLIENT.files.upload(
        file={
            "file_name": pdf_file,
            "content": open(file=pdf_file, mode="rb"),
        },
        purpose="ocr",
    )
    print("Signing pdf")
    signed_url = CLIENT.files.get_signed_url(file_id=uploaded_pdf.id)
    print("sending prompt")
    # pylint: disable=line-too-long
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all input fields from document and return a json. Ensure it is formatted so that on a follow up question you can use it to extract the information from a larger document that will be sent to you after this.",
                },
                {"type": "document_url", "document_url": signed_url.url},
            ],
        }
    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print("Response", chat_response.choices[0].message.content)
    return chat_response.model_dump_json()


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
    #     CUR_FORM = "refereral_package"
    #     json_response = extract_pa_form(pdf_file=referral_package)
    #     time.sleep(2)
    #     # # Save to a JSON file
    #     print("Saving PA filled out for: ", cur_patient)
    #     with open(f"{cur_patient}{CUR_FORM}.json", "w", encoding="UTF-8") as json_file:
    #         json.dump(json_response, json_file)  # type: ignore
