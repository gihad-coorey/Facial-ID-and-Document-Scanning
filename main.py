"""
Main Facial Recognition Script

This module coordinates the entire facial recognition process, which encompasses face extraction,
liveliness checking, and face comparison, providing a seamless workflow from image input to 
face verification result output.

Dependencies:
    - os: Provides functionalities to interact with the operating system, specifically file I/O operations.
    - cv2: OpenCV library used for computer vision tasks.
    - extract_face: A function from the face_extraction module that extracts faces from images.
    - compare_faces, mock_liveliness: Functions from the face_compare module that compare faces and 
                                      perform a liveliness check, respectively.

Expected Directory Structure:
    - test_ids: A directory containing JPEG images to be tested.
    - face_extraction/models: A directory containing the model file(s) used in face detection.

Functions:
    - main: Coordinates the facial recognition workflow.

Usage Example:
    Execute the script with the following command in the terminal:
    ```shell
    python main_face_recognition_script.py
    ```
"""
import os
import cv2
from face_extraction.face_extractor import extract_face
from liveliness_check.liveliness_check import liveliness_check
from face_compare.face_compare import compare_faces

IMAGE_NAME        = 'Gihad.png'
IMAGE_PATH        = os.path.join("test_ids", IMAGE_NAME)
SHOW_FACE_COMPARE = True

def show_face_compare(extracted_face, liveliness_frame):
  if liveliness_frame is not None and extracted_face is not None:
    height, width = 300, 400
    
    liveliness_frame_resized = cv2.resize(liveliness_frame, (width, height))
    extracted_frame_resized = cv2.resize(extracted_face, (width, height))
    combined_image = cv2.hconcat([liveliness_frame_resized, extracted_frame_resized])

    cv2.imshow('Face Compare', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows

def main():
  # Step 1: Extract face from ID
  print("Please provide an image of your identifying documentation.")
  extracted_face = extract_face(IMAGE_PATH)
  if extract_face is None:
    print("Face unable to be detected. Please retake image and ensure appropriate lighting, that the image is clear, and the face is fully in-frame.")
    return
  else:
    print("Face detected. Liveliness check will now commence.")

  # Step 2: Perform Liveliness Check
  liveliness_frame = liveliness_check()

  # Step 3: Compare frame from liveliness with Extracted ID
  print("Beginning face comparison")
  comparison = compare_faces(liveliness_frame, extracted_face)

  # SHOW BOTH FACES FOR TESTING
  if SHOW_FACE_COMPARE:
    show_face_compare(extracted_face, liveliness_frame)

  # Step 4: Check if True or False
  if comparison == True:
    print(f'Face in ID matches face in liveliness check.')
    print(f'You have passed all tests.')
    result = True

    return result

  else:
    print(f'Face in ID does not match face in liveliness check.')
    print(f'You have failed one or both tests.')
    result = False  

    return result

if __name__ == '__main__':
  main()
