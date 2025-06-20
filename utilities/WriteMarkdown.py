from pathlib import Path

def dict_to_markdown(left_blank: list, md_path: str) -> None:
    stripped = {}
    for values in left_blank:
        context = values.get("context")
        reason = values.get("reason")
        if "not applicable." in reason:
            continue
        if context not in stripped:
            stripped[context] = reason
        else:
            stripped[context] += "\n" + reason
        

    md_file = Path(md_path)
    md_file.parent.mkdir(parents=True, exist_ok=True)
    with open(md_file, 'w', encoding='utf-8') as mf:
        # 3) If it’s a dict, iterate key/value pairs
        mf.write(f"# \t\t Form Fields Left Blank\n\n")
        mf.write(f"## \tThe following list contains fields that were left blank because the referral lacked the necessary information or contained conflicting data. Any non-applicable fields have been omitted from this list. Please review the entire form carefully for any errors or missing details.\n\n")
        for key, value in stripped.items():
            # Write each key as an H2 heading, then the value as a paragraph
            mf.write(f"## {key}\n")
            # if the value is a list, write each item on its own line
            mf.write(f"{value}\n\n")

if __name__ == "__main__":
    pass
