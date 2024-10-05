"""
Liveliness Checker

This module provides functions to assess the liveliness of a person based on both passive 
and active methodologies using the MediaPipe library. It incorporates:
    - Passive checks which involve face and blink detection.
    - Active checks which guide the user through a series of gesture prompts.

Dependencies:
    - OpenCV (cv2)
    - MediaPipe (mediapipe)

Constants:
    - MIN_FACE_DETECTION_CONFIDENCE: Minimum confidence level for face detection.
    - MIN_HAND_DETECTION_CONFIDENCE: Minimum confidence level for hand detection.
    - MIN_BLINK_RATIO: Minimum ratio to identify a blink.
    - MIN_NUM_BLINKS: Minimum number of blinks required during passive check.
    - PASSIVE_CHECK_WAIT_TIME: Duration for the passive check.
    - ACTIVE_CHECK_WAIT_TIME: Duration for each prompt in the active check.
    - MAX_ACTIVE_CHECK_ATTEMPTS: Maximum number of prompts user gets in the active check.
    - NUM_ACTIVE_SUCCESSES: Number of successful prompts needed to pass the active check.
    - FRAME_WIDTH: Width of the frame.
    - FRAME_HEIGHT: Height of the frame.
    - FACE_BOX_WIDTH: Width of the face bounding box.
    - FACE_BOX_HEIGHT: Height of the face bounding box.
    - FACE_BOX_XMIN: Leftmost coordinate of the face bounding box.
    - FACE_BOX_YMIN: Topmost coordinate of the face bounding box.

Functions:
    - passive_check(cap): Perform passive face & blink detection.
      Parameters:
        cap: A livestream video capture.
      Returns:
        An image of the detected face, and a flag indicating whether passive check was passed.

    - active_check(cap): Active liveliness checker using prompt-directed gesture recognition.
      Parameters:
        cap: A livestream video capture.
      Returns:
        An image of the detected face, and a flag indicating whether active check was passed.

    - liveliness_check(): Combination liveliness checker using passive and active tests.
      Returns:
        An image of the face if it passes the liveliness check, else None.
"""




import os
import cv2
from mediapipe import tasks, solutions
from time import time

if __name__ != '__main__':
  # local directory imports
  from . import active_utils as active
  from . import passive_utils as passive
  from . import liveliness_utils as liveliness

# CONSTANTS
MIN_FACE_DETECTION_CONFIDENCE = 0.7
MIN_HAND_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.5
MIN_BLINK_RATIO = 4.7
MIN_NUM_BLINKS = 3
PASSIVE_CHECK_WAIT_TIME = 5
ACTIVE_CHECK_WAIT_TIME = 20
MAX_ACTIVE_CHECK_ATTEMPTS = 6
NUM_ACTIVE_SUCCESSES = 3

FRAME_WIDTH = 1800  # Change this to your desired frame width
FRAME_HEIGHT = 1000  # Change this to your desired frame height
FACE_BOX_WIDTH = 600
FACE_BOX_HEIGHT = 500
FACE_BOX_XMIN = (FRAME_WIDTH - FACE_BOX_WIDTH)//2
FACE_BOX_YMIN = (FRAME_HEIGHT - FACE_BOX_HEIGHT)//2

FONT = cv2.FONT_HERSHEY_COMPLEX

# Mediapipe hands and face detection modules
mp_face_detection = solutions.face_detection
mp_face_mesh = solutions.face_mesh
mp_hands = solutions.hands
mp_drawing = solutions.drawing_utils


