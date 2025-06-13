from mistralai import Mistral
import os
import json

MISRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-small-latest"
CLIENT = Mistral(api_key=MISRAL_API_KEY)


def fill_pa_json_from_referral(pdf_file: str, pa_json: str) -> json:
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
    with open(pa_json, "r", encoding="UTF-8") as input_json_file:
        json_content = json.load(input_json_file)
    print("sending prompt")
    # pylint: disable=line-too-long
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The Text below is your previous response. It contains input fields you extracted from another document.",
                },
                {"type": "text", "text": f"[INST] {json.dumps(json_content)},  [INST]"},
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
                    "text": "Review the completed file for correctness, then return it in json format filled out. In the json return a subsection with the key left_blank: [ list containing all the keys of the input fields left blank in a sentence that describes the location of where the input field is on the document. ] ",
                },
            ],
        }
    ]

    chat_response = CLIENT.chat.complete(model=MODEL, messages=messages)
    print("Response", chat_response.choices[0].message.content)
    return chat_response.model_dump_json()


if __name__ == "__main__":
    pass