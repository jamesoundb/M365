import requests
import re
import csv
from datetime import datetime
import pytz
import time

timezone = "America/New_York"

# Endpoints 
ms_admin_ctr = "https://status.office365.com/api/feed/mac"
pwr_plat_admin_ctr = "https://status.office365.com/api/feed/ppac"
azure_status = "https://azure.status.microsoft/en-us/status"
random_bad_endpoint = "https://httpstat.us/Random/400-404,500-504"

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
        # Display error message on the LED matrix
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
    
def m365_check():
    """Executes the health check for Microsoft 365 Admin Center."""
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Microsoft 365 Admin Center: *****")
    response_check(endpoint(ms_admin_ctr))

def pwr_plt_admin():
    """Executes the health check for Power Platform Admin Center."""
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Power Platform Admin Center: *****")
    response_check(endpoint(pwr_plat_admin_ctr))

def azure_stat():
    """Executes the health check for Azure Status."""
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Azure Status: *****")
    response_check(endpoint(azure_status))

def rand_bad_endpoint():
    """Executes the health check for Random Bad Endpoint."""
    print(f"Timestamp:{timestamp(timezone=timezone)} ***** Random Bad Endpoint: *****")
    response_check(endpoint(random_bad_endpoint))

def all_services_check():
    """Executes all service check functions"""
    m365_check()
    pwr_plt_admin()
    azure_stat()
    # rand_bad_endpoint()
    
if __name__ == '__main__':
    all_services_check()