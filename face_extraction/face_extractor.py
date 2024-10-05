"""
Face Extraction Utility Function

This module provides a utility function to extract a face from an image using the
MediaPipe and OpenCV libraries. The extracted face is obtained by performing face detection
and then cropping the image to the bounding box of the detected face.

Dependencies:
    - OpenCV (cv2)
    - MediaPipe (mp)
    - NumPy (np)
    - crop_face (from a local module)

Functions:
    - extract_face: Extracts a face from an image using a pre-trained model and returns the cropped face.
"""


from . import os, cv2, np, mp, python, vision, crop_face

MODEL_PATH = os.path.join("face_extraction", "models", "detector.tflite")

def extract_face(IMAGE_FILE):
  """
  Extracts a face from an image using a pre-trained face detection model.

  Parameters:
      IMAGE_FILE (str): Path to the image file from which the face should be extracted.
      MODEL_PATH (str): Path to the pre-trained model file (e.g., a .tflite file).

  Returns:
      np.ndarray or None: If a face is detected, returns a NumPy array representing the 
                          cropped face. If no face is detected, returns None.

  Note:
      - The function utilizes the MediaPipe library for face detection and OpenCV for image processing.
      - Ensure the model file specified by MODEL_PATH is compatible with the MediaPipe FaceDetector.
  """
      
  img = cv2.imread(IMAGE_FILE)

  model_file = open(MODEL_PATH, "rb")
  MODEL_DATA = model_file.read()
  model_file.close()

  # Create an FaceDetector object.
  base_options = python.BaseOptions(model_asset_buffer=MODEL_DATA)
  options = vision.FaceDetectorOptions(base_options=base_options)
  detector = vision.FaceDetector.create_from_options(options)

  # Convert image to mediapipe Image format
  image = mp.Image.create_from_file(IMAGE_FILE)
  # Detect faces in the input image
  detection_result = detector.detect(image)

  # pass image to face_detection_utility to get cropped, returns None if no face
  image_copy = np.copy(img)
  extracted_face = crop_face(image_copy, detection_result)

  return extracted_face     # Will return None if no face was detected
