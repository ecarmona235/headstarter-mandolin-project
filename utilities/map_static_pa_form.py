from mistralai import Mistral
import os
import json

MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def map_static_pa_form(pdf_file: str) -> json:
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
                    "text": "analyze a PDF document and extract all input fields along with their coordinates. Your task is to return a structured JSON map containing: **Field Name** (`name`): The label or identifier of the input field.*Field Type** (`type`): The type of input (e.g., text box, checkbox, dropdown). **Coordinates** (`x`, `y`): The position of the field on the page.**Field Dimensions** (`width`, `height`): The size of the field. **Page Number** (`page`): The page where the field is located. **Value** (' ') : Empty field to fill in value. This The value fill will be filled by you on a later response when you are given another document to extract the information from.",
                },
                {"type": "document_url", "document_url": signed_url.url},
            ],
        }
    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print("Response")
    return chat_response.model_dump_json()


if __name__ == "__main__":
    pass
