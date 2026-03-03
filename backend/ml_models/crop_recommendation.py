import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_model():
    print("Training Crop Recommendation Model...")
    data_path = '../data/crop_recommendation.csv'
    
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Please run generate_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    features = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    target = df['label']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model trained successfully. Accuracy: {accuracy * 100:.2f}%")

    model_dir = '../ml_models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'crop_rf_model.pkl')
    joblib.dump(rf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
