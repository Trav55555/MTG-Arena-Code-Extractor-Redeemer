import sys
import cv2
import pytesseract
from PIL import Image
from pathlib import Path
import pyautogui
import screeninfo
import pygetwindow as gw
import re
import time
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')
# Get Tesseract path and image folder path from the configuration file
tesseract_path = config.get('paths', 'tesseract')
image_folder = config.get('paths', 'image_folder')

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Function to bring the specified application window into focus
def focus_application_window(window_title):
    try:
        # Get the window with the given title
        app_window = gw.getWindowsWithTitle(window_title)[0]
        # Check if the window is active, if not, activate and maximize it
        if not app_window.isActive:
            app_window.activate()
            app_window.maximize()
        return True
    except IndexError:
        # Return False if the window is not found
        return False

# Function to perform OCR on an image and return the extracted text
def ocr_image_to_text(image_path):
    # Read the image using OpenCV
    img = cv2.imread(str(image_path))
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(gray)
    return text

# Function to extract codes from text using regular expressions
def extract_codes_from_text(text):
    # Find all codes in the text that match the regex pattern
    codes = re.findall(r'\b(?:[A-Za-z0-9]+-)+[A-Za-z0-9]+\b', text)
    return codes

def main():
    # Check if the required command-line arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python textbox_ocr.py <window_title> <textbox_label>")
        sys.exit(1)

    # Get the window title and textbox label from the command-line arguments
    window_title = sys.argv[1]
    textbox_label = sys.argv[2]

    # Focus the specified application window
    if not focus_application_window(window_title):
        print(f"Application window '{window_title}' not found.")
        return

    # Set the directory containing image files
    directory = image_folder
    # Find all image files in the directory with the specified extensions
    image_files = list(Path(directory).glob('*.jpg')) + list(Path(directory).glob('*.png')) + list(Path(directory).glob('*.jpeg'))

    # Perform OCR on the image files and extract codes
    codes = []
    for image_file in image_files:
        text = ocr_image_to_text(image_file)
        codes.extend(extract_codes_from_text(text))

    # Capture a screenshot of the primary monitor
    monitor = screeninfo.get_monitors()[0]
    screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))

    # Locate the textbox on the screen using the given label
    textbox_location = pyautogui.locateCenterOnScreen(textbox_label, confidence=0.7, grayscale=True)

    # Click on the textbox and paste the extracted codes
    if textbox_location:
        pyautogui.click(textbox_location)
        for code in codes:
            pyautogui.write(code)
            pyautogui.press('enter')
            time.sleep(5)
            pyautogui.doubleClick(textbox_location)
    else:
        print(f"Textbox with label '{textbox_label}' not found on screen.")
        