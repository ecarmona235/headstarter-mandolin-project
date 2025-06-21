import asyncio
from unittest import result

import mistralai
from utilities.ExtractFields import extract_map
from utilities.PromptGenerator import prompt_generator
from utilities.GeminiFill import fill_map
from utilities.GeminiMap import format_map
from utilities.MistralQueries import referral_information_extraction


async def process_patient(patient: str, pa_path: str, referral_path: str):

    extracted_map = extract_map(pa_path)
    res_dict = {}
    static_map = []

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

    async def step_one_static():
        prompt = prompt_generator("static_pa_prompt", {})
        result_gemini = await format_map(prompt=prompt, pdf_file=pa_path)
        print("....Static PA mappped....")
        return result_gemini

    async def step_two():
        result_mistral = await referral_information_extraction(referral=referral_path)
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

    async def step_three_static(gemini_dict: dict, mistral_string: str):
        prompt = prompt_generator(
            "fill_static_map",
            {"extracted_referral": mistral_string, "map_json": gemini_dict},
        )
        result_gemini = await fill_map(prompt=prompt)
        print("....PA static map filled....")
        return result_gemini

    if len(extracted_map) > 0:
        tasks = [step_one(), step_two()]
        results = await asyncio.gather(*tasks)
        for result in results:
            if type(result) == dict:
                res_dict["gemini"] = result
            else:
                res_dict["mistral"] = result

        final_result = await asyncio.gather(
            step_three(
                gemini_dict=res_dict["gemini"], mistral_string=res_dict["mistral"]
            )
        )
        print(f"....Returning json for {patient}....")
        return 1, final_result
    else:
        task = [step_one_static(), step_two()]
        results = await asyncio.gather(*task)
        for result in results:
            if type(result) == list:
                res_dict["gemini"] = result
            else:
                res_dict["mistral"] = result
        final_result =  await asyncio.gather(step_three_static(gemini_dict=res_dict["gemini"], mistral_string=res_dict["mistral"]))
        print(f"....Returning json for {patient}....")
        return 2, final_result
