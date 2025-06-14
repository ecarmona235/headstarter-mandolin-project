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
                    "text": "The Text below is your previous response. It contains input fields you formated to be filled from the document below",
                },
                {
                    "type": "text",
                    "text": f"[INST] {json.dumps(first_response)},  [INST]",
                },
                {
                    "type": "text",
                    "text": "Use the document below to extract the necessary information to fill the pdf input space in the format you saved it in. If addresses ensure to not mark the State, City and Zipcode in the address field and instead only use their pertaining fields. ",
                },
                {"type": "document_url", "document_url": signed_url.url},
                {
                    "type": "text",
                    "text": "If you run into conflicts make the best decision you can with the information you have, else leave it blank.",
                },
                {
                    "type": "text",
                    "text": "Review the completed input fields for correctness.In the json have another section with the tittle left_blank: '{' input field tittle left blank : Reason why it was left blank '}' ",
                },
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
