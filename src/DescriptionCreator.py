import requests
import json
import base64
import os

# Define the folder paths
base_folder = 'rooms'
description_folder = 'descriptions'
image_path = os.path.join(base_folder, 'testing.png')

# Ensure the descriptions folder exists
os.makedirs(description_folder, exist_ok=True)

def DescribeImage(image_path):
    # Replace 'api_key' with your actual Clarifai API key
    api_key = 'Clarifai API KEY'  # Make sure to replace this with your actual API key
    headers = {
        'Authorization': f'Key {api_key}',
        'Content-Type': 'application/json'
    }

    # Encode the image to base64
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Set up the data payload for the POST request
    data = json.dumps({
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": base64_image
                    }
                }
            }
        ]
    })

    # Clarifai API endpoint for your custom model trained to identify room cleanliness
    url = 'https://api.clarifai.com/v2/models/RoomCheck3/outputs'  # Replace with your custom model ID

    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()

        # Extract concepts and prepare to save to JSON
        concepts = [
            {"tag": concept['name'], "confidence": concept['value']}
            for concept in response_data['outputs'][0]['data']['concepts']
        ]

        # Define the path for the JSON file within the descriptions folder
        json_file_path = os.path.join(description_folder, 'room_cleanliness_tags.json')

        # Save to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(concepts, json_file, indent=4)

        print(f"Room cleanliness tags and confidence levels have been saved to '{json_file_path}'")
    else:
        # Print an error message if the request failed
        print("Failed to get tags:", response.text)

# Example usage
if __name__ == '__main__':
    DescribeImage(image_path)
