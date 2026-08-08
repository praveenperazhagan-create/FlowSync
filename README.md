# FlowSync 🚦

**AI-Powered Traffic Analysis and Smart Mobility Platform**

FlowSync is a full-stack traffic intelligence platform designed to analyze traffic data, predict traffic conditions, provide analytics, and present actionable information through a modern web dashboard.

The project combines:

- A **Next.js / TypeScript frontend**
- A **Python backend**
- An **AI/ML traffic prediction pipeline**
- A **data-cleaning and preprocessing pipeline**
- Traffic analytics and visualization
- Emergency and traffic-related dashboard features

> **Note:** The trained ML model file is intentionally not stored in this repository because it exceeds GitHub's 100 MB individual file limit.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Project Structure](#-project-structure)
5. [Technology Stack](#-technology-stack)
6. [Frontend](#-frontend)
7. [Backend](#-backend)
8. [AI and Machine Learning](#-ai-and-machine-learning)
9. [Data Cleaning Pipeline](#-data-cleaning-pipeline)
10. [Traffic Dataset](#-traffic-dataset)
11. [Installation](#-installation)
12. [Running the Project](#-running-the-project)
13. [Environment Variables](#-environment-variables)
14. [API Integration](#-api-integration)
15. [Data Processing Workflow](#-data-processing-workflow)
16. [Model File](#-model-file)
17. [Git and GitHub](#-git-and-github)
18. [Troubleshooting](#-troubleshooting)
19. [Future Improvements](#-future-improvements)
20. [Contributors](#-contributors)
21. [License](#-license)

---

# 🚦 Project Overview

Traffic congestion is affected by many variables such as vehicle volume, road conditions, weather, time of day, road infrastructure, nearby events, incidents, and public transportation.

FlowSync provides a centralized platform for processing these traffic-related variables and presenting the results through a user-friendly interface.

The platform is intended to support:

- Traffic monitoring
- Traffic condition analysis
- AI-assisted traffic prediction
- Historical traffic analysis
- Analytics dashboards
- Emergency-related information
- Dataset upload and processing
- Traffic trend visualization

The application follows a full-stack architecture where the frontend communicates with the backend API, while the backend handles data processing, AI/ML operations, and traffic analysis.

---

# ✨ Key Features

## 🖥️ Modern Web Dashboard

The frontend provides a responsive dashboard for interacting with the traffic analysis system.

Main pages include:

- Home
- Dashboard
- Analytics
- History
- Emergency
- Settings
- About
- Login
- Registration
- Forgot Password

---

## 📊 Traffic Analytics

The analytics section is designed to help users understand traffic patterns using:

- Traffic metrics
- Charts
- Historical information
- Traffic trends
- Prediction results
- Data summaries

---

## 🤖 AI-Based Traffic Analysis

The backend includes an AI/ML pipeline for traffic analysis.

The system can use traffic-related features such as:

- Traffic volume
- Average speed
- Travel time index
- Road characteristics
- Number of lanes
- Weather information
- Temperature
- Humidity
- Visibility
- Air quality
- Pedestrian count
- Heavy vehicle percentage
- Incidents
- Road closures
- Events
- Public transportation proximity
- School zones
- Construction zones
- Peak-hour indicators
- Weekend indicators
- Public holiday indicators

---

## 🧹 Automated Data Cleaning

FlowSync includes a dedicated data-cleaning program.

The pipeline performs:

- Dataset loading
- CSV/XLS/XLSX support
- Duplicate detection
- Duplicate removal
- Column-name standardization
- Empty row removal
- Empty column removal
- Text cleanup
- Missing-value analysis
- Numeric missing-value handling
- Datetime detection
- Datetime conversion
- Time-feature generation
- Outlier analysis
- Column-level statistics
- Cleaning reports

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────────┐
                    │       FlowSync UI        │
                    │  Next.js + TypeScript    │
                    └────────────┬─────────────┘
                                 │
                                 │ HTTP / API
                                 ▼
                    ┌──────────────────────────┐
                    │      Python Backend      │
                    │    API + Processing      │
                    └────────────┬─────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
        ┌─────────────┐   ┌──────────────┐  ┌──────────────┐
        │ Data        │   │ AI / ML      │  │ Traffic      │
        │ Processing  │   │ Prediction   │  │ Analysis     │
        └─────────────┘   └──────────────┘  └──────────────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 ▼
                    ┌──────────────────────────┐
                    │ Traffic Dataset / Data  │
                    └──────────────────────────┘
```

---

# 📁 Project Structure

The repository is organized approximately as follows:

```text
FlowSync/
│
├── backend/
│   ├── ai/
│   │   └── models/
│   │       └── traffic_model.pkl       # ignored/not committed
│   │
│   └── ...
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── ...
│
├── data_cleaning/
│   ├── traffic_data_cleaner.py
│   └── ...
│
├── frontend/
│   ├── app/
│   │   ├── about/
│   │   ├── analytics/
│   │   ├── auth/
│   │   │   ├── forgot-password/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── dashboard/
│   │   ├── emergency/
│   │   ├── history/
│   │   ├── settings/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/
│   │   ├── AnalyticsCharts.tsx
│   │   ├── AnimatedCounter.tsx
│   │   ├── EmergencyBanner.tsx
│   │   ├── Navbar.tsx
│   │   ├── ResultsPanel.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Skeleton.tsx
│   │   └── UploadCard.tsx
│   │
│   ├── hooks/
│   │   ├── useBackendHealth.ts
│   │   └── useTrafficAnalysis.ts
│   │
│   ├── lib/
│   │   └── utils.ts
│   │
│   ├── services/
│   │   └── api.ts
│   │
│   ├── types/
│   │   └── traffic.ts
│   │
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| Next.js | React web application framework |
| React | UI development |
| TypeScript | Type-safe frontend development |
| CSS | Application styling |
| npm | JavaScript package management |

---

## Backend

| Technology | Purpose |
|---|---|
| Python | Backend and ML development |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn / ML libraries | Machine learning |
| API framework | Backend API |
| Pickle | Model serialization |

---

## Data Processing

| Technology | Purpose |
|---|---|
| Pandas | Dataset processing |
| NumPy | Numerical analysis |
| CSV | Dataset format |
| Excel | Dataset input support |

---

# 🎨 Frontend

The frontend is implemented using Next.js and TypeScript.

## Main Pages

### Home

The landing page introduces FlowSync and provides access to the traffic platform.

### Dashboard

The dashboard provides the main traffic analysis interface.

### Analytics

The analytics page presents traffic statistics and visualizations.

### History

The history section allows users to review previous traffic analysis information.

### Emergency

The emergency section provides traffic/emergency-related information and interface components.

### Authentication

The project contains pages for:

- Login
- Register
- Forgot Password

### Settings

The settings page provides application/user configuration options.

### About

The about page provides information about the FlowSync project.

---

# 🔧 Frontend Components

Important reusable components include:

```text
AnalyticsCharts
AnimatedCounter
EmergencyBanner
Navbar
ResultsPanel
Sidebar
Skeleton
UploadCard
```

These components are used to build the dashboard and analysis interface.

---

# 🧠 Frontend Hooks

The project includes custom React hooks such as:

```text
useBackendHealth
useTrafficAnalysis
```

These hooks help the frontend communicate with backend services and manage traffic-analysis state.

---

# 🔌 Frontend API Service

Backend communication is centralized through:

```text
frontend/services/api.ts
```

Traffic-related types are defined in:

```text
frontend/types/traffic.ts
```

---

# 🐍 Backend

The backend is responsible for:

- Receiving requests from the frontend
- Processing traffic information
- Running AI/ML predictions
- Processing datasets
- Returning traffic analysis results
- Providing backend health/status information

The backend code is located inside:

```text
backend/
```

---

# 🤖 AI and Machine Learning

FlowSync includes a trained traffic model.

The trained model is stored locally as:

```text
backend/ai/models/traffic_model.pkl
```

However, this file is **not committed to GitHub** because the model is approximately 139 MB.

GitHub has a 100 MB per-file limit for normal Git repositories.

The repository therefore ignores the model file.

---

# 📦 Model Deployment

To run the AI functionality on another machine, the required model file must be supplied separately.

Expected path:

```text
backend/ai/models/traffic_model.pkl
```

After placing the model there, the backend can load it through the existing AI pipeline.

> Do not commit the model directly using normal Git.

For large model distribution, alternatives include:

- Git LFS
- Hugging Face Hub
- Cloud storage
- Model registry
- Release assets

---

# 🧹 Data Cleaning Pipeline

The data-cleaning program is located in:

```text
data_cleaning/traffic_data_cleaner.py
```

It is designed to process traffic datasets before they are used for analysis or machine learning.

---

## Dataset Loading

The loader supports:

```text
.csv
.xlsx
.xls
```

Example:

```python
FILE_PATH = "../data/raw/traffic_dataset.csv"
```

---

## Column Name Cleaning

Column names are standardized by:

- Removing leading/trailing spaces
- Converting names to lowercase
- Replacing spaces with underscores
- Replacing hyphens with underscores

Example:

```text
Average Speed → average_speed
Traffic Volume → traffic_volume
Road-Type → road_type
```

---

## Duplicate Detection

The pipeline detects exact duplicate rows.

Example output:

```text
Duplicate rows found: 0
```

Duplicate rows are removed automatically.

---

## Empty Data Removal

Completely empty rows and columns are removed.

---

## Text Cleaning

Text/categorical columns are cleaned by:

- Converting values to strings
- Removing unnecessary whitespace
- Converting empty strings to missing values

---

## Datetime Processing

Datetime columns are detected and converted.

For example:

```text
timestamp
```

can be converted into a proper datetime column.

---

## Time Features

The pipeline generates:

```text
timestamp_hour
timestamp_day_of_week
timestamp_is_weekend
```

These features can be useful for traffic prediction.

---

## Missing Values

Numeric missing values are filled using the median of the corresponding column.

Example:

```text
temperature_c
humidity_pct
visibility_km
avg_speed_kmph
```

Categorical and datetime values are not automatically filled using the numeric median strategy.

---

## Outlier Detection

Numeric columns are analyzed using the IQR method.

The pipeline calculates:

```text
Q1
Q3
IQR
Lower Bound
Upper Bound
```

and counts values outside the IQR boundaries as possible outliers.

---

# 📊 Traffic Dataset

The traffic dataset used during development contains traffic, road, environmental, and contextual information.

The dataset processed during development contained approximately:

```text
Rows: 200,001
Original Columns: 35
Final Columns: 38
```

The additional columns came from generated time features.

Examples of traffic-related fields include:

```text
latitude
longitude
num_lanes
speed_limit_kmph
heavy_vehicle_pct
pedestrian_count
temperature_c
humidity_pct
visibility_km
avg_wait_time_sec
parking_occupancy_pct
air_quality_index
avg_speed_kmph
travel_time_index
```

Boolean/contextual fields include examples such as:

```text
is_peak_hour
is_weekend
is_public_holiday
incident_reported
road_closure
public_transport_nearby
school_zone
construction_zone
event_nearby
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/praveenperazhagan-create/FlowSync.git
```

Then:

```bash
cd FlowSync
```

---

# 🐍 Backend Setup

Create a Python virtual environment.

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 🧹 Run Data Cleaning

Move to the data-cleaning directory:

```powershell
cd data_cleaning
```

Run:

```powershell
python traffic_data_cleaner.py
```

The program generates cleaned data and analysis files according to the configured output paths.

Example output:

```text
traffic_dataset_cleaned.csv
column_summary.csv
data_cleaning_report.txt
```

---

# 🖥️ Frontend Setup

Open a second terminal.

Move into the frontend:

```powershell
cd frontend
```

Install Node dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

---

# 🚀 Running the Full Project

The project requires both the backend and frontend to be running.

## Terminal 1 — Backend

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then start the backend using the project's configured backend entry point.

For example, if the project uses FastAPI/Uvicorn:

```powershell
uvicorn <backend_module>:app --reload
```

Replace `<backend_module>` with the actual backend module used by the project.

---

## Terminal 2 — Frontend

```powershell
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:3000
```

---

# 🔐 Environment Variables

If the backend or frontend requires environment variables, create the appropriate local environment files.

Typical frontend configuration may use:

```text
frontend/.env.local
```

Typical backend configuration may use:

```text
backend/.env
```

Do not commit secrets such as:

```text
API keys
database passwords
authentication secrets
private tokens
cloud credentials
```

These should be included in `.gitignore`.

---

# 🔄 Data Processing Workflow

The overall data pipeline follows this flow:

```text
Raw Traffic Dataset
        │
        ▼
Dataset Loading
        │
        ▼
Duplicate Detection
        │
        ▼
Column Name Cleaning
        │
        ▼
Empty Row/Column Removal
        │
        ▼
Text Cleaning
        │
        ▼
Datetime Detection
        │
        ▼
Time Feature Creation
        │
        ▼
Missing Value Handling
        │
        ▼
Outlier Analysis
        │
        ▼
Column Summary
        │
        ▼
Cleaned Dataset
        │
        ▼
AI / Traffic Analysis
        │
        ▼
Frontend Dashboard
```

---

# 📈 Data Quality Report

The cleaning pipeline generates:

```text
data_cleaning_report.txt
```

The report contains information about:

- Original dataset size
- Final dataset size
- Duplicate rows
- Removed empty rows
- Removed empty columns
- Text/categorical columns
- Datetime columns
- Created time features
- Missing-value changes
- Column statistics
- Possible outliers

---

# 🧪 Data Quality Example

A successful cleaning run can report information such as:

```text
Rows: 200,001
Columns: 38
Remaining exact duplicates: 0
```

The exact results depend on the input dataset.

---

# 🔗 API Integration

The frontend communicates with the backend through the API service:

```text
frontend/services/api.ts
```

The application uses typed traffic-related interfaces from:

```text
frontend/types/traffic.ts
```

This keeps the frontend API interaction and traffic-data structures organized.

---

# 🗂️ Important Git Notes

The trained model:

```text
backend/ai/models/traffic_model.pkl
```

is intentionally excluded from normal Git tracking because it is larger than GitHub's 100 MB file limit.

The project should therefore keep the model in `.gitignore`.

Example:

```gitignore
backend/ai/models/traffic_model.pkl
```

Do not simply run:

```bash
git add -f backend/ai/models/traffic_model.pkl
```

because GitHub will reject the normal Git push if the file is larger than 100 MB.

---

# 🌐 GitHub Repository

Project repository:

https://github.com/praveenperazhagan-create/FlowSync

---

# 🐛 Troubleshooting

## GitHub says "File exceeds GitHub's file size limit"

If you see:

```text
GH001: Large files detected
```

check large files:

```powershell
git ls-files | ForEach-Object {
    if (Test-Path $_) {
        $size = (Get-Item $_).Length
        if ($size -gt 100MB) {
            Write-Host "$size $_"
        }
    }
}
```

The traffic model should remain outside normal Git tracking.

---

## Frontend dependencies fail

Try:

```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
npm run dev
```

---

## Python dependencies fail

Make sure the virtual environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
pip install -r requirements.txt
```

---

## Backend cannot find the model

Verify:

```text
backend/
└── ai/
    └── models/
        └── traffic_model.pkl
```

The model must be provided separately if it is not included in the repository.

---

## Frontend cannot connect to backend

Check:

1. Backend is running.
2. Frontend API URL is correct.
3. Required environment variables exist.
4. CORS configuration allows the frontend origin.
5. The backend port matches the frontend API configuration.

---

# 🔮 Future Improvements

Potential future improvements include:

- Real-time traffic data integration
- Live traffic maps
- GPS-based traffic monitoring
- More advanced ML models
- Deep-learning traffic prediction
- Model versioning
- Cloud model hosting
- Automated model retraining
- More advanced anomaly detection
- Traffic forecasting
- Route optimization
- Emergency vehicle routing
- Real-time incident detection
- Database-backed history
- User authentication backend
- Role-based access control
- Deployment using Docker
- CI/CD pipeline
- Cloud deployment
- Monitoring and logging
- Automated data ingestion

---

# 👥 Contributors

FlowSync is a collaborative full-stack project.

Contributors can work on:

- Frontend development
- Backend development
- AI/ML
- Data engineering
- UI/UX
- Testing
- Documentation
- Deployment

When contributing, create a separate branch where possible:

```bash
git checkout -b feature/your-feature
```

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

---

# 📜 License

Add the project's chosen license here.

For example:

```text
MIT License
```

If the project does not currently have a license, the repository owner should decide which license to use before adding one.

---

# ⭐ FlowSync

FlowSync brings together:

```text
Data Engineering
       +
Machine Learning
       +
Python Backend
       +
Next.js Frontend
       +
Traffic Analytics
       =
AI-Powered Traffic Intelligence Platform
```

The goal is to turn raw traffic data into useful insights through a complete end-to-end platform.
