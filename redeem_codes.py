# This script reads the codes.txt file and attempts to input them into the application Magic: The Gathering Arena.
import json
import os
import sys
import time
import pyautogui
import pywinauto
import boto3


def countdown(seconds):
    # print out a countdown from the number of seconds passed in to 0
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)


if __name__ == '__main__':
    # use a command line option to determine whether a coordinates.json file should be read instead of performing OCR
    # on the image files
    if len(sys.argv) > 1:
        if sys.argv[1] == '--use-coordinates' or sys.argv[1] == '-u':
            # read the coordinates.json file
            with open('coordinates.json', 'r') as f:
                coordinates = json.load(f)
    else:
        # if the coordinates.json file doesn't exist, perform OCR on the image files
        coordinates = {}

    # create a session
    session = boto3.Session(profile_name='default')

    # create a client
    client = session.client('rekognition')

    # read the text from the codes.txt file line by line into a list
    with open('codes.txt', 'r') as f:
        codes = f.readlines()

    # create a pywinauto application object
    app = pywinauto.Application()

    # check if the application is already running
    try:
        app.connect(title='MTGA')
    except pywinauto.findwindows.ElementNotFoundError:
        # if the application is not running, launch it
        app.start('C:\\Program Files\\Wizards of the Coast\\MTGA\\MTGALauncher\\MTGALauncher.exe')
        # wait for the application to launch, and print out the time countdown
        for i in range(60, 0, -1):
            print(i)
            # if the count is a multiple of 10, try and connect to the application, and if it is successful,
            # break out of the loop
            if i % 10 == 0:
                try:
                    app.connect(title='MTGA')
                    # wait for an additional 15 seconds to allow the application to fully launch
                    print('waiting 15 seconds...')
                    countdown(15)
                    break
                except pywinauto.findwindows.ElementNotFoundError:
                    pass
            time.sleep(1)

    # bring the application into focus
    app.window(title='MTGA').set_focus()

    # take a screenshot of the application
    pyautogui.screenshot('screenshot.png')

    # determine the size of the application window
    window_size = pyautogui.size()
    print(window_size)

    # get the width and height of the application window
    if coordinates.get('window_size'):
        window_width = coordinates['window_size'][0]
        window_height = coordinates['window_size'][1]
    else:
        window_width = window_size[0]
        window_height = window_size[1]
        coordinates['window_size'] = [window_width, window_height]

    # use amazon rekognition to identify the location of the store button
    with open('screenshot.png', 'rb') as image:
        image_bytes = image.read()
        response = client.detect_text(Image={'Bytes': image_bytes})
        for item in response['TextDetections']:
            if item['Type'] == 'LINE' and item['DetectedText'] == 'Store':
                print(item['Geometry']['BoundingBox'])
                break
        # store the coordinates of the store button
        store_button_x = item['Geometry']['BoundingBox']['Left'] * window_width
        store_button_y = item['Geometry']['BoundingBox']['Top'] * window_height
        coordinates['store_button'] = [store_button_x, store_button_y]

    # long click the store button
    pyautogui.mouseDown(store_button_x, store_button_y)
    time.sleep(1)
    pyautogui.mouseUp(store_button_x, store_button_y)

    # wait for the store window to appear, countdown ten seconds
    countdown(8)

    if coordinates.get('redeem_code_textbox'):
        redeem_code_textbox_x = coordinates['redeem_code_textbox'][0]
        redeem_code_textbox_y = coordinates['redeem_code_textbox'][1]
    else:
        # take a screenshot of the store window
        pyautogui.screenshot('screenshot.png')

        # use amazon rekognition to identify the location of the redeem code textbox
        with open('screenshot.png', 'rb') as image:
            image_bytes = image.read()
            response = client.detect_text(Image={'Bytes': image_bytes})
            for item in response['TextDetections']:
                if item['Type'] == 'LINE' and item['DetectedText'] == 'Redeem Code':
                    print(item['Geometry']['BoundingBox'])
                    break
            # store the coordinates of the redeem code textbox
            redeem_code_textbox_x = item['Geometry']['BoundingBox']['Left'] * window_width
            redeem_code_textbox_y = item['Geometry']['BoundingBox']['Top'] * window_height
            coordinates['redeem_code_textbox'] = [redeem_code_textbox_x, redeem_code_textbox_y]

    # loop through the codes
    for code in codes:
        print(code)
        # click the center of the 'Redeem Code' textbox
        pyautogui.doubleClick(redeem_code_textbox_x, redeem_code_textbox_y)

        # clear the textbox
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')

        # input the code
        pyautogui.write(code)

        # hit enter to submit the code
        pyautogui.press('enter')

        # wait for the 'OK' button to appear
        time.sleep(3)

        if coordinates.get('ok_button'):
            ok_button_x = coordinates['ok_button'][0]
            ok_button_y = coordinates['ok_button'][1]
        else:
            # take a screenshot of the application
            pyautogui.screenshot('screenshot.png')

            # use amazon rekognition to identify the location of the 'OK' button
            with open('screenshot.png', 'rb') as image:
                image_bytes = image.read()
                response = client.detect_text(Image={'Bytes': image_bytes})
                for item in response['TextDetections']:
                    if item['Type'] == 'LINE' and item['DetectedText'] == 'OK':
                        print(item['Geometry']['BoundingBox'])
                        break
                # store the coordinates of the 'OK' button
                ok_button_x = item['Geometry']['BoundingBox']['Left'] * window_width
                ok_button_y = item['Geometry']['BoundingBox']['Top'] * window_height
                coordinates['ok_button'] = [ok_button_x, ok_button_y]

        # long click the center of the 'OK' button
        pyautogui.mouseDown(ok_button_x, ok_button_y)
        time.sleep(1)
        pyautogui.mouseUp(ok_button_x, ok_button_y)

        # wait for the 'Claim Prize' button to appear
        time.sleep(1)
        if coordinates.get('claim_prize_button'):
            claim_prize_button_x = coordinates['claim_prize_button'][0]
            claim_prize_button_y = coordinates['claim_prize_button'][1]
        else:
            # take a screenshot of the application
            pyautogui.screenshot('screenshot.png')

            # use amazon rekognition to identify the location of the 'Claim Prize' button
            with open('screenshot.png', 'rb') as image:
                image_bytes = image.read()
                response = client.detect_text(Image={'Bytes': image_bytes})
                for item in response['TextDetections']:
                    if item['Type'] == 'LINE' and item['DetectedText'] == 'Claim Prize':
                        print(item['Geometry']['BoundingBox'])
                        break
                # store the coordinates of the 'Claim Prize' button
                claim_prize_button_x = item['Geometry']['BoundingBox']['Left'] * window_width
                claim_prize_button_y = item['Geometry']['BoundingBox']['Top'] * window_height
                coordinates['claim_prize_button'] = [claim_prize_button_x, claim_prize_button_y]

        # long click the center of the 'Claim Prize' button
        pyautogui.mouseDown(claim_prize_button_x, claim_prize_button_y)
        time.sleep(1)
        pyautogui.mouseUp(claim_prize_button_x, claim_prize_button_y)

        # wait for the 'Redeem Code' textbox to appear
        countdown(2)

    # save coordinates to a file in json format
    with open('coordinates.json', 'w') as f:
        json.dump(coordinates, f)

    # delete the screenshot
    os.remove('screenshot.png')

    # ask user if they want to close the application, if yes do it, if not exit the program. sanitize the input
    close = input('Do you want to close the application? (y/n): ')
    while close.lower() != 'y' and close != 'n':
        close = input('Do you want to close the application? (y/n): ')
        if close == 'y':
            app.kill()
        else:
            sys.exit()
