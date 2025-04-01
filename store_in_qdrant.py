#!/usr/bin/env python3

import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Load Qdrant client
client = QdrantClient("localhost", port=6333)  # Ensure Qdrant is running

# Create a collection if not exists
collection_name = "netbox_devices"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Load embeddings
with open("device_embeddings.json", "r") as f:
    device_data = json.load(f)

# Insert data into Qdrant
points = []
for device in device_data:
    points.append(PointStruct(
        id=device["id"],  # Unique identifier
        vector=device["embedding"],  # Store the vector embedding
        payload={
            "name": device.get("name", "Unknown"),
            "device_type": device.get("device_type", {}).get("display", "Unknown"),
            "manufacturer": device.get("device_type", {}).get("manufacturer", {}).get("display", "Unknown"),
            "device_role": device.get("device_role", {}).get("display", "Unknown"),
            "serial": device.get("serial", "Unknown"),
            "site": device.get("site", {}).get("display", "Unknown"),
            "location": device.get("location", {}).get("display", "Unknown"),
            "rack": device.get("rack", {}).get("display", "Unknown"),
            "status": device.get("status", {}).get("label", "Unknown"),
            "comments": device.get("comments", ""),
        }
    ))

client.upsert(collection_name=collection_name, points=points)

print("Data stored in Qdrant.")

