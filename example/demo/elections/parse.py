import json
import csv
import os

# Folder containing the JSON files
data_folder = 'data'

def remove_prefix(value, prefix):
    if value.startswith(prefix):
        return value[len(prefix):].strip()
    return value


# Function to extract needed fields from JSON
def extract_json_data(json_data):
    # Extracting infobox.has_parts.name (4-digit year)
    infobox = json_data.get('infobox', [])
    year = None
    electoral_vote = None
    running_mate = None
    nominee = None

    for section in infobox:
        if 'has_parts' in section:
            for part in section['has_parts']:
                # Extract year from name
                if 'name' in part and part['name'][:4].isdigit():
                    year = part['name'][:4]

                for child in part['has_parts']:
                    val = ''
                    if 'value' in child and child['value']:
                        val = child['value']

                    # Extract value starting with 'Electoral vote'
                    if val.startswith('Electoral vote'):
                        electoral_vote = remove_prefix(val, 'Electoral vote')

                    # Extract value starting with 'Running mate'
                    if val.startswith('Running mate'):
                        running_mate = remove_prefix(val, 'Running mate')

                    # Extract value starting with 'Nominee'
                    if val.startswith('Nominee'):
                        nominee = remove_prefix(val, 'Nominee')

    # Return the extracted fields
    return year, electoral_vote, running_mate, nominee


# Specify the path to save the CSV in the 'data' folder
output_file_path = os.path.join(data_folder, 'output.csv')

# Open CSV file for writing
with open(output_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Year', 'Nominee', 'Running Mate', 'Electoral Vote']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                year, electoral_vote, running_mate, nominee = extract_json_data(json_data)

                # electoral_vote is a set of integers in a string separated by spaces, parse it into a list of integers
                if electoral_vote:
                    electoral_vote = [int(vote) for vote in electoral_vote.split() if vote.isdigit()]
                else:
                    electoral_vote = []  # Or handle the None case as needed

                # Write the data to CSV
                writer.writerow({
                    'Year': year,
                    'Nominee': nominee,
                    'Running Mate': running_mate,
                    'Electoral Vote': electoral_vote
                })

print(f"Data extraction complete. Check {output_file_path}.")
