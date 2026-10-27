# AgroFusion 🌱
### AI-Powered Precision Farming Assistant

**Live Website:** https://agrofusion-ai.vercel.app/

AgroFusion is a precision-farming web prototype that helps users explore data-informed crop, nutrient, and irrigation decisions using soil and weather inputs. It combines a responsive web interface with a machine-learning crop-ranking model and rule-based guidance for fertilizer and irrigation.

> **Important:** AgroFusion is a prototype and decision-support aid. Its recommendations are not a substitute for soil testing, local agronomy advice, or validated farm-management practices.

## Features

- **Crop recommendation:** Ranks the top three crop matches using a Random Forest classifier.
- **Soil and field inputs:** Accepts nitrogen (N), phosphorus (P), potassium (K), soil pH, soil type, and crop growth stage.
- **Weather inputs:** Accepts temperature, humidity, rainfall, and soil-moisture values.
- **Current weather lookup:** Can retrieve current conditions through the OpenWeatherMap API when a city and API key are supplied.
- **Fertilizer guidance:** Highlights potential NPK gaps against illustrative prototype targets.
- **Irrigation guidance:** Applies transparent rule-based checks using rainfall, soil moisture, and temperature.
- **Recommendation history:** Stores recent recommendations in a PostgreSQL database and displays recent records.
- **Responsive interface:** Built with HTML, CSS, and JavaScript, with a botanical visual style.

## Live Demo

Visit **https://agrofusion-ai.vercel.app/** to explore the deployed application.

The project is maintained in GitHub and deployed through Vercel. The application code includes a Flask backend, so the deployment must also provide a compatible Python runtime and configured environment variables for backend routes and database access to work. If the live site is served as a static frontend only, API-backed features will require a separately deployed backend or a compatible serverless configuration.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Machine learning | scikit-learn, Random Forest Classifier |
| Data processing | pandas, NumPy |
| Database | PostgreSQL, psycopg |
| Weather integration | OpenWeatherMap API, requests |
| Configuration | python-dotenv |
| Version control | Git, GitHub |
| Deployment | Vercel |

## Project Structure

```text
AgroFusion/
├── app.py                         # Flask application and API routes
├── requirements.txt               # Python dependencies
├── .env                           # Local environment variables (do not commit)
├── agrofusion.db                  # Database file included in the supplied archive
├── data/
│   └── crop_recommendation.csv    # Optional crop recommendation dataset
├── modules/
│   ├── db.py                      # PostgreSQL connection and history operations
│   ├── engine.py                  # Crop model and recommendation logic
│   └── weather.py                 # OpenWeatherMap integration
├── static/
│   ├── css/
│   │   └── style.css              # Interface styling
│   ├── images/
│   │   └── hero-farm.svg           # Local hero illustration
│   └── js/
│       └── app.js                 # Frontend interactions and API calls
├── templates/
│   └── index.html                 # Main web page
└── README.md
```

## How It Works

1. The user enters soil, weather, and field information.
2. The frontend sends the values to the Flask `/api/recommend` endpoint.
3. The recommendation engine uses a Random Forest model to rank likely crops.
4. Prototype rules generate nutrient-gap notes and irrigation guidance.
5. The recommendation is saved to PostgreSQL, and the interface displays the result.
6. The user can optionally fetch current weather or load recent recommendation history.

### Recommendation API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serves the main web page |
| `POST` | `/api/recommend` | Generates crop, fertilizer, and irrigation insights |
| `POST` | `/api/weather` | Retrieves current weather for a city |
| `GET` | `/api/history` | Returns recent saved recommendations |

## Run Locally

### Requirements

- Python 3.10 or later
- pip
- A PostgreSQL database (for example, a Neon PostgreSQL database)
- An OpenWeatherMap API key if you want to use the current-weather lookup

### 1. Clone the repository

```bash
git clone https://github.com/<your-github-username>/<your-repository-name>.git
cd AgroFusion
```

Replace the repository URL and folder name with the actual values for your GitHub repository.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Add your own PostgreSQL connection string:

```env
DATABASE_URL="postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require"
```

Use the connection string supplied by your database provider. Never commit real credentials to GitHub.

### 5. Start the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

> The app initializes its PostgreSQL recommendations table when it starts. A reachable database and a valid `DATABASE_URL` are therefore required for startup.

## Crop Dataset

For dataset-based recommendations, place a crop recommendation CSV at:

```text
data/crop_recommendation.csv
```

The dataset should include these columns:

```text
N, P, K, temperature, humidity, ph, rainfall, label
```

The code also accepts `crop` as the label column if `label` is not present.

If the CSV is missing, the application creates a small synthetic demonstration dataset so the model can run. In that mode, results are for demonstration and interface testing only; they should not be presented as validated agricultural predictions. The displayed score is the model's class probability, not a guarantee of crop success.

## Environment Variables and API Keys

- `DATABASE_URL` — required for PostgreSQL persistence and recommendation history.
- OpenWeatherMap API key — entered in the interface for a weather lookup; it is sent to the backend with the request.

For production, consider moving weather API credentials to server-side environment variables rather than asking users to enter a key, and validate all incoming values on the backend.

## Deployment Notes: GitHub + Vercel

1. Push the project to a GitHub repository.
2. Import the repository into Vercel.
3. Configure the project’s build and runtime settings for the application architecture.
4. Add required environment variables in Vercel Project Settings.
5. Deploy and verify the frontend and each API endpoint.

**Architecture note:** The included code is a Flask application (`app.py`) and does not include a Vercel configuration file in the supplied project archive. A standard static Vercel deployment will not automatically run this Flask server. To use all backend features on the live domain, configure a compatible Python/serverless deployment or host the Flask API separately and point the frontend requests to that API. Confirm the live deployment's runtime and routes before describing the backend as fully deployed.

## Limitations and Responsible Use

- Crop ranking depends on the quality and suitability of the training dataset.
- Fertilizer guidance compares inputs with illustrative NPK targets; it does **not** calculate a safe fertilizer dose.
- Irrigation guidance uses simple prototype rules and is not a calibrated crop-water model.
- Weather lookup returns current conditions, not a forecast.
- Soil type and growth stage are currently contextual inputs; the crop classifier itself uses NPK, temperature, humidity, pH, and rainfall.
- Always verify recommendations with soil tests, local weather information, crop-specific guidance, and a qualified local agronomist before making farm decisions.

## Security Checklist

- Keep `.env`, database credentials, and API secrets out of version control.
- Add `.env` and local virtual-environment folders to `.gitignore`.
- If a real database password or secret has ever been committed or shared in a ZIP, rotate it immediately and update the deployment environment variables.
- Use HTTPS and restrict access to database credentials.
- Do not expose database connection strings in client-side JavaScript or public documentation.

## Future Enhancements

- Add validated, region-specific crop datasets and model evaluation metrics.
- Integrate forecast data and location-aware weather insights.
- Improve irrigation estimates using crop type, soil properties, and crop-water requirements.
- Add user accounts, farm profiles, and exportable recommendation reports.
- Add input validation, monitoring, automated tests, and deployment health checks.
- Configure a production-ready backend architecture for the deployed application.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing the change.

## License

No license file was present in the supplied project archive. Add a `LICENSE` file before publishing the project for reuse, and specify the license you intend to use.

---

**AgroFusion — Grow thoughtfully. Harvest sustainably.**
