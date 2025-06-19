import asyncio
import pathlib
from google import genai
from google.genai import types
import os
import json

from pydantic import BaseModel


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash"
CLIENT = client = genai.Client(api_key=GEMINI_API_KEY)

    

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
        lambda: CLIENT.models.generate_content(
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
