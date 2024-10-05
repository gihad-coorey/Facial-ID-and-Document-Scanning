"""
This script contains functions for detecting faces within images and videos using OpenCV and face_recognition library.
It allows for:
    - Extracting a face from an image.
    - Detecting a face in a live video stream and returning the largest detected face.
    - Comparing two faces and determining if they belong to the same person.

Dependencies:
    - OpenCV
    - face_recognition

Functions:
    - compare_faces: Compares two face images and determines if they belong to the same person.
"""

import cv2
import face_recognition
from face_extraction.face_extractor import extract_face

# Compares face with the 'best' frame from the video stream
def compare_faces(stream_face, extracted_face):
  
    """
    Compare two faces and determine if they belong to the same person.

    This function takes two images containing faces, converts them to a compatible format,
    and then uses the face_recognition library to compare them and determine if they are
    of the same person.

    Parameters:
        stream_face (array): An image of a face captured from a video stream.
        extracted_face (array): An image of a face extracted from a static image.

    Returns:
        bool: True if the faces match, False otherwise or if no faces are detected/available for comparison.

    Notes:
        Ensure that the input images are in BGR format (such as those read by OpenCV).
    """

    # Convert to same format
    # Check if at stream_face or extracted_face are not null
    if stream_face is None or extract_face is None:
        return False
    streamed_face_rgb = cv2.cvtColor(stream_face, cv2.COLOR_BGR2RGB)
    extracted_face_rgb = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2RGB)
    # Get the face encodings for each image
    streamed_face_encoding = face_recognition.face_encodings(streamed_face_rgb)
    extracted_face_encoding = face_recognition.face_encodings(extracted_face_rgb)
    # Check if at least one face encoding is available for comparison
    if not streamed_face_encoding or not extracted_face_encoding:
        return False  # No faces detected
    # Get boolean value for face comparison
    result =  face_recognition.compare_faces([streamed_face_encoding[0]], extracted_face_encoding[0])
    return result[0]

