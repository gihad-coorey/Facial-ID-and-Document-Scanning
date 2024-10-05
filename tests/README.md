# Test Instructions

## Face Extractor Test
1. Navigate to the root directory and run the following:
```bash
python3 -m unittest tests/test_face_extractor.py
```
2. Wait a few moments and you will see probabilities for the associated extracted face, or it will tell you if a face was not able to be found.
- Note: Feel free to add some images to the test_ids folder if you want to test additional images

## Image vs Liveliness Comparison Test
1. Navigate to the root directory and run the following:
```bash
python3 -m unittest tests/test_face_compare.py
```
2. The script will access each person folder in the test_faces folder. Each person folder contains 2 images. The script will check if each pair of images contains the same person. 

3. Wait a few moments and you will see probabilities for the associated extracted face, or it will tell you if a face was not able to be found. You will see a "True" result if the person image folder contains two images of the same person. You will see a "False" result if the image folder contains two images of different people.
- Note: Feel free to add some images to the test_faces folder if you want to test additional images. The images provided are from www.pexels.com and www.pixabay.com.
