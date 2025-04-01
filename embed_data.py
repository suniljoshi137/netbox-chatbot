#!/usr/bin/env python3

import json
import requests
from sentence_transformers import SentenceTransformer


NETBOX_URL = "YOUR_NETBOX_URL"
API_KEY = "ADMIN_API_KEY"

headers = {
    "Authorization": f"Token {API_KEY}"
}


netbox_url = "NETBOX_URL/api/dcim/devices/"

def get_netbox_devices():

    devices = []  # List to hold all devices
    url = netbox_url
    while url:
        # Send GET request to fetch devices
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            data = response.json()
            devices.extend(data['results'])  # Add the current page of devices to the list
            url = data.get('next')  # Get the URL for the next page, if it exists

        else:
            print(f"Failed to retrieve devices: {response.status_code}")
            break

    return devices


device_data = get_netbox_devices()
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

for device in device_data:
    # Extract necessary fields and ensure they are strings
    text_representation = " ".join([
        str(device.get("name", "Unknown")),
        str(device.get("device_type", {}).get("display", "Unknown")),
        str(device.get("device_type", {}).get("manufacturer", {}).get("display", "Unknown")),
        str(device.get("device_role", {}).get("display", "Unknown")),
        str(device.get("serial", "Unknown")),
        str(device.get("site", {}).get("display", "Unknown")),
        str(device.get("location", {}).get("display", "Unknown")),
        str(device.get("rack", {}).get("display", "Unknown")),
        str(device.get("status", {}).get("label", "Unknown")),
        str(device.get("comments", ""))
    ])

    print(f"Encoding text: {text_representation}")

    try:
        device["embedding"] = model.encode(text_representation).tolist()
    except Exception as e:
        print(f"Error encoding text: {text_representation}")
        print(f"Exception: {e}")
        device["embedding"] = []

with open("device_embeddings.json", "w") as f:
    json.dump(device_data, f, indent=4)

print("Embeddings generated and saved.")
