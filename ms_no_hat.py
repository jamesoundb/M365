import requests
import re
import csv
from datetime import datetime
import pytz
import time

TIMEZONE = "America/New_York"
ENDPOINTS = {
    "ms_admin_ctr" : "https://status.office365.com/api/feed/mac",
    "pwr_plat_admin_ctr" : "https://status.office365.com/api/feed/ppac",
    "azure_status" : "https://azure.status.microsoft/en-us/status",
    "random_bad_endpoint" : "https://httpstat.us/Random/400-404,500-504"
}

PRINTS = ["***** Microsoft 365 Admin Center: *****",
          "***** Power Platform Admin Center: *****",
          "***** Azure Status: *****",
          "***** Random Bad Endpoint: *****"]

def timestamp(timezone: str) -> str:
    """Takes a timezone parameter and returns a formatted timestamp for month, day, year, hours, and minutes."""
    est = pytz.timezone(timezone)
    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    timestamp = est_now.strftime("%m/%d/%Y %H:%M")

    return timestamp

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
    
def response_check(response=None):
    """Takes an endpoint response parameter and returns True if endpoint status is available."""
    try:
        if response is not None:
            response.raise_for_status()  # Raise an exception for non-successful status codes
            print("\n" + "Status Code:", response.status_code)
            html_content = response.text
   
            if "Available" in html_content:
                print("Status is Available." + "\n")
            else:
                print("Status is Unavailable." + "\n")
        
    except requests.exceptions.RequestException as e:
        error_message = "Error occurred: \n" + str(e)
        print(error_message)
        match = re.search(r":\s*([0-9]+)", error_message)
        if match:
            error_number = match.group(1)
        else:
            print("No number found.")
        
        result = False
        
        print("Response Check Result:", result)
        return result
    

def end_address(endpoint_dict):
    http = []
    for k, v in endpoint_dict.items():
        http.append(v)
    return http


def checks_prints(endpoints, prints):
    http = end_address(endpoints)
    for i, print_item in enumerate(prints):
        print(f"Timestamp:{timestamp(timezone=TIMEZONE)}" + print_item)
        response_check(endpoint((http[i])))


if __name__ == '__main__':
    checks_prints(endpoints=ENDPOINTS, prints=PRINTS)
