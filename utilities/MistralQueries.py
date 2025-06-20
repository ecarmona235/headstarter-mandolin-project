import asyncio
from mistralai import Mistral, ocr, DocumentURLChunk
import os
import json


MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-ocr-latest"
CLIENT = Mistral(api_key=MISTRAL_API_KEY)


async def Referral_Information_Extraction(referral: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_):referral pdf

    Returns:
        json : containing a list of referralPages[InformationPerPage]
    """
    loop = asyncio.get_event_loop()

    with open(referral, "rb") as f:
        uploaded_referral_pdf = CLIENT.files.upload(
            file={"file_name": "Referral", "content": f.read()}, purpose="ocr"
        )
    signed_referral_url = CLIENT.files.get_signed_url(file_id=uploaded_referral_pdf.id)
    response = await loop.run_in_executor(
        None,
        lambda: CLIENT.ocr.process(
            model=MODEL,
            document=DocumentURLChunk(document_url=signed_referral_url.url),
            include_image_base64=False,
        ),
    )
    return "\n\n".join(page["markdown"] for page in response.model_dump()["pages"])


if __name__ == "__main__":
    pass
