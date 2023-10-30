import json
import requests
from datetime import datetime

# URL of the JSON data
url = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList?inactive=true"

# Function to convert Unix timestamp to human-readable format
def unix_timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%B %d, %Y, %H:%M:%S UTC')

# start here
if __name__=="__main__":

    # Fetch JSON data from the URL
    response = requests.get(url)
    data = response.json()

    # Extract widlfire information
    widlfire_data = data["features"][:10]  # Display only the top 10 widlfires

    # Read website template
    template_file = open("site-template.html", "r")
    html_content = template_file.read()
    widlfireDataContent = ""

    for i, widlfire in enumerate(widlfire_data, 1):
        name = widlfire["properties"]["Name"]
        location = widlfire["properties"]["County"]
        starttime = widlfire["properties"]["Started"]
        starttime = widlfire["properties"]["Started"]
        isactive = widlfire["properties"]["IsActive"]
        
        container_class = "container"
        if i % 2 == 0:
            container_class += " alternate"
        
        widlfireDataContent += f"""
        <div class="{container_class}">
            <p><strong>Wildfire {i}:</strong><br>
            - Name: {name}<br>
            - Location: {location}<br>
            - Started: {starttime}<br>
            - IsActive: {isactive}</p><br>
        </div>
        """

    html_content = html_content.replace("pythonGeneratedContent", widlfireDataContent)

    # Write HTML content to a file
    with open("wildfire.html", "w") as html_file:
        html_file.write(html_content)

    print("Wildfire html generated!")
