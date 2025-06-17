from httpx import Client
from mistralai import Mistral
import os
import json


MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def map_pa_form(pdf_file: str, referral: str, extracted: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_): _description_

    Returns:
        json: _description_
    """
    print("Uploading pa form")
    pa_form = CLIENT.files.upload(
        file={
            "file_name": referral,
            "content": open(file=pdf_file, mode="rb"),
        },
        purpose="ocr",
    )
    signed_pa_form = CLIENT.files.get_signed_url(file_id=pa_form.id)

    up_referral_pdf = CLIENT.files.upload(
        file={
            "file_name": referral,
            "content": open(file=referral, mode="rb"),
        },
        purpose="ocr",
    )

    signed_referral_pdf = CLIENT.files.get_signed_url(file_id=up_referral_pdf.id)
    print("sending prompt")
    with open(extracted, "r") as f:
        map_str = f.read()
    # pylint: disable=line-too-long
    messages = [
        {
            "role": "system",
            "content": 'You are given:\n1. A Preapproval Form PDF that must be filled using extracted data.\n2. A Referral Packet PDF, which contains the visible source data needed to populate the form.\n3. A field map extracted from the Preapproval Form using PyPDF, provided as a JSON structure.\n\nYour goal is to generate a fully populated JSON field map to be passed into a PyPDF pipeline for form filling. This map should preserve the structure of the input field map and include visual overlay instructions for fields that are missing from the map.\n\n PRESERVE STRUCTURE\n- Keep the structure of all fields in the input map intact—do not modify or delete any existing keys (e.g., `/T`, `/FT`, `/TU`, `/Ff`, `/AA`, `/_States_`, `/Kids`, etc.).\n- Do not combine or collapse multi-part fields (e.g., MM/DD/YYYY components must remain separate).\n\n MAP VALUES FROM SOURCE\nFor each field object in the map:\n- Try to match its `/TU` (tooltip) exactly (case-sensitive) with a label in the Referral Packet. If matched, set the field’s `/V` value accordingly.\n- If `/TU` doesn’t match, try matching its `/T`.\n- If no confident match is found, set `/V` to `""` and log it under `"left_blank"`.\n\n REPORT MISSING VALUES\nAt the end of your output, append:\n```json\n"left_blank": {\n  "<field_key>": {\n    "/TU": "<that field’s TU>",\n    "reason": "reason for why its left blank"\n, "field description" : "Description of field },\n  ...\n}\n```\nInclude every field from the map with a blank `/V`.\n\n ADD VISUAL OVERLAY FIELDS\nIf you discover any data in the Referral Packet that is not linked to a field in the map, append a new object to a top-level `"missing_fields"` array. This array contains instructions for text overlay to simulate a filled form field:\n```json\n"missing_fields": [\n  {\n    "field": "description or label of missing field",\n    "type": "text",\n    "x": <number>,\n    "y": <number>,\n    "width": <number>,\n    "height": <number>,\n    "page": <number>,\n    "value": "John Doe"\n  },\n  ...\n]\n```\nOnly include fields truly absent from the PyPDF map.\n\n FINAL OUTPUT\nReturn one single valid JSON object:\n- Preserving all original map structure\n- With `/V` values populated for matched fields\n- With `"left_blank"` for unmatched ones\n- With `"missing_fields"` for new visual-only overlays\n\nNo markdown, no commentary—return valid JSON only.',
        },
        {
            "role": "user",
            "content": "Use these two forms"
            + f"- form A: file‐ID {signed_pa_form}\n"
            + f"- form B: file‐ID {signed_referral_pdf}\n"
        },
        {"role": "user",
            "content": f"Here is the JSON map: + {map_str}"}

    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print("Response sent")
    return chat_response.model_dump_json()


if __name__ == "__main__":
    pass
