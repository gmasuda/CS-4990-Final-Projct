import os
from openai import OpenAI
import cv2
import DescriptionCreator
import json

#folder path
folder_path = 'rooms'
image_path = os.path.join(folder_path, 'photo.png')
folder_path2 = 'descriptions'
image_path2 = os.path.join(folder_path2, 'room_cleanliness_tags.json')

OPENAPI_KEY = "OPENAPI_KEY"
api_key = OPENAPI_KEY

if not api_key:
    raise ValueError("API key is not set in environment variables.")

client = OpenAI(api_key=api_key)

def CreateDescription():
    DescriptionCreator.DescribeImage(image_path)
    FormattedString = JsonToString(image_path2)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "assistant",
                    "content": "I am role-playing a helpless child for a TV show. You are role-playing \
                    a character who is authoritarian, strict, harsh, and manipulative. I am going \
                    to provide you with a series of tags that describe the quality of a bedroom in the \
                    format tag: item in the room followed by the confidence level. " + FormattedString + "Based \
                    on these tags I NEED A MEAN RESPONSE USING THESE CONFIDENCE LEVELS OF how bad the quality \
                    is of my room is for the sake of a script.  Make sure to make comments specific towards the \
                    tags and the confidence levels provided. If the confidence level is below 5% then make sure to \
                    exclude that tag from your comment. As you make this comment make sure you don't mention the \
                    confidence levels or the tags to me, but make sure you still use them to be more specific towards \
                    the quality of my room."
                }
            ],
            model="gpt-4-turbo"
            
        )
        print(FormattedString)
        # Accessing the content of the first message from the assistant's response
        #print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")

def RoomDetection():
    # Initialize the camera (0 is the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Loop to continuously get frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly ret is True
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Display the resulting frame
        cv2.imshow('Camera', frame)

        # Wait for a key press and check if it's 'q' or 'p'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            # Save the frame as an image file
            cv2.imwrite(image_path, frame)
            print("Photo taken!")
            DescriptionCreator.DescribeImage(image_path)
            CreateDescription()

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def JsonToString(file_path):
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

def Test():
    DescriptionCreator.DescribeImage(image_path)
    CreateDescription()


if __name__ == '__main__':
    #RoomDetection()
    #Test()
    CreateDescription()
