from ast import List
import asyncio
from mistralai import Mistral, ocr, DocumentURLChunk
from mistralai.extra import response_format_from_pydantic_model
import os
import json
from pydantic import BaseModel, Field


MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = "mistral-ocr-latest"
CLIENT = Mistral(api_key=MISTRAL_API_KEY)


class InformationPerPage(BaseModel):
    page_number: str = Field(
        ..., description="The page number the information came from."
    )
    value: str = Field(..., description="Information Extracted on page")


class ReferralPages(BaseModel):
    all_information: List[InformationPerPage]


bbox_format = response_format_from_pydantic_model(ReferralPages)


async def Referral_Information_Extraction(prompt: str, referral: str) -> json:
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
            document=DocumentURLChunk(document_url=signed_referral_url),
            prompt=prompt,
            bbox_annotation_format=bbox_format,
            include_image_base64=True,
        ),
    )
    return response.model_dump_json()


if __name__ == "__main__":
    pass
