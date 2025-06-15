from mistralai import Mistral
import os
import json

MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def fill_pa_json_from_referral(pdf_file: str, first_response: str) -> json:
    """_summary_

    Args:
        pdf_file (str): _description_

    Returns:
        json: _description_
    """
    print("Uploading pdf 1")
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
                    "text": "You are provided with:\n1. A previously structured field map in JSON form.\n2. The corresponding PDF document containing the source data.\n\nYour task is to populate values for each field using **only the visible data** in the document.\n\n Instructions:\n- If the field includes `\"/FT\": \"/Tx\"`, extract the relevant text and populate `\"/V\"` with the corresponding value.\n- If the field includes `\"/FT\": \"/Btn\"` (checkbox or radio):\n  - If selected, assign `\"/V\"` the matching on-state (e.g., `\"/Yes\"`, `\"/On\"`).\n  - If unselected or unclear, leave `\"/V\"` blank or as `\"/Off\"`.\n- If the field has no interactive structure but includes a `/position` block (from OCR), extract the visible nearby value and assign it to `\"/V\"`.\n- If a value cannot be confidently extracted, leave `\"/V\": \"\"` and include the field in a `left_blank` object at the end.\n\n Response Format:\nReturn a single JSON object where each field retains its original structure and keys, with `\"/V\"` populated accordingly.\nAt the end, add:\n```json\n\"left_blank\": {\n  \"<field_key>\": {\n    \"reason\": \"<why this value is missing>\",\n    \"location\": {\n      \"page\": X,\n      \"x\": Y,\n      \"y\": Z\n    }\n  }\n}\n```\n\n Do not:\n- Rename, restructure, or omit original field entries.\n- Introduce semantic key names like 'patient_name'.\n- Return commentary, markdown, or anything other than valid JSON."
                },
                {
                    "type": "text",
                    "text": f"[INST] {json.dumps(first_response)},  [INST]",
                },
                {"type": "document_url", "document_url": signed_url.url},
            ],
        }
    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print(
        "Response sent",
    )
    return chat_response.model_dump_json()


if __name__ == "__main__":
    pass
