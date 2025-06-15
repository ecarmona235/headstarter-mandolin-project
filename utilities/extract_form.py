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
                repaired_data = json.loads(repair_json(content[0]))
                if type(repaired_data) is list:
                    temp = content[0].split("left_blank")
                    extracted_data["left_blank"] = json.loads(repair_json(temp[1]))
                    extracted_data["form"] = json.loads(repair_json(temp[0]))
                else:
                    extracted_data["left_blank"] = repaired_data.pop("left_blank")
                    extracted_data["form"] = repaired_data
                with open(
                    f"{file_to_print.split("_")[0]}_filled_form.json",
                    "w",
                    encoding="UTF-8",
                ) as json_file:
                    json.dump(extracted_data["form"], json_file, default=str)  # type: ignore
                with open(
                    f"{file_to_print.split("_")[0]}_left_blank.json",
                    "w",
                    encoding="UTF-8",
                ) as json_file:
                    json.dump(extracted_data["left_blank"], json_file, default=str)  # type: ignore

            
            for key, value in json_data.items():
                iterate_json(value, indent + 4, extracted_data)  # Recursively go deeper

        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                iterate_json(item, indent + 4)

    iterate_json(data)  # Start recursive iteration


if __name__ == "__main__":
    pass
