import os
import json
import pathlib
import asyncio

from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Tuple

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash"
L_CLIENT = genai.Client(api_key=GEMINI_API_KEY)


async def format_map(prompt: str, pdf_file: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_): pa_form pdf

    Returns:
        json: formats the field extracted from fitz
    """
    file_path = pathlib.Path(pdf_file)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: L_CLIENT.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(
                    data=file_path.read_bytes(), mime_type="application/pdf"
                ),
                prompt,
            ],
        ),
    )
    return response.to_json_dict()

class OCRBlock(BaseModel):
    page: int = Field(
        ..., 
        description="1-based page number where this text block was found"
    )
    bbox: Tuple[int, int, int, int] = Field(
        ..., 
        description="Bounding box of the block as (x0, y0, x1, y1) in PDF points"
    )
    text: str = Field(
        ..., 
        description="Raw text extracted by the OCR engine"
    )

class OCRResult(BaseModel):
    blocks: List[OCRBlock] = Field(
        ..., 
        description="List of all OCRBlock entries across the document"
    )
async def format_static_map(prompt: str, pdf_file: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_): pa_form pdf

    Returns:
        json: formats the field extracted from fitz
    """
    file_path = pathlib.Path(pdf_file)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: L_CLIENT.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(
                    data=file_path.read_bytes(), mime_type="application/pdf"
                ),
                prompt,
            ],
        ),
    )
    return response.to_json_dict()


if __name__ == "__main__":
    pass
