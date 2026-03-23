# We're importing the 'requests' library — this is what lets us
# make HTTP requests (basically, visit URLs) from Python.
import requests
import matplotlib.pyplot as plt

# This is the URL of the Homebrew Analytics API.
# It returns the install data for the last 30 days in JSON format.
URL = "https://formulae.brew.sh/api/analytics/install/30d.json"

# This line actually sends the request to the URL and stores the response.
# Think of 'response' as the envelope that came back from the vending machine —
# it contains the data, plus some info about whether the request succeeded.
response = requests.get(URL)

# Before we trust the data, we should check if the request actually worked.
# Status code 200 means "success" in web language.
# (You've probably seen 404 before — that means "not found". Same idea.)
if response.status_code == 200:
    print("Success! Data received.")
    
    # .json() converts the raw text response into a Python dictionary —
    # a data structure Python can actually work with.
    data = response.json()
    
    # Let's see what keys (sections) are at the top level of this data.
    # This is like opening the envelope and checking what's inside before reading it.
    print("Top-level keys in the data:", data.keys())
    
    # Now let's look at just the first record so we know what one entry looks like.
    # The actual install records live inside data["items"]
    first_item = data["items"][0]
    print("\nHere's what one record looks like:")
    print(first_item)
    
    # And let's see how many total records there are
    print(f"\nTotal number of packages in this dataset: {len(data['items'])}")

else:
    # If something went wrong, print the error code so we know what happened.
    print(f"Something went wrong. Status code: {response.status_code}")


