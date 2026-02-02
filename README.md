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
