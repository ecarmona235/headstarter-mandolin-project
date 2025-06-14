import json
import re


def extract_json(text: str):
    """Extracts JSON from a string that contains extra text before the JSON starts.

    Args:
        text (str): String containing JSON with extra text.
    """
    json_match = re.search(r"\{.*", text, re.DOTALL)
    if json_match:
        json_data = json_match.group(0)  # Extract only the JSON part
        return json.loads(json_data)  # Convert string to dictionary
    else:
        return text  # Return original text if no JSON is found


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
            for key, value in json_data.items():
                if (
                    key == "content"
                    and isinstance(value, str)
                    and "Here is the" in value
                ):
                    # Predifined 
                    value = extract_json(value.split("```json")[1])
                    extracted_data["form"] = value
                    json_to_dump = extracted_data.get("form")["pages"]
                    left_blank = extracted_data["form"].get("left_blank")
                    if json_to_dump and left_blank:
                        with open(
                            f"{file_to_print.split("_")[0]}_filled_form.json",
                            "w",
                            encoding="UTF-8",
                        ) as file:
                            json.dump(json_to_dump, file, indent=4)
                            
                        with open(
                            f"{file_to_print.split("_")[0]}_left_blank.json",
                            "w",
                            encoding="UTF-8",
                        ) as file:
                            json.dump(left_blank, file, indent=4)

                iterate_json(value, indent + 4)  # Recursively go deeper

        elif isinstance(json_data, list): # exisiting
            for index, item in enumerate(json_data):
                if type(item) is dict:
                    extracted_data["form"] = item["message"]["content"].split("```json")[1].split("```")[0]
                    try:
                        
                        extracted_data["form"] = extract_json(extracted_data["form"])
                        left_blank = extracted_data["form"].pop("left_blank")
                                            
                        extracted_data["left_blank"] = left_blank
                        with open(
                                f"{file_to_print.split("_")[0]}_left_blank.json",
                                "w",
                                encoding="UTF-8",
                            ) as file:
                                json.dump(extracted_data["left_blank"], file, indent=4)
                    except: # static
                        extracted_data["form"] = json.loads(item["message"]["content"].split("```json")[1].split('```')[0].split(',\n"left_blank"')[0].replace('"', '\"'))
                        with open(
                                f"{file_to_print.split("_")[0]}_filled_form.json",
                                "w",
                                encoding="UTF-8",
                            ) as file:
                                json.dump(extracted_data["form"], file, indent=4)
                        extracted_data["left_blank"] = json.loads(item["message"]["content"].split("```json")[1].split('```')[0].split(',\n"left_blank":')[1].replace('"', '\"'))
                        print(extracted_data["left_blank"])
                        with open(
                                f"{file_to_print.split("_")[0]}_left_blank.json",
                                "w",
                                encoding="UTF-8",
                            ) as file:
                                json.dump(extracted_data["left_blank"], file, indent=4)
                        print("\n")
                iterate_json(item, indent + 4)

    iterate_json(data)  # Start recursive iteration


if __name__ == "__main__":
    pass
