import asyncio
import os
import json
import re
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google import genai

from pydantic import BaseModel, Field
from typing import List

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash"
H_CLIENT = genai.Client(api_key=GEMINI_API_KEY)


class PAFormAnswer(BaseModel):
    name: str
    page: int
    field_lable: str
    answer: str = Field(
        description="Answer to the question based on the extracted referral package"
    )


class LeftBlank(BaseModel):
    name: str
    page: int
    context: str = Field(description="Original context information")
    reason: str = Field(description="Reason why it was left blank")


class ResponseDict(BaseModel):
    fields: List[PAFormAnswer]
    left_blank: List[LeftBlank]


class ResponseFormat(BaseModel):
    response_dict: ResponseDict


async def fill_map(prompt: str) -> json:
    """_summary_

    Args:
        pdf_file (_type_): Fills map using gemini

    Returns:
        json: formats the field with values filled
    """
    loop = asyncio.get_event_loop()
    raw = ResponseFormat.model_json_schema(
        ref_template="#/definitions/{model}", mode="validation"
    )

    if "$defs" in raw:
        raw["definitions"] = raw.pop("$defs")


    response = await loop.run_in_executor(
        None,
        lambda: H_CLIENT.models.generate_content(
            model=MODEL,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                    ],
                }
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema" : ResponseFormat
                },
        ),
    )

    candidate = response.candidates[0]
    parts = candidate.content.parts[0]
    if parts.function_call:
        args = candidate.function_call.args
        response_dict = args["response_dict"]
        result = ResponseFormat(**{"response_dict": response_dict})
    else:
        text_blob = parts.text
        try:
            # try to load raw
            payload = json.loads(text_blob)
            result = payload["response_dict"]
        except json.JSONDecodeError:
            # if it fails, extract the {...} block via regex
            m = re.search(r'(\{.*\})', text_blob, re.DOTALL)
            if not m:
                raise RuntimeError("Couldn't find JSON in the model output")
            payload = json.loads(m.group(1))
            result = payload["response_dict"]

    return result



if __name__ == "__main__":
    pass
