from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load the model
MODEL_PATH = "crop_recommendation_model.pkl"
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model file not found. Please train the model first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        load_model()
        if model is None:
            return jsonify({'error': 'Model not available. Please ensure the model is trained.'}), 500

    try:
        data = request.json
        # Create DataFrame with valid feature names
        features_dict = {
            'N': [float(data['N'])],
            'P': [float(data['P'])],
            'K': [float(data['K'])],
            'temperature': [float(data['temperature'])],
            'humidity': [float(data['humidity'])],
            'ph': [float(data['ph'])],
            'rainfall': [float(data['rainfall'])]
        }
        
        features_df = pd.DataFrame(features_dict)
        prediction = model.predict(features_df)[0]
        
        return jsonify({'prediction': prediction, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

if __name__ == '__main__':
    load_model()
    app.run(debug=True, use_reloader=False)
