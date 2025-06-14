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
                    "text": "You are given an input filed map in the form of a json and the original pdf of which the map was extracted from, check map for correctness, if any input fields are missing correct it, on the follow up response you will be filling in the values. Maintain the input map as it will be used to fill in the form at a later time. Return your response in a json that will be returned to you in the next request. Format the json however it will be best for you to read and fill it in on the next request but maintain the map.",
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
