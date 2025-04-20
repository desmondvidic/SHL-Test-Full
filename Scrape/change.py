import json
import re

def transform_assessment_data(data):
    test_type_map = {
        "A": "Ability & Aptitude",
        "B": "Biodata & Situational Judgement",
        "C": "Competencies",
        "D": "Development & 360",
        "E": "Assessment Exercises",
        "K": "Knowledge & Skills",
        "P": "Personality & Behavior",
        "S": "Simulations"
    }

    for entry in data:
        # Convert booleans to Yes/No
        entry["remote_testing"] = "Yes" if entry.get("remote_testing") else "No"
        entry["adaptive_IRT"] = "Yes" if entry.get("adaptive_IRT") else "No"

        # Replace test_type codes with full forms
        entry["test_type"] = [test_type_map.get(code, code) for code in entry.get("test_type", [])]

        # Extract number from assessment length string
        raw_length = entry.get("assessment length", "")
        match = re.search(r'\d+', raw_length)
        if match:
            entry["assessment length"] = str(int(match.group()))
        else:
            entry["assessment length"] = "-1"


    return data

# File I/O
input_file = "embed.json"
output_file = "transformed2.json"

with open(input_file, "r", encoding="utf-8") as infile:
    data = json.load(infile)

transformed_data = transform_assessment_data(data)

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(transformed_data, outfile, indent=2)
