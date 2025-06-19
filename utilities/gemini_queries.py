import asyncio
import pathlib
import httpx
from google import genai
from google.genai import types
import os
import json



GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash"
CLIENT = client = genai.Client(api_key=GEMINI_API_KEY)


async def gemini_loop_async(prompt: str, pdf_file: str, map: dict) -> json:
    """_summary_

    Args:
        pdf_file (_type_): _description_

    Returns:
        json: _description_
    """
    file_path = pathlib.Path(pdf_file)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: CLIENT.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(  
                    data=file_path.read_bytes(),
                    mime_type='application/pdf'),
                prompt
            ]
        )
    )
    return response.to_json_dict()


if __name__ == "__main__":
    pass
