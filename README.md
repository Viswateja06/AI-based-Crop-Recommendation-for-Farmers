# GreenPulse India: AI-Based Farmer Query Support and Advisory System

## Overview
This is a full-stack, AI-powered agricultural advisory platform designed to help farmers by answering queries related to crops, diseases, soil, weather, fertilizers, market prices, and government schemes.

It features a state-of-the-art responsive interface, a FastAPI backend, and fully localized and dynamic Artificial Intelligence running on your own computer hardware.

## Key Features
- **Multilingual Offline AI Chatbot:** Natively processes and streams conversational AI responses in 8 regional languages (English, Hindi, Telugu, Tamil, Malayalam, Marathi, Odia, Kannada) using a completely offline instance of **Ollama (Llama 3.2)**.
- **Real-Time Data (RAG):** The AI chatbot dynamically scrapes Wikipedia, Google News RSS, and live search HTML to provide up-to-date accurate market prices, agricultural news, and context.
- **Disease & Pest Detection:** Image upload module targeting crop leaf analysis powered by a PyTorch Convolutional Neural Network (ResNet18). Features aggressive data augmentation and Transfer Learning targeting to robustly isolate single leaves and ignore human hands/background noise.
- **Crop & Fertilizer Recommendation:** Recommends the most suitable seeds using a scikit-learn Random Forest model trained on NPK, pH, temperature, and rainfall datasets.
- **Weather Advisory:** Dashboard generating intelligent alerts based on real-time environmental APIs.

## Tech Stack
- **Frontend:** React.js, TailwindCSS, Vite, Axios, Lucide React.
- **Backend:** Python, FastAPI, Uvicorn, BeautifulSoup4, Feedparser.
- **AI & ML:** Ollama (Llama 3.2), Scikit-learn, Pandas, PyTorch (Transfer Learning).

## Setup Instructions

### 1. Artificial Intelligence Component (Ollama)
This project requires absolutely no cloud API keys. It runs 100% offline.
1. Download & Install [Ollama](https://ollama.com/)
2. Open a terminal and run `ollama run llama3.2` to download the generative model to your machine. 

### 2. Backend Setup & Machine Learning
For the ML models to work correctly, you must train them on your local system first.
1. Open a terminal and navigate to the project directory: `cd backend`
2. Activate a Virtual Environment: `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `python -m pip install -r requirements.txt` (All libraries including RAG scrapers and kagglehub will install securely).
4. Download the dataset & train the crop recommendation model:
   - `python ml_models\generate_data.py`
   - `python ml_models\crop_recommendation.py`
5. Download the PlantVillage images & train the Disease Recognition CNN:
   - `python ml_models\train_disease_model.py` *(Highly optimized via base-layer freezing to finish epochs in seconds)*
6. Start the server:
   - `python -m uvicorn app.main:app --reload`
   - The backend runs on `http://127.0.0.1:8000`.

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Build and launch the UI: `npm run dev`
4. Open your browser to `http://localhost:5173`.
