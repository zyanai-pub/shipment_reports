# 📦 Shipment Report Automation API

This is a FastAPI-based project for generating enriched shipment reports using data from TMS, Windward, and weather services. It includes an AI model to detect whether a shipment delay is weather-related.

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Install dependencies

Make sure you have **Python 3.8+** installed.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can install dependencies manually:

```bash
pip install fastapi uvicorn transformers pandas
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

> Replace `main` with the name of your Python file (e.g. `app.py`, `server.py`) if it's different.

### 4. Open in Browser

- API Root: [http://localhost:8000](http://localhost:8000)
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root welcome message |
| `/api/tms` | GET | Fetch TMS shipment data |
| `/api/windward/{container_number}` | GET | Get tracking data for a specific container |
| `/generate-report` | GET | Generate and download a CSV shipment report |

---

## 📂 Output

The generated shipment report will be saved as:

```
output/shipment_report.csv
```

Make sure the `output/` folder exists or will be created by the app.

---

## 🧠 Model Used

This project uses the Hugging Face `facebook/bart-large-mnli` model for zero-shot classification to identify weather-related delay reasons.

---

## 📄 License

This project is for internal or educational use only. Add a license section if needed.
