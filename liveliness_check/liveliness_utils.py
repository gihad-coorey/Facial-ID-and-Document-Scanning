"""
Liveliness Utilities

This module provides utility functions to detect and annotate faces and hands 
in an image using the MediaPipe library. It includes functions to:
    - Draw bounding boxes around detected faces.
    - Draw landmarks and connections on detected hands.
    - Draw facial landmarks using a facial mesh.

Dependencies:
    - OpenCV (cv2)
    - MediaPipe (mediapipe)

Functions:
    - draw_face_box: Draws a bounding box around the detected face in an image.
    - draw_hands: Draws landmarks and connections on detected hands in an image.
    - draw_face_mesh: Draws facial landmarks using a facial mesh.
"""

import cv2
from mediapipe import solutions

# Mediapipe hands and face detection modules
mp_face_detection = solutions.face_detection
mp_face_mesh = solutions.face_mesh
mp_hands = solutions.hands
mp_drawing = solutions.drawing_utils

"""
  Draw a bounding box around the detected face in an image.

  Parameters:
      mp_task: The MediaPipe task used for face detection.
      rgb_frame (np.ndarray): The frame (image) in which to detect and annotate the face.
      frame_width (int): Width of the frame.
      frame_height (int): Height of the frame.

  Returns:
      detections: The detected faces in the frame.

  Note:
      - The function annotates 'rgb_frame' with a bounding box around the detected face.
      - Assumes 'mp_task' is a configured and ready-to-use MediaPipe task for face detection.
  """
#def draw_face_box(mp_task, rgb_frame, frame_width, frame_height):
def get_face_box(mp_task, rgb_frame, frame_width, frame_height):
  detected_faces = mp_task.process(rgb_frame).detections
  if detected_faces:
    detected_face = detected_faces[0] # take first detected face
    face_box = detected_face.location_data.relative_bounding_box
    face_x, face_y, face_width, face_height = int(face_box.xmin * frame_width), int(face_box.ymin * frame_height), int(face_box.width * frame_width), int(face_box.height * frame_height)
    #cv2.rectangle(rgb_frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (0, 255, 0), 2)
    return face_x, face_y, face_width, face_height
  return None
            
  """
  Draw landmarks and connections on detected hands in an image.

  Parameters:
      mp_task: The MediaPipe task used for hand detection.
      rgb_frame (np.ndarray): The frame (image) in which to detect and annotate hands.
      frame_width (int): Width of the frame.
      frame_height (int): Height of the frame.

  Returns:
      multi_hand_landmarks: The detected hand landmarks in the frame.

  Note:
      - The function annotates 'rgb_frame' with landmarks and connections on the detected hands.
      - Assumes 'mp_task' is a configured and ready-to-use MediaPipe task for hand detection.
  """
def draw_hands(mp_task, rgb_frame):
  detected_hands = mp_task.process(rgb_frame).multi_hand_landmarks
  if detected_hands:
    for hand in detected_hands:
      mp_drawing.draw_landmarks(rgb_frame, hand, mp_hands.HAND_CONNECTIONS)
  return detected_hands

  """
  Draw facial landmarks using a facial mesh.

  Parameters:
      mp_task: The MediaPipe task used for facial landmark detection.
      rgb_frame (np.ndarray): The frame (image) in which to detect and annotate facial landmarks.
      frame_width (int): Width of the frame.
      frame_height (int): Height of the frame.

  Returns:
      list of tuple or None: A list of (x, y) tuples representing the detected facial landmarks, 
                              or None if no face is detected.

  Note:
      - The function annotates 'rgb_frame' with facial landmarks using a facial mesh.
      - Assumes 'mp_task' is a configured and ready-to-use MediaPipe task for facial landmark detection.
  """
  
#def draw_face_mesh(mp_task, rgb_frame, frame_width, frame_height):
def get_face_mesh(mp_task, rgb_frame, frame_width, frame_height):
  detected_faces = mp_task.process(rgb_frame).multi_face_landmarks
  if detected_faces:
    detected_face = detected_faces[0] # take first detected face
    mp_drawing.draw_landmarks(rgb_frame, detected_face, mp_face_mesh.FACEMESH_CONTOURS, 
                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1), 
                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1))
    return [(int(landmark.x * frame_width), int(landmark.y * frame_height)) for landmark in detected_face.landmark]
  return None

def is_inside_rect(point, rect):
    x, y, w, h = rect
    return (x <= point[0] <= x + w and y <= point[1] <= y + h)

def calc_intersection_area(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))

    return x_overlap * y_overlap

def init_camera(frame_width, frame_height):
  cap = cv2.VideoCapture(0)
  cap.set(3, frame_width)
  cap.set(4, frame_height)
  if not cap.isOpened():
    print("Error: Failed to open the webcam.")
    exit(1)
  return cap
