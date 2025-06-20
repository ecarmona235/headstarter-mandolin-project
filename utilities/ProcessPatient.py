import asyncio
from unittest import result
from utilities.ExtractFields import extract_map
from utilities.PromptGenerator import prompt_generator
from utilities.GeminiFill import fill_map
from utilities.GeminiMap import format_map
from utilities.MistralQueries import Referral_Information_Extraction


async def process_patient(patient: str, pa_path: str, referral_path: str):

    extracted_map = extract_map(pa_path)
    res_dict = {}

    async def step_one():
        prompt = prompt_generator(
            "pa_prompt",
            {
                "extracted_fields": extracted_map,
            },
        )
        result_gemini = await format_map(prompt=prompt, pdf_file=pa_path)
        print("....PA mapped....")
        return result_gemini

    async def step_two():
        result_mistral = await Referral_Information_Extraction(referral=referral_path)
        print("....Referral extracted...")
        return result_mistral

    async def step_three(gemini_dict: dict, mistral_string: str):
        prompt = prompt_generator(
            "fill_in_map",
            {"extracted_referral": mistral_string, "map_json": gemini_dict},
        )
        result_gemini = await fill_map(prompt=prompt)
        print("....PA map filled....")
        return result_gemini

    tasks = [step_one(), step_two()]
    results = await asyncio.gather(*tasks)
    for result in results:
        if type(result) == dict:
            res_dict["gemini"] = result
        else:
            res_dict["mistral"] = result

    final_result = await asyncio.gather(
        step_three(gemini_dict=res_dict["gemini"], mistral_string=res_dict["mistral"])
    )
    print(f"....Returning json for {patient}....")

    return final_result
