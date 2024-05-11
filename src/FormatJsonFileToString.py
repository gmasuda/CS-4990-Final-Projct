import json
import os

def format_json_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return ""

    formatted_string = ""
    for item in json_data:
        tag = item["tag"]
        confidence = item["confidence"]
        formatted_string += f"tag:{tag}; confidence:{confidence:.2f}, "
    # Remove the trailing comma and space
    formatted_string = formatted_string[:-2]
    return formatted_string

# Example usage: Provide the file path as an argument

folder_path2 = 'descriptions'
image_path2 = os.path.join(folder_path2, 'room_cleanliness_tags.json')

formatted_string = format_json_file_to_string(image_path2)
print(formatted_string)
