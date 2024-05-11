import cv2
import os

def FaceDetection():
    #folder path
    folder_path = 'rooms'

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

            image_path = os.path.join(folder_path, 'photo.png')
            # Save the frame as an image file
            cv2.imwrite(image_path, frame)
            print("Photo taken!")

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    FaceDetection()
