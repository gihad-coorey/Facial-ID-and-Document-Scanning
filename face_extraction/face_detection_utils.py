"""
Face Detection and Cropping Utility Functions

This module provides utility functions to assist in facial detection and image
processing, particularly converting normalised coordinates to pixel coordinates, 
selecting the face with the highest detection probability, and cropping an image 
to focus on a detected face.

Dependencies:
    - math (standard library)
    - numpy as np
    - Tuple, Union from typing module (standard library)

Functions:
    - _normalized_to_pixel_coordinates: Converts normalized coordinates to pixel coordinates.
    - get_highest_probability_face: Selects the face detection with the highest probability.
    - crop_face: Crops the input image around the detected face.
"""


from . import Tuple, Union, math, np

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px

def get_highest_probability_face(detection_result):
  """Incase ID has multiple images it selects the face with the highest probability
  Args:
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Highest probability detection
  """
  highest_probability = 0.0
  highest_probability_face = None

  for detection in detection_result.detections:
    probability = detection.categories[0].score

    if probability > highest_probability:
      highest_probability = probability
      highest_probability_face = detection

  return highest_probability_face

def crop_face(image, detection_result) -> np.ndarray:
  """Draws bounding boxes on the input image crops and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Cropped image of face.
  """
  detection = get_highest_probability_face(detection_result)

  # Draws border around face
  bbox = detection.bounding_box
  x = bbox.origin_x
  y = bbox.origin_y
  width = bbox.width
  height = bbox.height

  # Expand the border, 20 = 20px extra boarder, can modify as needed for face comparison
  x -= 20
  y -= 20
  width += 2 * 20
  height += 2 * 20

  # Checks the border is within the original image boundaries
  x = max(x, 0)
  y = max(y, 0)
  width = min(width, image.shape[1] - x)
  height = min(height, image.shape[0] - y)

  cropped_face_image = image[y:y+height, x:x+width]
  probability = detection.categories[0].score

  if probability > 0.8:
    print(f"Probability image contains a face = ", probability)    # TESTING
    return cropped_face_image
  
  else: 
    return None