import pandas as pd
import numpy as np
import os

def generate_crop_data():
    """Generates a synthetic dataset for Crop Recommendation."""
    print("Generating synthetic crop recommendation dataset...")
    np.random.seed(42)

    # Simplified list of crops
    crops = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
             'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
             'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
             'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']

    data = []
    # Generate around 100 samples per crop with some assumed realistic ranges
    for crop in crops:
        for _ in range(100):
            if crop in ['rice', 'jute']: # high water/temp
                n, p, k = np.random.randint(60, 100), np.random.randint(30, 60), np.random.randint(30, 50)
                temp = np.random.uniform(20.0, 30.0)
                hum = np.random.uniform(80.0, 95.0)
                ph = np.random.uniform(5.0, 7.5)
                rain = np.random.uniform(150.0, 300.0)
            elif crop in ['apple', 'grapes']: # cooler, moderate water
                n, p, k = np.random.randint(10, 40), np.random.randint(120, 140), np.random.randint(190, 205)
                temp = np.random.uniform(10.0, 25.0)
                hum = np.random.uniform(80.0, 95.0)
                ph = np.random.uniform(5.5, 6.5)
                rain = np.random.uniform(60.0, 120.0)
            else: # general mix
                n, p, k = np.random.randint(20, 120), np.random.randint(10, 80), np.random.randint(10, 80)
                temp = np.random.uniform(18.0, 35.0)
                hum = np.random.uniform(40.0, 85.0)
                ph = np.random.uniform(5.5, 7.5)
                rain = np.random.uniform(40.0, 150.0)

            data.append([n, p, k, temp, hum, ph, rain, crop])

    df = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/crop_recommendation.csv', index=False)
    print("Dataset saved to ../data/crop_recommendation.csv")

if __name__ == "__main__":
    generate_crop_data()
