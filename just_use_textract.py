# this script is used to detect sequences of letters and numbers in an image separated by '-', using the AWS
# Rekognition API. The script is used to extract codes from pictures of trading cards. the script generates a list of
# the codes it detects and stores them in a text file.
import re
from pathlib import Path
import boto3
import sys


def ocr_image_to_text(image_file):
    text = ''

    # if the image-text directory doesn't exist, create it
    if not Path('image-text').exists():
        Path('image-text').mkdir()

    # create a session
    session = boto3.Session(profile_name='default')

    # Create a Rekognition client
    client = session.client('textract')

    #  if there is a file in the image-text directory with the same name as the image file, read the text from the file
    #  instead of performing OCR on the image file
    if Path(f'image-text/{image_file.stem}.txt').exists():
        with open(f'image-text/{image_file.stem}.txt', 'r') as f:
            text = f.read()
    else:
        # Read the image file
        with open(image_file, 'rb') as image:
            image_bytes = image.read()

        # Perform OCR on the image
        response = client.detect_document_text(Document={'Bytes': image_bytes})

        # Extract the text from the response
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text += item["Text"]

    # save the text to a file labeled with the image file name and the .txt extension to a directory named image-text,
    # which will be created if it doesn't exist
    with open(f'image-text/{image_file.stem}.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    return text


def extract_codes_from_text(text):
    # code type 1 starts and ends with 5 characters, and contains 4 '-' characters. the following regex will find all
    # codes of type 1 in the text
    pattern = r'(?:\w{5}[-]\w{5}[-]\w{5}[-]\w{5}[-]\w{5})'

    # code type 2 starts and ends with 3 characters, and contains only 2 '-' characters. the following regex
    # will find all codes of type 2 in the text
    pattern2 = r'(?:\w{3}[-]\w{4}[-]\w{3})'

    codes = re.findall(pattern, text)
    codes.extend(re.findall(pattern2, text))
    return codes


if __name__ == '__main__':
    codes = []
    # Check if the required command-line arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python just_use_textract.py <image_folder>")
        sys.exit(1)

    # Get the image folder from the command-line argument and iterate through the files
    image_folder = sys.argv[1]
    image_files = [file for file in Path(image_folder).iterdir() if file.suffix in ['.jpg', '.png', '.jpeg']]

    # Perform OCR on the image file and extract codes
    for file in image_files:
        print(f'working on {file}...')
        text = ocr_image_to_text(file)
        code = extract_codes_from_text(text)
        codes.append(code)

    with open('codes.txt', 'w', encoding='utf-8') as f:
        for code in codes:
            print(code[0])
            f.write(code[0] + '\n')
