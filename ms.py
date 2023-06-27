import requests
import re
import csv
from sense_hat import SenseHat
from datetime import datetime
import pytz
import time
from graphics import smiley_face, sad_face, red, green, blue, white, yellow, black, heart, checkmark, x, arrow_up, arrow_down, question_mark

sense = SenseHat()
timezone = "America/New_York"

# Endpoints 
ms_admin_ctr = "https://status.office365.com/api/feed/mac"
pwr_plat_admin_ctr = "https://status.office365.com/api/feed/ppac"
azure_status = "https://azure.status.microsoft/en-us/status"
random_bad_endpoint = "https://httpstat.us/Random/400-404,500-504"

def blink_leds() -> None:
    """Flashes the LED matrix for 2 times"""
    # if not on:
    for _ in range(2):  # 2 iterations for approximately 2 seconds
        sense.clear(white)  # Turn on LEDs (white)
        time.sleep(0.5)  # Pause for 0.5 seconds
        sense.clear()  # Turn off LEDs
        time.sleep(0.5)  # Pause for 0.5 seconds

def timestamp(timezone: str) -> str:
    """Takes a timezone parameter and returns a formatted timestamp for month, day, year, hours, and minutes."""
    est = pytz.timezone(timezone)
    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    timestamp = est_now.strftime("%m/%d/%Y %H:%M")

    return timestamp

def led_time(timezone: str) -> str:
    """Takes a timezone parameter and returns a formatted timestamp wih hours and minutes."""
    est = pytz.timezone(timezone)
    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    led_timestamp = est_now.strftime("%H:%M")

    return led_timestamp


def endpoint(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for non-successful status codes
        result = True
    except requests.exceptions.RequestException as e:
        error_message = "Error occurred: " + str(e)
        result = False
    finally:
        return response

def led_timestamp(timestamp, text, background):
    for i in range(len(timestamp)):
        # Set pixels on the LED matrix
        for y in range(8):
            sense.set_pixel(i, y, text)
        
        # Display character on the LED matrix
        sense.set_rotation(180)
        sense.show_letter(timestamp[i], text_colour=text, back_colour=background)
        time.sleep(1)  # Delay to display each character
    
    result = True
    return result


def response_check(response=None):
    try:
        if response is not None:
            response.raise_for_status()  # Raise an exception for non-successful status codes
            # on = True
            # Display smiley face on the LED matrix
            sense.set_rotation(180)
            sense.set_pixels(smiley_face)
            time.sleep(2)
            print("\n" + "Status Code:", response.status_code)
            html_content = response.text
   
            if "Available" in html_content:
                print("Status is Available." + "\n")
                led_timestamp(timestamp=led_time(timezone=timezone), text=blue, background=green)
                sense.set_pixels(smiley_face)
            else:
                print("Status is Unavailable." + "\n")
                led_timestamp(timestamp=led_time(timezone=timezone), text=yellow, background=red)
                sense.set_pixels(sad_face)
    except requests.exceptions.RequestException as e:
        # Display error message on the LED matrix
        error_message = "Error occurred: \n" + str(e)
        print(error_message)
        match = re.search(r":\s*([0-9]+)", error_message)
        if match:
            error_number = match.group(1)
        else:
            print("No number found.")
        sense.set_rotation(180)
        sense.show_message(error_number, text_colour=yellow, back_colour=red, scroll_speed=0.3)
        sense.set_pixels(sad_face)
        result = False
        
        print("Response Check Result:", result)
        return result

def m365_check():
    blink_leds()
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Microsoft 365 Admin Center: *****")
    response_check(endpoint(ms_admin_ctr))
    time.sleep(2)

def pwr_plt_admin():
    blink_leds()
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Power Platform Admin Center: *****")
    response_check(endpoint(pwr_plat_admin_ctr))
    time.sleep(2)

def azure_stat():
    blink_leds()
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Azure Status: *****")
    response_check(endpoint(azure_status))
    time.sleep(2)

def rand_bad_endpoint():
    blink_leds()
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Random Bad Endpoint: *****")
    response_check(endpoint(random_bad_endpoint))
    time.sleep(2)

def graphics():
    sense.set_rotation(180)
    sense.set_pixels(heart)
    time.sleep(5)
    sense.set_rotation(180)
    sense.set_pixels(checkmark)
    time.sleep(5)
    sense.set_rotation(180)
    sense.set_pixels(x)
    time.sleep(5)
    sense.set_rotation(180)
    sense.set_pixels(arrow_up)
    time.sleep(5)
    sense.set_rotation(180)
    sense.set_pixels(arrow_down)
    time.sleep(5)
    sense.set_rotation(180)
    sense.set_pixels(question_mark)

def all_services_check():
    m365_check()
    pwr_plt_admin()
    azure_stat()
    # rand_bad_endpoint()
    
if __name__ == '__main__':
    all_services_check()