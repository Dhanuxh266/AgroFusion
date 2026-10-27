# AgroFusion — Precision Farming Web Prototype

A Flask web application with an editorial, botanical visual direction inspired by the supplied reference: soft white `#E8E9DF`, sage green `#A9B887`, deep olive `#2E3D28`, spacious layouts, and clean modern typography.

## Features
- Responsive HTML/CSS/JavaScript frontend (no Streamlit)
- Flask endpoints for crop, fertilizer and irrigation recommendations
- Random Forest crop ranking (top 3)
- Soil and weather inputs, soil type and growth stage fields
- Optional current weather lookup through OpenWeatherMap
- SQLite recommendation history
- Reuses the supplied `agrofusion.db` database and compatible `recommendations` table
- Local botanical SVG illustration, so the hero artwork does not depend on an external image host

## Run on Windows / VS Code
1. Extract the ZIP.
2. Open the extracted `agrofusion_web` folder in VS Code.
3. In the terminal, run:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

4. Open `http://127.0.0.1:5000` in your browser.

## Dataset
For a dataset-backed model, place the Kaggle Crop Recommendation Dataset at `data/crop_recommendation.csv`. Expected columns: `N, P, K, temperature, humidity, ph, rainfall, label`.

If the CSV is absent, a small synthetic demo dataset is generated so the application can start. The demo model is for interface testing only; it must not be presented as measured real-world model accuracy. The displayed score is the model's class probability, not a guarantee of crop success.

## Notes
- The fertilizer logic compares inputs with simple illustrative NPK targets. It does not calculate a safe application dose. Use a soil test and local agronomist recommendations for real farms.
- Irrigation logic is a simple demonstration rule set, not a calibrated crop water model.
- The optional weather endpoint reads current weather, not a forecast.
- `agrofusion.db` is included from the uploaded archive. Back it up before using the project for new data.
