import requests
import re
import csv
from sense_hat import SenseHat
from datetime import datetime
import pytz
import time
from graphics import smiley_face, sad_face, red, green, blue, white, yellow, black, heart, checkmark, x, arrow_up, arrow_down, question_mark

sense = SenseHat()

TIMEZONE = "America/New_York"
ENDPOINTS = {
    "ms_admin_ctr" : "https://status.office365.com/api/feed/mac",
    "pwr_plat_admin_ctr" : "https://status.office365.com/api/feed/ppac",
    "azure_status" : "https://azure.status.microsoft/en-us/status"
    # "random_bad_endpoint" : "https://httpstat.us/Random/400-404,500-504"
}

PRINTS = ["***** Microsoft 365 Admin Center: *****",
          "***** Power Platform Admin Center: *****",
          "***** Azure Status: *****"]
        #   "***** Random Bad Endpoint: *****"]

def blink_leds() -> None:
    """Flashes the LED matrix 2 times"""
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
    """Takes a timezone parameter and returns a formatted timestamp with hours and minutes."""
    est = pytz.timezone(timezone)
    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    led_timestamp = est_now.strftime("%H:%M")

    return led_timestamp


def endpoint(endpoint: str) -> requests.models.Response:
    """Takes an endpoint string parameter (ex:https://status.office365.com/api/feed/mac) and returns the response code."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for non-successful status codes
        result = True
    except requests.exceptions.RequestException as e:
        error_message = "Error occurred: " + str(e)
        result = False
    finally:
        return response

def led_timestamp(timestamp: str, text: tuple, background: tuple):
    """Takes timestamp format ('%H:%M'), text color, and background color parameters then displays the time to the LED matrix."""
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
    """Takes an endpoint response parameter and returns True if endpoint status is available."""
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
                led_timestamp(timestamp=led_time(timezone=TIMEZONE), text=blue, background=green)
                sense.set_pixels(smiley_face)
                result = True
            else:
                print("Status is Unavailable." + "\n")
                led_timestamp(timestamp=led_time(timezone=TIMEZONE), text=yellow, background=red)
                sense.set_pixels(sad_face)
                result = False
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


def graphics():
    """Executes all graphics patterns from graphics module."""
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


def end_address(endpoint_dict):
    http = []
    for k, v in endpoint_dict.items():
        http.append(v)
    return http


def checks_prints(endpoints, prints):
    http = end_address(endpoints)
    for i, print_item in enumerate(prints):
        blink_leds()
        print(f"Timestamp:{timestamp(timezone=TIMEZONE)}" + print_item)
        response_check(endpoint((http[i])))
        time.sleep(2)


if __name__ == '__main__':
    checks_prints(endpoints=ENDPOINTS, prints=PRINTS)