import requests
import os
import json

WINDWARD_API_BASE = os.getenv("WINDWARD_API_BASE", "http://localhost:8000")


# External consumer function (calls FastAPI endpoint)
def get_windward_data(container_number):
    response = requests.get(f"{WINDWARD_API_BASE}/api/windward/{container_number}")
    if response.status_code == 200:
        return response.json()
    return {}


# Internal logic (used by FastAPI endpoint handler)
def fetch_windward_data(container_number):
    with open("mock_data/mock_windward.json") as f:
        data = json.load(f)
        tracked = data.get("trackedShipments", {}).get("data", [])
        for item in tracked:
            shipment = item.get("shipment", {})
            if shipment.get("containerNumber") == container_number:
                return {
                    "actualArrivalAt": shipment.get("status", {}).get("actualArrivalAt"),
                    "delay": shipment.get("status", {}).get("delay"),
                    "scac": shipment.get("scac"),
                    "location": {
                        "lat": 55.6761,  # example for Copenhagen
                        "lon": 12.5683
                    }
                }
        return {}
