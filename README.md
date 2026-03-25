# AI-Based Farmer Query Support and Advisory System

## Overview
This is a full-stack, AI-powered agricultural advisory platform designed to help farmers by answering queries related to crops, diseases, soil, weather, fertilizers, market prices, and government schemes.

It features a state-of-the-art responsive interface, a FastAPI backend, and fully localized and dynamic Artificial Intelligence running on your own computer hardware.

## Features
- **Farmer Query Chatbot:** Natively processes and streams conversational AI responses and detects agricultural intents (weather, market, disease) using a completely offline instance of **Ollama (Llama 3.2)**.
- **Disease & Pest Detection:** Image upload module targeting crop leaf analysis powered by a custom PyTorch Convolutional Neural Network (ResNet18) trained on the PlantVillage dataset.
- **Crop & Fertilizer Recommendation:** Recommends the most suitable seeds using a scikit-learn Random Forest model trained on NPk, pH, temperature, and rainfall datasets.
- **Weather Advisory:** Dashboard generating intelligent alerts based on environmental conditions.

## Tech Stack
- **Frontend:** React.js, TailwindCSS, Vite, Axios, Lucide React (Icons).
- **Backend:** Python, FastAPI, Uvicorn.
- **AI & ML:** Ollama (Llama 3.2), Scikit-learn, Pandas, NumPy, PyTorch.

## Setup Instructions

### 1. Artificial Intelligence Component (Ollama)
Instead of relying on costly external API keys (like OpenAI or HuggingFace), this project has been fully updated to run offline natively.
1. Download & Install [Ollama](https://ollama.com/)
2. Open a terminal and run `ollama run llama3.2` to download the generative model to your machine. 

### 2. Backend Setup & Machine Learning
For the ML models to work correctly, you must train them on your local system first.
1. Open a terminal and navigate to the project directory: `cd backend`
2. Activate a Virtual Environment: `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt` (and check `pip install kagglehub` for the image downloader)
4. Download the dataset & train the crop recommendation model:
   - `python ml_models\generate_data.py`
   - `python ml_models\crop_recommendation.py`
5. Download the PlantVillage images & train the Disease Recognition CNN:
   - `python ml_models\train_disease_model.py` *(Warning: High computational cost!)*
6. Start the server:
   - `uvicorn app.main:app --reload`
   - The backend runs on `http://127.0.0.1:8000`.

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Build and launch the UI: `npm run dev`
4. Open your browser to `http://localhost:5173`.

## Architecture Highlights
- The frontend guarantees seamless tab-switching by seamlessly hiding components (rather than destroying them) inside the shadow DOM, ensuring typed conversation histories and analysis results are permanently retained when switching navigation menu tabs.
- Chatbot responses dynamically scroll to the bottom of the page in real-time as the AI streams its text generation back to the farmer using a bespoke visual typewriter component.