""" Perform passive face & blink detection.
@param: a livestream video capture.
@return: an image of the detected face, and a flag indicating whether passive check was passed. """
def passive_check(cap):
  blink_counter = 0
  is_blinking = False
  start_time = int(time())

  with mp_face_detection.FaceDetection(min_detection_confidence=MIN_FACE_DETECTION_CONFIDENCE) as face_detection:
    with mp_face_mesh.FaceMesh(min_detection_confidence=MIN_FACE_DETECTION_CONFIDENCE, min_tracking_confidence=MIN_TRACKING_CONFIDENCE) as face_mesh:
      while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
          print("Error: Failed to read a frame from the webcam.")
          continue

        frame = cv2.flip(frame, 1)
        
        # Convert the frame to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_height, rgb_width, channel = rgb_frame.shape
        cv2.rectangle(rgb_frame, (FACE_BOX_XMIN, FACE_BOX_YMIN), (FACE_BOX_XMIN + FACE_BOX_WIDTH, FACE_BOX_YMIN + FACE_BOX_HEIGHT), (0, 0, 255), 2)

        # Draw face box
        facebox = liveliness.get_face_box(face_detection, rgb_frame, rgb_width, rgb_height)
        if facebox is None:
          continue
        face_x,face_y,face_width,face_height = facebox
        cv2.rectangle(rgb_frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (0, 255, 0), 2)

        # Calculate the intersection area between the detected face and the face box
        intersection = liveliness.calc_intersection_area((face_x, face_y, face_width, face_height), (FACE_BOX_XMIN, FACE_BOX_YMIN, FACE_BOX_WIDTH, FACE_BOX_HEIGHT))

        # Check if the face is inside the specified rectangle
        if(intersection < face_width * face_height * 0.95):
          cv2.putText(rgb_frame, "Face not detected in box", (FACE_BOX_XMIN, FACE_BOX_YMIN - 10), FONT, 1, (100, 255, 0), 2)
        else:
          face_mesh_coords = liveliness.get_face_mesh(face_mesh, rgb_frame, rgb_width, rgb_height)
          if face_mesh_coords is None:
            print("Face mesh not found")
            continue

          cv2.putText(rgb_frame, "Face detected!", (FACE_BOX_XMIN, FACE_BOX_YMIN - 10), FONT, 1, (0, 255, 0), 2)

          # Blink debouncing logic
          if(passive.get_blink_state(rgb_frame, face_mesh_coords, MIN_BLINK_RATIO)):
            is_blinking = True
          elif is_blinking:
            is_blinking = False
            blink_counter += 1

        
        cv2.putText(rgb_frame, f'Total Blinks {blink_counter}', (30, 150), FONT, 1.7, (0, 0, 255), 1)
        cv2.putText(rgb_frame, f'Time elapsed {round(time() - start_time, 2)}', (30, 200), FONT, 1.1, (255, 255, 255), 1)

        # Check passive liveliness and set flags as needed
        if int(time()) - start_time == PASSIVE_CHECK_WAIT_TIME:
          if blink_counter < MIN_NUM_BLINKS:
            print(f"Passive check failed with {blink_counter} blinks in {PASSIVE_CHECK_WAIT_TIME} seconds.")
            passive_check_passed = False
            return None, passive_check_passed

          passive_check_passed = True
          extracted_face = frame.copy()#[FACE_BOX_Y:FACE_BOX_Y + FACE_BOX_HEIGHT, FACE_BOX_X:FACE_BOX_X + FACE_BOX_WIDTH]
          print(f"Passive check passed with {blink_counter} blinks in {PASSIVE_CHECK_WAIT_TIME} seconds!")
          return extracted_face, passive_check_passed
        
        cv2.imshow('Webcam Liveliness Test', cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
        
        key = cv2.waitKey(20) & 0xFF
        if key == ord('q') or key == ord('Q'):  # quit
          cap.release()
          cv2.destroyAllWindows()
          break
        if key == ord('r') or key == ord('R'):  # restart
          blink_counter = 0
          is_blinking = False
          start_time = int(time())
          print("Restarting passive check...")
          continue
      
  return None, False

""" Active liveliness checker using prompt-directed gesture recognition.
@param: a livestream video capture.
@return: an image of the detected face, and a flag indicating whether active check was passed. """
def active_check(cap):
  model_path = os.path.join('liveliness_check', 'gesture_recognizer.task')
  model_file = open(model_path, "rb")
  model_asset_buf = model_file.read()
  model_file.close()

  # Define the gesture recognition modules
  BaseOptions = tasks.BaseOptions
  GestureRecognizer = tasks.vision.GestureRecognizer
  GestureRecognizerOptions = tasks.vision.GestureRecognizerOptions
  VisionRunningMode = tasks.vision.RunningMode

  # Configure a GestureRecognizer object to recognise the pre trained gestures from the Google model.
  gestureOptions = GestureRecognizerOptions(
    base_options = BaseOptions(model_asset_buffer=model_asset_buf),
    running_mode = VisionRunningMode.IMAGE,
    min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
    )
  
  num_attempts = 0
  num_correct = 0
  current_prompt = active.get_prompt(None)
  start_time = int(time())

  # Initialize the face detection, face mesh, and hand tracking models
  with mp_face_detection.FaceDetection(min_detection_confidence=MIN_FACE_DETECTION_CONFIDENCE) as face_detection:
    with mp_hands.Hands(min_detection_confidence=MIN_HAND_DETECTION_CONFIDENCE) as hands:
      with GestureRecognizer.create_from_options(gestureOptions) as recogniser:
        while cap.isOpened():
          ret, frame = cap.read()
          if not ret:
            print("Error: Failed to read a frame from the webcam.")
            continue

          if num_attempts >= MAX_ACTIVE_CHECK_ATTEMPTS:
            print(f"Failed to detect required gesture {MAX_ACTIVE_CHECK_ATTEMPTS} times. Liveliness check failed.")
            break

          time_left = ACTIVE_CHECK_WAIT_TIME + start_time - int(time())
          if(time_left == 0):
            print(f"Failed with prompt {current_prompt}!")
            time_left = ACTIVE_CHECK_WAIT_TIME
            num_attempts += 1
            current_prompt = active.get_prompt(current_prompt)
            start_time = int(time())
          
          # Convert the frame to RGB for Mediapipe
          rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          rgb_frame = cv2.flip(rgb_frame, 1)
          rgb_height, rgb_width, channel = rgb_frame.shape
          cv2.rectangle(rgb_frame, (FACE_BOX_XMIN, FACE_BOX_YMIN), (FACE_BOX_XMIN + FACE_BOX_WIDTH, FACE_BOX_YMIN + FACE_BOX_HEIGHT), (0, 0, 255), 2)

          # Draw face box
          facebox = liveliness.get_face_box(face_detection, rgb_frame, rgb_width, rgb_height)
          if facebox is None:
            continue
          face_x,face_y,face_width,face_height = facebox
          cv2.rectangle(rgb_frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (255, 0, 0), 2)

          # Check if the face is inside the specified rectangle
          intersection = liveliness.calc_intersection_area((face_x, face_y, face_width, face_height), 
                                                            (FACE_BOX_XMIN, FACE_BOX_YMIN, FACE_BOX_WIDTH, FACE_BOX_HEIGHT))
          
          if(intersection < face_width * face_height * 0.85):
            cv2.putText(rgb_frame, "Face not detected in box", (FACE_BOX_XMIN, FACE_BOX_YMIN - 10), FONT, 1, (100, 255, 0), 2)
          else:
            cv2.putText(rgb_frame, "Face detected!", (FACE_BOX_XMIN, FACE_BOX_YMIN - 10), FONT, 1, (0, 255, 0), 2)
            
            # Draw hands
            liveliness.draw_hands(hands, rgb_frame)
            
          # Display the current prompt
          cv2.putText(rgb_frame, f"Prompt #{num_attempts+1}: {current_prompt}", (20, 350), FONT, 1, (0, 0, 255), 2)
          cv2.putText(rgb_frame, f"{time_left} secs left...", (20, 400), FONT, 1, (0, 0, 255), 2)

          # Will return as soon as one successful frame is seen; ie. benefit of the doubt given to the user
          if active.check_gesture(recogniser, cv2.flip(rgb_frame,1), current_prompt):
            print(f"Passed active with prompt {current_prompt}!")
            num_correct += 1
            num_attempts += 1
            current_prompt = active.get_prompt(current_prompt)
            start_time = int(time())
            if num_correct >= NUM_ACTIVE_SUCCESSES:
              extracted_face = frame.copy()#[FACE_BOX_Y:FACE_BOX_Y + FACE_BOX_HEIGHT, FACE_BOX_X:FACE_BOX_X + FACE_BOX_WIDTH]
              return extracted_face, True
          
          cv2.imshow('Webcam Liveliness Test', cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
          
          key = cv2.waitKey(20) & 0xFF
          if key == ord('q') or key == ord('Q'):  # quit
            cap.release()
            cv2.destroyAllWindows()
            break
          if key == ord('r') or key == ord('R'):  # restart
            num_attempts = 0
            current_prompt = active.get_prompt(None)
            start_time = int(time())
            print("Restarting active check...")
            continue

  return None, False

""" Combination liveliness checker using passive and active tests.
@return: An image of the face if it passes the liveliness check, else None."""
def liveliness_check():

  cap = liveliness.init_camera(FRAME_WIDTH, FRAME_HEIGHT)
  
  extracted_face, passive_check_passed = passive_check(cap)
  if passive_check_passed:
    print("Passive check passed!")
    cap.release()
    cv2.destroyAllWindows()
    return extracted_face
  
  print("Passive check failed. Beginning active check.")
  extracted_face, active_check_passed = active_check(cap)
  if active_check_passed:
    print("Active check passed!")
    cap.release()
    cv2.destroyAllWindows()
    return extracted_face
  
  print("Liveliness check failed!")
  cap.release()
  cv2.destroyAllWindows()
  return None

if __name__ == "__main__":
  import active_utils as active
  import passive_utils as passive
  import liveliness_utils as liveliness

  extracted_face = liveliness_check()

  if extracted_face is None:
    print("Face not detected. Please retry liveliness check.")
    exit(0)
  
  cv2.imshow('Extracted Face', extracted_face)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

