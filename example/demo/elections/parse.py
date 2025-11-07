"""This script parses chart information"""

import json
import csv
import os

DATA_FOLDER = 'data'

def remove_prefix(value, prefix):
    """Removes a specified prefix from a string if it exists and strips whitespace."""
    if value.startswith(prefix):
        return value[len(prefix):].strip()
    return value

def extract_json_data(data_dict):
    """Extracts key election data from a structured content JSON object."""
    infoboxes = data_dict.get('infoboxes', [])
    extracted_year = None
    extracted_electoral_vote = None
    extracted_running_mate = None
    extracted_nominee = None

    for section in infoboxes:
        if 'has_parts' in section:
            for part in section['has_parts']:
                if 'name' in part and part['name'][:4].isdigit():
                    extracted_year = part['name'][:4]

                for child in part['has_parts']:
                    val = ''
                    if 'value' in child and child['value']:
                        val = child['value']

                    if val.startswith('Electoral vote'):
                        extracted_electoral_vote = remove_prefix(val, 'Electoral vote')

                    if val.startswith('Running mate'):
                        extracted_running_mate = remove_prefix(val, 'Running mate')

                    if val.startswith('Nominee'):
                        extracted_nominee = remove_prefix(val, 'Nominee')

    return extracted_year, extracted_electoral_vote, extracted_running_mate, extracted_nominee

output_file_path = os.path.join(DATA_FOLDER, 'output.csv')

with open(output_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Year', 'Nominee', 'Running Mate', 'Electoral Vote']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_FOLDER, filename), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                year, electoral_vote, running_mate, nominee = extract_json_data(json_data)

                if electoral_vote:
                    electoral_vote = [int(vote) for vote in electoral_vote.split() if vote.isdigit()]
                else:
                    electoral_vote = []

                writer.writerow({
                    'Year': year,
                    'Nominee': nominee,
                    'Running Mate': running_mate,
                    'Electoral Vote': electoral_vote
                })

print(f"Data extraction complete. Check {output_file_path}.")
