# AI-Based Farmer Query Support and Advisory System

## Overview
This is a full-stack, AI-powered agricultural advisory platform designed to help farmers by answering queries related to crops, diseases, soil, weather, fertilizers, market prices, and government schemes.

It integrates both Natural Language Processing (intent routing logic) and Machine Learning (Random Forest for crop recommendation, Mock CNN for disease detection).

## Features
- **Farmer Query Chatbot:** Simulated NLP intent detection and response generation.
- **Disease & Pest Detection:** Image upload module targeting crop leaf analysis.
- **Crop & Fertilizer Recommendation:** Utilizes a custom-trained scikit-learn Random Forest model trained on synthetic NPk, pH, temperature, and rainfall datasets.
- **Weather Advisory:** Dashboard generating mock intelligent alerts based on environmental conditions.

## Tech Stack
- **Frontend:** React.js, TailwindCSS, Vite, Axios, Lucide React (Icons).
- **Backend:** Python, FastAPI, Uvicorn.
- **ML & Data:** Scikit-learn, Pandas, NumPy, PyTorch (mock implementation).
- **Database:** SQLite / PostgreSQL (implemented via SQLAlchemy).

## Setup Instructions

### 1. Backend Setup
1. Open terminal and navigate to the project directory.
2. Change context to the backend: `cd backend`
3. Activate Virtual Environment (if not active): `.\venv\Scripts\Activate.ps1`
4. Make sure dependencies are installed: `pip install -r requirements.txt` (or install manually as listed in project definition files).
5. Generate the synthetic dataset and train the ML Model:
   - `cd ml_models`
   - `python generate_data.py`
   - `python crop_recommendation.py`
   - `cd ..`
6. Run the local uvicorn server:
   - `uvicorn app.main:app --reload`
   - API will be live at `http://127.0.0.1:8000`. You can see auto-generated docs at `/docs`.

### 2. Frontend Setup
1. Open a new terminal instance.
2. Change context to the frontend: `cd frontend`
3. Install dependencies: `npm install`
4. Run the development server:
   - `npm run dev`
   - Web App will be live at `http://localhost:5173`.

## Architecture Details
The system utilizes a central API routing core (`app.agent.controller.py`) which processes chatbot input. Given bandwidth limits common in target regions, images and external APIs are accessed efficiently out-of-band when explicitly requested (such as in disease detection). Responsive styling is primarily handled via Tailwind CSS Utility classes avoiding huge CSS file transfers.
