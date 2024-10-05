"""
Testing Script for Face Extractor

This module is utilized to conduct unit tests for the face extraction functionality
of a facial recognition system. It aims to validate that the `extract_face` function
from the `face_extraction` module efficiently detects and extracts faces from a directory 
of test images.

Dependencies:
    - os: Facilitates interaction with the operating system, particularly file and directory operations.
    - cv2: OpenCV library for computer vision tasks, used here for image handling and display.
    - unittest: Standard unit testing library in Python.
    - extract_face function from the face_extraction module.

Structure of Test Data:
    - The test images should be stored in a directory named 'test_ids'.
    - All test images should be JPEG files (with a '.jpg' extension).

Functions:
    - setUp: Initialises the list of image files to be tested.
    - test_face_detection: Iterates through each image, attempting to extract a face, and visually 
                           displays the extracted face for visual validation.
    - visualize_face: Displays the extracted face using OpenCV's imshow function.

Example:
    Execute the test with the following command in the terminal:
    ```shell
    python -m unittest test_face_detection.py
    ```
"""


import os, cv2, unittest
from face_extraction import extract_face

class TestFaceDetection(unittest.TestCase):
  def setUp(self):
    self.image_files = [f for f in os.listdir('test_ids') if f.endswith('.jpg')]

  def test_face_detection(self):
    for image_file in self.image_files:
      image_path = os.path.join('test_ids', image_file)
      detected_face = extract_face(image_path)
        
      # If the detected_face is None, it means probability was < 0.8
      if detected_face is None:
        print(f"No face detected in {image_file}. Please resubmit your ID document. The image may be blurred or distorted.")
      else:
        visualize_face(detected_face)

def visualize_face(extracted_face) -> None:
  """
  View the cropped image.
  Anykey to skip to next image.
  """
  # Show extracted face
  cv2.imshow("Annotated Image", extracted_face)
  # Wait for a key press and then close the window
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  unittest.main()
