import cv2
import pyautogui
import pytesseract
import pygetwindow
import os
import re
from pytesseract import Output
import time
from screeninfo import get_monitors
from PIL import Image

# Set up Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# For example: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# or: pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


def find_textbox(screenshot, text):
    d = pytesseract.image_to_data(screenshot, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        if d['text'][i] == text:
            x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
            return x + w // 2, y + h // 2
    return None


def get_screenshot_all_monitors():
    monitors = get_monitors()
    stitched_screenshot = None

    for monitor in monitors:
        screenshot = pyautogui.screenshot(
            region=(monitor.x, monitor.y, monitor.width, monitor.height))
        if stitched_screenshot is None:
            stitched_screenshot = screenshot
        else:
            stitched_screenshot = Image.new(
                'RGB', (stitched_screenshot.width + screenshot.width, stitched_screenshot.height))
            stitched_screenshot.paste(
                screenshot, (stitched_screenshot.width - screenshot.width, 0))

    return stitched_screenshot


def extract_codes_from_images(directory):
    image_files = [f for f in os.listdir(
        directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    codes = []

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        image = cv2.imread(image_path)
        text = pytesseract.image_to_string(image)

        # Extract codes using a regular expression
        code_regex = r'(\w+-\w+(?:-\w+)*)'
        found_codes = re.findall(code_regex, text)

        codes.extend(found_codes)

    return codes


def main():
   # Extract codes from images in the specified directory
    directory = './images'
    items = extract_codes_from_images(directory)

    # Take a screenshot of all monitors
    screenshot = get_screenshot_all_monitors()

    # Find the textbox by searching for a specific text label
    textbox_label = 'Redeem Code'  # Replace this with the text label you want to find
    textbox_position = find_textbox(screenshot, textbox_label)

    if textbox_position:
        # Click on the textbox
        pyautogui.click(textbox_position)

        # Iterate through the list and paste each item
        for item in items:
            # Type and submit the item
            pyautogui.write(item)
            pyautogui.press('enter')

            # Add delay between pasting items, if necessary
            time.sleep(10)

            pyautogui.click(textbox_position)
            pyautogui.click(textbox_position)

    else:
        print("Textbox not found.")


if __name__ == '__main__':
    main()
