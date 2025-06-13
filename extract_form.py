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
                    print("form")
                    value = extract_json(value.split("```")[1])
                    extracted_data["form"] = value
                    json_to_dump = extracted_data.get("form")
                    print(json_to_dump)
                    with open(
                        f"{file_to_print.split("_")[0]}_filled_form.json",
                        "w",
                        encoding="UTF-8",
                    ) as file:
                        json.dump(json_to_dump, file, indent=4)

                iterate_json(value, indent + 4)  # Recursively go deeper

        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                iterate_json(item, indent + 4)
        elif isinstance(json_data, str) and "Here is" in json_data:
            value = extract_json(json_data.split("```")[1])
            iterate_json(value, indent + 4)  # Recursively go deeper

    iterate_json(data)  # Start recursive iteration


if __name__ == "__main__":
    pass