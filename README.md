<<<<<<< HEAD
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
=======
# AI-Based Crop Recommendation System

An AI-driven decision support system that recommends the most suitable crop for farmers based on soil and weather parameters using a Random Forest Machine Learning model.

## Features
- **Accurate Predictions**: Uses a Random Forest classifier trained on agricultural data.
- **Paramaters**: Considers Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, and Rainfall.
- **Modern UI**: Clean, responsive, and glassmorphism-based design.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation & Setup

1.  **Clone/Download the project** to your local machine.
2.  **Navigate to the project directory**:
    ```bash
    cd crop_recommendation_system
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Training the Model
Before running the application, you must train the machine learning model.
```bash
python train_model.py
```
This script will:
- Download the dataset (`cropdata.csv`) automatically.
- Train the Random Forest model.
- Save the model as `crop_recommendation_model.pkl`.
- Print the model's accuracy.

## Running the Application
1.  **Start the Flask server**:
    ```bash
    python app.py
    ```
2.  **Open your browser** and go to:
    ```
    http://127.0.0.1:5000
    ```

## Usage
1.  Enter the soil and climate parameters in the form.
2.  Click "Get Recommendation".
3.  The system will display the best crop for your conditions.

## Project Structure
- `app.py`: Main Flask application.
- `train_model.py`: Script to train and save the ML model.
- `templates/index.html`: Frontend HTML.
- `static/css/style.css`: Frontend Styling.
- `static/js/script.js`: Frontend Logic.
- `requirements.txt`: Python dependencies.
>>>>>>> origin/main
