from mistralai import Mistral
import os
import json

MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def fill_pa_static_json_from_referral(pdf_file: str, first_response: str) -> json:
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
                    "text": 'You are now provided with a new document. Your task is to extract values from it to populate the previously extracted static input field map.\n\nInstructions:\n- Use only information explicitly found in the document.\n- For each entry in the existing field map, fill in the value by updating the `"value"` key.\n- Do not modify any of the existing keys or their formatting (e.g., `name`, `type`, `x`, `y`, `width`, `height`, `page`).\n- Do not add or remove any fields.\n- If a value cannot be confidently extracted from the document, leave `"value": ""` and log an explanation in the final section.\n\nReturn only one JSON object in this format:\n\n```json\n{\n  "fields": [\n    {\n      "name": "Full Name",\n      "type": "text",\n      "x": 150,\n      "y": 720,\n      "width": 200,\n      "height": 20,\n      "page": 1,\n      "value": "John Doe"\n    },\n    ...\n  ],\n  "left_blank": {\n    "<field name>": {\n      "reason": "<why this value could not be extracted>",\n      "location": {\n        "page": X,\n        "x": Y,\n        "y": Z\n      }\n    }\n  }\n}\n\nImportant:\n- Return valid JSON only.\n- Keep the object and array structure exactly the same as in the previous response.',
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
