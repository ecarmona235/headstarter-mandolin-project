from mistralai import Mistral
import os
import json


MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def map_pa_form(pdf_file: str, extracted_fields: str) -> json:
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
                    "text": "You are provided with:\n\n1. A JSON object representing a field map extracted from a PDF using PyPDF.\n2. The original PDF document from which this map was generated.\n\nYour goals:\n- Review the input map for accuracy and completeness.\n- If any visible form fields are missing, detect them using OCR and append them to the map.\n\nFor each field (existing or newly added):\n- Add a `/d` key containing a concise, human-readable description of the field, inferred from `/TU`, `/T`, or its visual context.\n- If the field is a checkbox or radio button (`\"/FT\": \"/Btn\"`), make the description action-oriented (e.g., “Check if patient is diabetic”).\n- If the field exists only visually but has no interactive field properties (e.g. a label and a line), treat it as a non-interactive field and append it using OCR-detected position.\n  - Include these keys:\n```json\n\"/position\": {\n  \"x\": <number>,\n  \"y\": <number>,\n  \"width\": <number>,\n  \"height\": <number>,\n  \"page\": <number>\n}\n```\n  - You may omit interactive-only keys like `/FT` or `/Ff` for visual-only fields.\n\n Requirements:\n- Do **not** modify existing field keys (like `/T`, `/FT`, `/Ff`, `/TU`, `/V`).\n- Do **not** rename or remove fields.\n- Add only `/d` and `/position` where necessary.\n\n Return:\n- A single valid JSON object representing the updated field map with descriptions.\n- Do not return explanations, markdown formatting, or commentary—**JSON only**."
                },
                {
                    "type": "text",
                    "text": f"{json.dumps(extracted_fields, default=str)}",
                },
                {"type": "document_url", "document_url": signed_url.url},
            ],
        }
    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print("Response", chat_response.choices[0].message.content)
    return chat_response.model_dump_json()


if __name__ == "__main__":
    pass
