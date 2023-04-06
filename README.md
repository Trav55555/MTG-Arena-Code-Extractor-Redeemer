# Textbox OCR

This script is designed to perform OCR on a series of images, extract codes from the recognized text, and paste the codes into a specified textbox in an application window.

## Requirements

- Python 3.6 or later
- OpenCV
- Tesseract OCR
- pytesseract
- PyGetWindow
- PyAutoGUI
- screeninfo

Install the required Python packages using:

pip install opencv-python pytesseract pygetwindow pyautogui screeninfo

Make sure to [install Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) on your system as well.

## Usage

Replace <path_to_tesseract_executable> in the script with the correct path to the Tesseract executable on your system. Replace <path_to_your_image_directory> with the path to the directory containing your image files.

To run the script, use the following command:

python textbox_ocr.py "Your Application Window Title" "Your Text Label"

The script will focus the specified application window, locate the textbox with the given label, and paste the extracted codes into the textbox one by one.
