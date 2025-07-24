import requests
import os
import json

TMS_API_BASE = os.getenv("TMS_API_BASE", "http://localhost:8000")  # Your FastAPI app base

# External consumer function (calls FastAPI endpoint)
def get_tms_shipments():
    response = requests.get(f"{TMS_API_BASE}/api/tms")
    response.raise_for_status()
    return response.json().get("shipments", [])

# Internal logic (used by FastAPI endpoint handler)
def fetch_tms_shipments():
    with open("mock_data/mock_tms.json") as f:
        raw = json.load(f)
        sgl = raw.get("sgl", {})
        header = sgl.get("header", {})
        parties = sgl.get("parties", {})
        containers = sgl.get("containers", [])
        milestones = sgl.get("milestones", {})

        # Default to one container if none listed in 'containers'
        container_number = "ABCD1234567"
        for event in milestones.get("allEvents", []):
            if event.get("containerNo"):
                container_number = event.get("containerNo")
                break

        return [{
            "fileNo": header.get("fileNo"),
            "customer": {"name": parties.get("customer", {}).get("name")},
            "shipper": {"name": parties.get("shipper", {}).get("name")},
            "containerNumber": container_number,
            "scac": header.get("linerBookingNo", "OOCL"),
            "initialCarrierETA": sgl.get("routing", {}).get("destinationEta")
        }]