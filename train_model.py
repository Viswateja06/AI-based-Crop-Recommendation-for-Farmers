import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import requests
import os

# Configuration
DATASET_URL = "https://raw.githubusercontent.com/Gladiator07/Harvestify/master/Data-processed/crop_recommendation.csv"
DATASET_PATH = "cropdata.csv"
MODEL_PATH = "crop_recommendation_model.pkl"

def download_dataset():
    if not os.path.exists(DATASET_PATH):
        print(f"Downloading dataset from {DATASET_URL}...")
        response = requests.get(DATASET_URL)
        if response.status_code == 200:
            with open(DATASET_PATH, 'wb') as f:
                f.write(response.content)
            print("Dataset downloaded successfully.")
        else:
            print(f"Failed to download dataset. Status code: {response.status_code}")
            exit(1)
    else:
        print("Dataset already exists.")

def train_model():
    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # Check for missing values
    if df.isnull().sum().sum() > 0:
        print("Warning: Missing values found. Dropping rows with missing values...")
        df.dropna(inplace=True)
        
    # Features and Target
    # Assumes columns are N, P, K, temperature, humidity, ph, rainfall, label
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save Model
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(rf, MODEL_PATH)
    print("Model saved successfully.")

if __name__ == "__main__":
    download_dataset()
    train_model()
