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
    
    # Grab all the package records from the "items" key
    items = data["items"] # list of items in data dicitonary

    # only take the top 20 packages (they are already sorted by popularity)
    top20 = items[:20] # list of first 20 items in items list (each object is a dictionary identical to the items list)

    # Build two separate lists — one for names, one for counts.
    # We also need to clean the count: remove the comma and convert to integer.
    # '485,036' -> '485036' -> 485036
    names = [item["formula"] for item in top20] # the name is stored under "formula"
    counts = [int(item["count"].replace(",", "")) for item in top20]

    # --- Draw the bar chart ---
    
    # Create a figure (the canvas) and set its size in inches
    plt.figure(figsize=(14, 7))
    
    # Draw the bars. range(20) gives us positions 0-19 on the x-axis.
    plt.bar(range(20), counts, color="steelblue")
    
    # Label each bar on the x-axis with the package name.
    # rotation=45 tilts the labels so they don't overlap.
    plt.xticks(range(20), names, rotation=45, ha="right")
    
    # Add axis labels and a title
    plt.xlabel("Package Name")
    plt.ylabel("Install Events (last 30 days)")
    plt.title("Top 20 Most Installed Homebrew Packages (Last 30 Days)")
    
    # tight_layout() automatically adjusts spacing so labels don't get cut off
    plt.tight_layout()
    

    # Save the chart as an image file instead of trying to display a window.
    # This works 100% of the time regardless of your OS or display settings.
    print("Chart saved as brew_chart.png")
    plt.savefig("brew_chart.png") # saving the plot as a png is a smarter and more reliable practice
    plt.show()

else:
    # If something went wrong, print the error code so we know what happened.
    print(f"Something went wrong. Status code: {response.status_code}")


