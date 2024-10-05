"""
Active Liveliness Check with Gesture Recognition

This module provides utility functions for performing active liveliness checks and recognising 
specific gestures in an image using the MediaPipe library. It includes functions to:
    - Generate random prompts for active liveliness tests.
    - Check if specific gestures are performed based on the prompts.
    - Recognise and validate the user's gesture in a given frame.

Dependencies:
    - OpenCV (cv2)
    - MediaPipe (mediapipe)
    - random

Functions:
    - get_prompt: Generates random prompts for active liveliness tests or retrieves the function to check a specific prompt.
    - check_left_peace, check_right_peace, check_left_palm, check_left_thumbs_up, check_right_palm, check_right_thumbs_up: Validate specific user gestures.
    - check_gesture: Recognises and validates the user's gesture in a given frame.
"""


import cv2
from mediapipe import Image, ImageFormat
from random import choice as random_choice

# Function to generate random prompts for active liveliness tests
def get_prompt(current, return_checker_function=False):
    """
    Generate a random prompt for liveliness tests or retrieve a function to check a specific prompt.
    
    Parameters:
        current (str): The current active prompt.
        return_checker_function (bool, optional): If True, returns the function to check the 'current' prompt. Defaults to False.
    
    Returns:
        str or function: If return_checker_function is False, returns a new random prompt different from 'current'. 
                         If True, returns the function to check the 'current' prompt.
    """

    prompts = {
        "Throw a peace sign": check_peace_sign,
        "Show your palm": check_palm,
        "Do a thumbs up": check_thumbs_up,
    }
    if not return_checker_function:
        prompt = random_choice(list(prompts.keys()))
        if prompt == current: # don't want the same prompt twice in a row
            prompt = get_prompt(current)
        return prompt
    return prompts[current] # return the correct checker function if the flag is set

def check_peace_sign(user_gesture):
    return "Victory" in user_gesture

def check_palm(user_gesture):
    return "Open_Palm" in user_gesture

def check_thumbs_up(user_gesture):
    return "Thumb_Up" in user_gesture

def check_gesture(task, rgb_frame, current_prompt):
   
   
   """
  Recognise and validate the user's gesture in a given frame.

  Parameters:
      task: The MediaPipe task used for gesture recognition.
      rgb_frame (np.ndarray): The frame (image) in which to recognize the gesture.
      current_prompt (str): The current active prompt for which the user's gesture should be checked.

  Returns:
      bool: True if the user successfully performs the gesture corresponding to 'current_prompt', otherwise False.

  Note:
      - The function also annotates 'rgb_frame' with the recognized gesture and whether the user was successful 
        in performing the correct gesture.
      - Assumes 'task' is a configured and ready-to-use MediaPipe task for gesture recognition.
  """
   mp_frame = Image(image_format=ImageFormat.SRGB, data=rgb_frame)
   result = task.recognize(mp_frame)

   if(result.gestures == [] or result.handedness == [] or
        result.gestures[0][0].category_name == "None" or
        result.handedness[0][0].category_name == "None"):
        return False

   current_user_gesture = f"{result.gestures[0][0].category_name} {result.handedness[0][0].category_name} Hand"

   success = get_prompt(current_prompt, return_checker_function=True)(current_user_gesture)
   return success
