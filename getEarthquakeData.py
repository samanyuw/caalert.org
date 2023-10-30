import json
import requests
from datetime import datetime

# URL of the JSON data
# url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"

# Function to convert Unix timestamp to human-readable format
def unix_timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%B %d, %Y, %H:%M:%S UTC')

# start here
if __name__=="__main__":

    # Fetch JSON data from the URL
    response = requests.get(url)
    data = response.json()

    # Extract earthquake information
    earthquake_data = data["features"][:100]  # Display only the top 10 earthquakes
       
    # Read website template
    template_file = open("site-template.html", "r")
    html_content = template_file.read()
    earthquakeDataContent = ""
    count = 0

    for i, earthquake in enumerate(earthquake_data, 1):
        magnitude = earthquake["properties"]["mag"]
        location = earthquake["properties"]["place"]
        timestamp = earthquake["properties"]["time"]
        time_readable = unix_timestamp_to_datetime(timestamp)


        ca_data_only = location.split(",")[-1].lstrip().rstrip()
        print(ca_data_only)
        
        if (ca_data_only == "CA"):
            container_class = "container"
            if count % 2 == 0:
                container_class += " alternate"
            if magnitude >= 5:
                container_class += " red-bg"
            
            earthquakeDataContent += f"""
            <div class="{container_class}">
                <p><strong>Earthquake {count+1}:</strong><br>
                - Magnitude: {magnitude}<br>
                - Location: {location}<br>
                - Time: {time_readable}</p><br>
            </div>
            """
            count = count + 1
            if (count == 20):
                break


    print (count)
    html_content = html_content.replace("pythonGeneratedContent", earthquakeDataContent)

    # Write HTML content to a file
    with open("index.html", "w") as html_file:
        html_file.write(html_content)

    print("Earthquake html generated!")
