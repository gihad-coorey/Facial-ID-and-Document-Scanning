"""
Eye Blinking Detection and Ratio Calculation

This module provides utility functions to detect eye blinking and calculate 
the eye ratio using facial landmarks detected by the MediaPipe library. It includes functions to:
    - Calculate the Euclidean distance between two points.
    - Calculate the eye ratio based on facial landmarks.
    - Determine whether eyes are blinking based on a given ratio threshold.
    
Dependencies:
    - OpenCV (cv2)
    - math (for sqrt function)

Functions:
    - euclideanDistance: Calculates the Euclidean distance between two points.
    - eyeRatio: Calculates the eye ratio based on facial landmarks.
    - get_blink_state: Determines whether eyes are blinking based on a given ratio threshold.
"""


from math import sqrt
import cv2

# face bounder indices 
FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]

# lips indices for Landmarks
LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]

# Euclaidean distance 
def euclideanDistance(point, point1):
  """
  Calculate the Euclidean distance between two points.

  Parameters:
      point, point1 (tuple of int): The (x, y) coordinates of the two points.

  Returns:
      float: The Euclidean distance between the two points.

  Example:
      >>> euclideanDistance((1,2), (3,4))
      2.8284271247461903
  """
  x, y = point
  x1, y1 = point1
  distance = sqrt((x1 - x)**2 + (y1 - y)**2)
  return distance

# Blinking Ratio
def eyeRatio(img, landmarks, right_indices, left_indices):
  """
  Calculate the eye ratio based on facial landmarks.

  Parameters:
      img (np.ndarray): The image containing the face.
      landmarks (list of tuple): The facial landmarks as (x, y) coordinates.
      right_indices, left_indices (list of int): Indices of landmarks for right and left eyes.

  Returns:
      float: The average eye ratio calculated using specified landmarks.

  Note:
      - Assumes 'landmarks' contain valid facial landmarks obtained from a facial landmark detector.
      - 'right_indices' and 'left_indices' should contain valid indices corresponding to eye landmarks.
  """
  # Right eyes 
  rh_right = landmarks[right_indices[0]]
  rh_left = landmarks[right_indices[8]]
  # vertical line 
  rv_top = landmarks[right_indices[12]]
  rv_bottom = landmarks[right_indices[4]]
  # draw lines on right eyes 

  # LEFT_EYE 
  lh_right = landmarks[left_indices[0]]
  lh_left = landmarks[left_indices[8]]

  # vertical line 
  lv_top = landmarks[left_indices[12]]
  lv_bottom = landmarks[left_indices[4]]

  rhDistance = euclideanDistance(rh_right, rh_left)
  rvDistance = euclideanDistance(rv_top, rv_bottom)

  lvDistance = euclideanDistance(lv_top, lv_bottom)
  lhDistance = euclideanDistance(lh_right, lh_left)

  reRatio = rhDistance/rvDistance
  leRatio = lhDistance/lvDistance

  ratio = (reRatio+leRatio)/2
  return ratio 

def get_blink_state(rgb_frame, mesh_coords, min_blink_ratio):
  """
  Determine whether eyes are blinking based on a given ratio threshold.

  Parameters:
      rgb_frame (np.ndarray): The frame (image) containing the face.
      mesh_coords (list of tuple): The facial landmarks as (x, y) coordinates.
      min_blink_ratio (float): The threshold below which the eyes are considered as blinking.

  Returns:
      bool: True if eyes are blinking, False otherwise.

  Note:
      - Assumes 'mesh_coords' contain valid facial landmarks obtained from a facial landmark detector.
      - If the calculated eye ratio is greater than 'min_blink_ratio', eyes are considered as blinking.
  """
  eye_ratio = eyeRatio(rgb_frame, mesh_coords, RIGHT_EYE, LEFT_EYE)
  (t_w, t_h), _= cv2.getTextSize(f'Ratio : {round(eye_ratio,2)}', cv2.FONT_HERSHEY_COMPLEX, 0.7, 1) # getting the text size
  x,y = (30,100)
  padding = 3
  cv2.rectangle(rgb_frame, (x-padding, y+padding), (x+t_w+padding, y-t_h-padding), (0,0,0), -1) # draw rectangle 
  cv2.putText(rgb_frame,f'Ratio : {round(eye_ratio,2)}', (x,y),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 1) # draw in text
  return eye_ratio > min_blink_ratio
