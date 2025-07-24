# 🚢 Shipment Report Automation API

A FastAPI-based solution for automating freight reporting using logistics, tracking, and weather APIs. It enriches data with AI-driven insights using HuggingFace's `facebook/bart-large-mnli` model to detect whether shipment delays are related to weather.

---

## 📦 Features

- 🔗 Integrates with:
  - Logistics TMS API
  - Windward Tracking API
  - Open-Meteo Weather API
- 🧠 Uses zero-shot classification to detect weather-related delay reasons
- 📄 Exports data to a downloadable CSV
- ⚡ Runs as a FastAPI web server

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/shipment-report-automation.git
cd shipment-report-automation
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, you can generate one with:

```txt
fastapi
uvicorn
pandas
transformers
torch
requests
python-dotenv
```

### 4. Set environment variables

Create a `.env` file in the project root:

```env
TMS_API_BASE=https://your-tms-api.com
WINDWARD_API_BASE=https://your-windward-api.com
```

---

## 🚀 Running the App

### Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### Access API Docs:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📥 API Endpoint

### `GET /generate-report`

- Triggers report generation
- Returns a downloadable CSV file

### CSV Output Fields:

| Field             | Description                            |
| ----------------- | -------------------------------------- |
| fileNo            | Internal file number                   |
| customer.name     | Customer name                          |
| shipper.name      | Shipper name                           |
| containerNumber   | Container ID                           |
| scac              | Carrier code                           |
| initialCarrierETA | Estimated time of arrival              |
| actualArrivalAt   | Actual arrival time                    |
| delay.reasons     | Reason for shipment delay              |
| temperature       | Temperature at delay location (if any) |
| wind              | Wind speed at delay location (if any)  |

---

## 🧠 AI Classifier

We use HuggingFace's `facebook/bart-large-mnli` model to detect whether delay reasons are weather-related:

- `True` → triggers a weather API call
- `False` → weather fields are left `None`

Example:

```python
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
res = classifier("Delayed due to high winds", ["weather-related", "not weather-related"])
```

---

## 🐳 Docker (Optional)

### Dockerfile

```Dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run:

```bash
docker build -t shipment-api .
docker run -p 8000:8000 shipment-api
```

---

## 📬 Contact & Support

Feel free to reach out at [your.email\@example.com] if you have questions or want to contribute.

---

## 📄 License

MIT © 2025 Your Name

