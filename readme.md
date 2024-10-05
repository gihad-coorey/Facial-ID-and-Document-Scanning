# J Forex Money Transfer: Liveliness Check Software

## Introduction
J Forex Money Transfer is a service that enables customers to send money online securely and quickly. J Forex has engaged the University of Western Australia (Professional Computing unit - CITS3200) to develop a liveliness check so they may align with current legislative requirements. 

This software first extracts the image of a users' face from an identifying document (such as a passport or driver's licence). It then commences a passive liveliness check, where a user livestreams their face and their blinking frequency is assessed. If this fails, they will then be shown a randomised selection of prompts. These prompts include various hand gestures (for example, "open-palm" or "thumbs up"). This checks whether the user can respond in real time, and finally compares the images captured in the livestream to the extracted face from the document. 


This software utilises MediaPipe for the liveliness check, face_recognition, and OpenCV to support its functionality. 


<br>

## Table of Contents

- [User Navigation](#user-navigation)
- [Feature Overview](#special-features)
- [Face Extraction](#face-extraction)
- [Liveliness Check](#liveliness-check)
- [Face Matching](#face-matching)
- [Design and Development](#design-and-development)
- [Getting Started](#getting-started)
- [Attributions](#attributions)
- [Support](#support)
- [Contributors](#contributors)

<br>

## User (J Forex customer) Navigation

To utilise this software, users should be directed to provide an image of their identifying documentation (such as a passport or driver licence). Once having captured this image, the user will be informed as to whether their face was able to be extracted from the provided image. If successful, they commence to liveliness check. If unsuccessful, they repeat this step.

The liveliness check commences by recording a livestream of the user's face, acting as an anti-spoofing technique. Based on passive techniques (measuring the blinking frequency of the user), the user may complete this phase. If the blinking method was unsuccessful, the user will continue on to an active check, where they will be required to follow prompts displayed on the screen (hand gesture prompts). If this active check also fails, the user will be required to repeat this stage.

Finally, if the outcome of the facial comparison (where the face from the ID is compared to an image extracted from the livestream) is determined to not be a match, they will be required to repeat the entire process again.

<br>

## Feature Overview
- Face Extraction: Extracts a user's face from ID.
- Liveliness Check: Uses video and gesture analysis to confirm the liveliness of a user as an anti-spoofing technique.
- Face Matching: Compares the extracted face with the one from the liveliness check to confirm identity.

### Face Extraction
The face extraction feature extracts the user's face from their identifying documentation. The script first utilises an image provided by the user. Utilising this image, MediaPipe will extract the user's face. If no face can be found, the program will print a statement informing the user with a general list of requirements (i.e. ensure you have good lighting, the camera is in focus, etc). This script returns a Boolean representing the outcome of face extraction.

### Liveliness Check
The liveliness check uses MediaPipe and will first utilise the user's camera. It will begin livestreaming and commence a 'passive' check. Note that the user is required to position their head within the red frame. This initial check analyses blinking frequency and requires less effort from the user. If this check passes, face comparison begins. If the check fails, the liveliness program will commence an 'active' check. The active check randomly displays prompts for the user to follow (composed of various hand gestures) and will evaluate the user's ability to follow these instructions. If the user was able to successfully follow these prompts, face comparison begins. Else, this step must be repeated. The liveliness function will return a Boolean value representing the outcome of the liveliness check.

This process aims to produce a secure liveliness check with anti-spoofing properties. 

### Face Matching
This is the final stage in the process. During the liveliness check, a still will be captured when a user successfully demonstrates their liveliness. Comparing this still to the extracted face from identifying documentation, this feature will deduce whether the user in the liveliness check is the same individual featured in the documentation. The face matching feature will return a Boolean value representing the outcome facial comparison. 


<br>

## Design and Development
This program was developed utilising well-maintained and highly-regarded APIs. Here are some of the key aspects of the design and development process:
### Technologies Utilised
- Python 3
- OpenCV
- Mediapipe
- Additional dependencies are listed in the 'requirements.txt' file 


### Testing and Quality Assurance
Our development prioritises testing and quality assurance to ensure a reliable and robust user experience. We have implemented a comprehensive series of tests using the unittest framework for all of our features. These tests include functionality tests for features like face extraction, liveliness checks, face comparison and anti-spoofing methods. There will also be an integration test that ensures the entire program runs correctly and can handle returned false Boolean values. To run the described tests for this program, navigate to project directory (CITS3403) and execute the test files. This can be done by running the commands below in the terminal or command prompt.

1. Face Extractor Test: 
    ```bash
    python -m unittest tests/test_face_extractor.py
    ```
2. Face Comparison Test:
    ```bash
    python3 -m unittest tests/test_face_compare.py

### Security Considerations
The security considerations within this software largely come from the passive and active liveliness checks. The passive check ensures a real person is blinking, whilst the active takes on a more intensive approach, requiring hand gestures and following instructions. This prevents the utilisation of images to pass a liveliness check, as well as video footage (as following instructions will be required). 

### Scalability and Deployment - Information for J Forex IT Department 
The following section  outlines considerations for the J Forex IT Department's integration of this software into their application. Due to the nature of this project, no user interface (UI) has been included. Instead, the functionality of these main features should be utilised as the back-end for the liveliness check process and a front-end should be developed to support this.

J Forex IT employees should note the following:
- The **face extraction function requires the passing in of the identifying documentation image**. When integrating this software, this should utilise the user's camera to capture the image (which was outside the scope of this project). 
- The ID image should be deposited in the **test_ids** folder with the name of **TEST_IMAGE.jpg**.
- The features utilised all specify a threshold for the resulting Boolean values. This can be altered to increase or decrease sensitivity where required. Legislation should be followed to determine the appropriate accuracies. These can be found in:
    - face_detection_utils.py
    - liveliness_check.py
- The sensitivity of the passive blink test works best when the user's face is close to the camera. We recommend an oval face-alignment shape is added to the UI to reduce false negative results (i.e. reducing the number of users who do not pass the passive check). Currently, a red frame has been overlayed for the demonstration of this product.
- Set constants in liveliness_check.py to be dependent on the user's device type and camera size.
- The printed statements in the terminal consist of a combination of developer remarks (assist in the development of the features) and user remarks  (assist the user in progressing through the liveliness check). The developers should display the user remarks with the UI for the user to follow.
- Additionally, this software displays the webcam feed with the mapping of facial features and hand gestures. It may be preferable for the mapping  to be hidden from users and can be done so in front-end design.

For scalability, the use of well-maintained APIs ensures that managing increasing usage is possible. MediaPipe is currently an opensource/free API and its permissions allow commercial use. 


<br>

## Getting Started
This guides’ target audience is the IT department at J Forex Money Transfer. This software is intended to be implemented into their application to provide the functionality for a liveliness check. This will assist the company in meeting legal requirements to ensure the identity of their customers has been proven.
### Installation
1. Clone the repository
    ```bash
    git clone https://github.com/AbhinavDevelops/Facial-ID-and-Document-Scanning.git
    ```
2. Navigate to the project directory
    ```bash
    cd Facial-ID-and-Document-Scanning
    ```
3. Setup Python Environment: 
    ```bash
    python -m venv venv
    ```
4. Activate Environment: 
    Unix:
    ```bash
    source venv/bin/activate
    ``` 
    Windows:
    ```bash
    .\venv\Scripts\activate
    ``` 
5. (Windows) If you encounter a security error while activating the virtual environment, try this:
    ```bash
    Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
    ```
    Then run this again:
    ```bash
    .\venv\Scripts\activate
    ```
6. Install Required Packages: 
    ```bash
    pip install -r requirements.txt
    ```
7. Insert Identification Document Image into THE "test_ids" Folder. 
    Ensure it is named "TEST_IMAGE.jpg".

### Run Program
1. Start the Application:
    ```bash
    python main.py
    ```

### Test Instructions

### Face Extractor Test
1. Navigate to the root directory and run the following:
```bash
python3 -m unittest tests/test_face_extractor.py
```
2. Wait a few moments and you will see probabilities for the associated extracted face, or it will tell you if a face was not able to be found.
- Note: Feel free to add some images to the test_ids folder if you want to test additional images

### Image vs Liveliness Comparison Test
1. Navigate to the root directory and run the following:
```bash
python3 -m unittest tests/test_face_compare.py
```
2. The script will access each person folder in the test_faces folder. Each person folder contains 2 images. The script will check if each pair of images contains the same person. 

3. Wait a few moments and you will see probabilities for the associated extracted face, or it will tell you if a face was not able to be found. You will see a "True" result if the person image folder contains two images of the same person. You will see a "False" result if the image folder contains two images of different people.
- Note: Feel free to add some images to the test_faces folder if you want to test additional images. The images provided are from www.pexels.com and www.pixabay.com.
    

### Troubleshooting: Windows users
Due to the use of dlib, the user is required to have the necessary build tools installed. dlib requires Visual Studio with C++ support to be built on Windows (such as the use of [CMake](https://cmake.org/download/)). The contributors utilising a Windows operating system elected to install the Desktop Development with C++ workload within [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/). After installation on Visual Studio, the code ran on Visual Studio Code. See the image below for the relevant workload installation:

![Visual Studio Build Tools C++](images/VS_BuildTools_C++.png)


<br>

## Attributions
- Please view the requirements.txt file for a detailed listing of all external libraries utilised
- Googles' MediaPipe API was utilised across multiple features in this programme (https://developers.google.com/mediapipe)
- OpenCV was also utlised to support the development of these features (https://opencv.org/)
- Face recognition was utilised to compare the face extracted from the identification documentation to the liveliness stream (https://pypi.org/project/face-recognition/)
- Images used for test face comparison sourced from www.pexels.com and www.pixabay.com

<br>

## Support
Please contact one of the contributors (listed below). Alternatively, contact the Unit Coordinator of Professional Computing at UWA (CITS3200), Michael Wise:
michael.wise@uwa.edu.au

<br>

## Contributors
- Abhinav Rajaram (23082057): 23082057@student.uwa.edu.au
- Alison Jeon (22835304): 22835304@student.uwa.edu.au
- Gihad Coorey (23091788): 23091788@student.uwa.edu.au
- Julia Celiberti  (22891889): 22891889@student.uwa.edu.au
- Matt Masel (20518121): 20518121@student.uwa.edu.au
- William Shields (23280485): 23280485@student.uwa.edu.au

This project was supported by the guidance of its auditor, Dr Zulqarnain Gilani.
<br>