from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.utils.get_tms import get_tms_shipments, fetch_tms_shipments
from src.utils.get_windward import get_windward_data, fetch_windward_data
from src.utils.get_weather import get_weather_data
import pandas as pd
import os
from transformers import pipeline

app = FastAPI()

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


@app.get("/api/tms")
def api_tms():
    return {"shipments": fetch_tms_shipments()}


@app.get("/api/windward/{container_number}")
def api_windward(container_number: str):
    return fetch_windward_data(container_number)


def is_weather_related(text):
    if not text:
        return False
    result = classifier(text, candidate_labels=["weather-related", "not weather-related"])
    return result["labels"][0] == "weather-related" and result["scores"][0] >= 0.8


def process_shipment(shipment):
    file_no = shipment.get("fileNo")
    customer_name = shipment.get("customer", {}).get("name")
    shipper_name = shipment.get("shipper", {}).get("name")
    container_number = shipment.get("containerNumber")
    eta = shipment.get("initialCarrierETA")

    windward_data = get_windward_data(container_number)
    actual_arrival = windward_data.get("actualArrivalAt")
    delay_reasons_list = windward_data.get("delay", {}).get("reasons", [])
    delay_reasons = "; ".join(
        r.get("delayReasonDescription", "") for r in delay_reasons_list
    )
    location = windward_data.get("location", {})
    scac = windward_data.get("scac")

    weather_data = {"temperature": None, "wind": None}
    if delay_reasons and is_weather_related(delay_reasons):
        lat = location.get("lat", 0)
        lon = location.get("lon", 0)
        timestamp = actual_arrival[:13] + ":00" if actual_arrival else ""
        weather_data = get_weather_data(lat, lon, timestamp)

    return {
        "fileNo": file_no,
        "customer.name": customer_name,
        "shipper.name": shipper_name,
        "containerNumber": container_number,
        "scac": scac,
        "initialCarrierETA": eta,
        "actualArrivalAt": actual_arrival,
        "delay.reasons": delay_reasons,
        "temperature": weather_data["temperature"],
        "wind": weather_data["wind"]
    }


@app.get("/")
def root():
    return {"message": "Shipment Report Automation API"}


@app.get("/generate-report")
def generate_report():
    shipments = get_tms_shipments()
    report_rows = []

    for shipment in shipments:
        shipment_information = process_shipment(shipment)
        report_rows.append(shipment_information)

    df = pd.DataFrame(report_rows)
    output_path = "output/shipment_report.csv"
    os.makedirs("../output", exist_ok=True)
    df.to_csv(output_path, index=False)

    return FileResponse(output_path, media_type="text/csv", filename="shipment_report.csv")
