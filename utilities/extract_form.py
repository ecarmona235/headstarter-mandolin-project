import ast
import json
from json_repair import repair_json


def extract_form(file_to_print: str):
    """Recursively prints JSON key-value pairs, waiting for Enter before each.

    Args:
        file_to_print (str): Path to the JSON file.
    """
    # Load JSON data
    with open(file_to_print, "r", encoding="UTF-8") as input_json_file:
        data = json.load(input_json_file)

    # Ensure it's a dictionary
    if isinstance(data, str):
        data = json.loads(data)

    # Recursive function to iterate through nested JSON
    def iterate_json(json_data, indent=0, extracted_data=None):
        if extracted_data is None:
            extracted_data = {"form": None}
        if isinstance(json_data, dict):
            if "message" in json_data and "content" in json_data["message"]:
                content = (
                    json_data["message"]["content"].split("```json")[1].split("```")
                )
                try:  # predefined and exisiting
                    extracted_data["form"] = content[0].split('"left_blank":')[0] # predefined
                    extracted_data["left_blank"] = content[0].split('"left_blank":')[1] # # predefined and exisiting
                    # print(extracted_data["form"])
                    possible = extracted_data["form"].split('"fields":')
                    if len(possible) >1:  # existing
                        # print(possible[0])
                        extracted_data["form"] = possible[1]
                        print("possible")
                        extracted_data["form"] = repair_json(extracted_data["form"])
                        extracted_data["left_blank"] = repair_json(extracted_data["left_blank"])
                        with open(
                        f"{file_to_print.split("_")[0]}_filled_form.json", "w", encoding="UTF-8"
                        ) as json_file:
                            json.dump(json.loads(extracted_data["form"]), json_file, default=str)  # type: ignore
                        with open(
                            f"{file_to_print.split("_")[0]}_left_blank.json", "w", encoding="UTF-8"
                        ) as json_file:
                            json.dump(json.loads(extracted_data["left_blank"]), json_file, default=str)  # type: ignore 
                        return
                    else: # predefined
                        extracted_data["form"] = repair_json(extracted_data["form"])
                        extracted_data["left_blank"] = repair_json(extracted_data["left_blank"])
                        with open(
                        f"{file_to_print.split("_")[0]}_filled_form.json", "w", encoding="UTF-8"
                        ) as json_file:
                            json.dump(json.loads(extracted_data["form"]), json_file, default=str)  # type: ignore
                        with open(
                            f"{file_to_print.split("_")[0]}_left_blank.json", "w", encoding="UTF-8"
                        ) as json_file:
                            json.dump(json.loads(extracted_data["left_blank"]), json_file, default=str)  # type: ignore 
                        return
                #     with open(
                #     f"{file_to_print.split("_")[0]}_filled_form.json", "w", encoding="UTF-8"
                #     ) as json_file:
                #         json.dump(json.loads(extracted_data["form"]), json_file, default=str)  # type: ignore
                #     with open(
                #         f"{file_to_print.split("_")[0]}_left_blank.json", "w", encoding="UTF-8"
                #     ) as json_file:
                #         json.dump(json.loads(extracted_data["left_blank"]), json_file, default=str)  # type: ignore
                except: # static
                    print("In except 1")
                    extracted_data["form"] = json_data["message"]["content"].split("```json")[1].split("```")[0]
                    extracted_data["left_blank"] = json_data["message"]["content"].split("```json")[2].split("```")[0]
                    with open(
                    f"{file_to_print.split("_")[0]}_filled_form.json", "w", encoding="UTF-8"
                    ) as json_file:
                        json.dump(json.loads(extracted_data["form"]), json_file, default=str)  # type: ignore
                    with open(
                        f"{file_to_print.split("_")[0]}_left_blank.json", "w", encoding="UTF-8"
                    ) as json_file:
                        json.dump(json.loads(extracted_data["left_blank"]), json_file, default=str)  # type: ignore
                    return 
                    
                #     return
                # try:  # static case
                #     extracted_data["form"] = json_data["message"]["content"].split("```json")[1].split("```")[0]
                #     extracted_data["left_blank"] = json_data["message"]["content"].split("```json")[2].split("```")[0]

            for key, value in json_data.items():
                iterate_json(value, indent + 4, extracted_data)  # Recursively go deeper

        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                iterate_json(item, indent + 4)

    iterate_json(data)  # Start recursive iteration


if __name__ == "__main__":
    pass
