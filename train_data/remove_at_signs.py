import os
import json
import glob

def remove_at_signs_from_fields(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'join' and isinstance(value, list):
                data[key] = [item.replace('@@', '') for item in value]
            elif key == 'column' and isinstance(value, str):
                data[key] = value.replace('@@', '')
            else:
                remove_at_signs_from_fields(value)
    elif isinstance(data, list):
        for item in data:
            remove_at_signs_from_fields(item)

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Update the JSON content
    remove_at_signs_from_fields(data)

    # Write the updated JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def process_all_json_files_in_directory(directory):
    for file_path in glob.iglob(os.path.join(directory, '**', '*.json'), recursive=True):
        process_json_file(file_path)

# Specify the directory to process
directory_to_process = '/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial'

# Process all JSON files in the specified directory and its subdirectories
process_all_json_files_in_directory(directory_to_process)