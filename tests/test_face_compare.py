"""
Testing Script for Face Comparison

This module contains unit tests for the face comparison functionality 
in a facial recognition system. The tests ensure that the function 
`compare_faces` from the `face_compare` module correctly identifies and 
compares faces from a directory of test images.

Dependencies:
    - unittest: Standard unit testing library in Python.
    - os: Provides a way of using operating system dependent functionality 
          such as reading from the file system.
    - sys: To access some variables used or maintained by the interpreter.
    - extract_face function from the face_extraction.face_extractor module.
    - compare_faces function from the face_compare.face_compare module.

Structure of Test Data:
    - The test faces should be organized in a directory named 'test_faces'.
    - Each individual or subject should have their own sub-folder within 'test_faces'.
    - Each of these sub-folders should contain at least two images of the subject's face.

Functions:
    - test_compare_faces: Validates the functionality of the `compare_faces` function by
                          comparing two images from each individual's folder.

Example:
    To run the test, use the following command:
    ```shell
    python -m unittest test_face_compare.py
    ```
"""


import unittest
import os
import sys

from face_compare.face_compare import compare_faces  # Import the compare_faces function
from face_extraction.face_extractor import extract_face  # Import the compare_faces function

class TestCompareFaces(unittest.TestCase):
    def test_compare_faces(self):
        test_faces_dir = 'test_faces'

        # Loop through each person folder
        for person_folder in os.listdir(test_faces_dir):
            person_folder_path = os.path.join(test_faces_dir, person_folder)

            # Check if it's a directory
            if os.path.isdir(person_folder_path):
                # List all files in the person's folder
                files = os.listdir(person_folder_path)

                # Ensure there are at least two files (faces) to compare
                self.assertGreaterEqual(len(files), 2, f"Insufficient test files in {person_folder}. Ensure there are at least 2 images.")

                # Load the first two faces in the folder
                face_1_path = os.path.join(person_folder_path, files[0])
                face_2_path = os.path.join(person_folder_path, files[1])

                #Extract each face using the existing function
                face_1_extracted = extract_face(face_1_path)
                face_2_extracted = extract_face(face_2_path,)

                #Face comparison test occurs here
                result = compare_faces(face_1_extracted, face_2_extracted)
                print(person_folder, "result:", result)

if __name__ == '__main__':
    unittest.main()
