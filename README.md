Machine Learning Models

The project includes three machine learning approaches:

Random Forest

A tree-based machine learning model used for classification using engineered BGP route features.

Support Vector Machine (SVM)

A supervised learning model used to classify routing observations based on extracted BGP features.

LSTM

A sequence-based deep learning model used to analyze AS-path information and identify patterns associated with potential hijacking events.

BGP Features

The project uses features including:

Prefix length
AS path length
Unique AS count
AS-path prepending indicator
Origin position
Origin-at-end indicator
Peer ASN
AS path
Project Structure
AI-Based-BGP-Hijacking-Detection/
│
├── app/
│   └── ...
│
├── datasets/
│   ├── sample/
│   ├── processed/
│   └── raw/
│
├── models/
│   ├── lstm_maxlen.pkl
│   ├── lstm_model.keras
│   ├── lstm_tokenizer.pkl
│   └── svm_model.pkl
│
├── results/
│   └── README.md
│
├── src/
│   ├── data_preprocessing/
│   ├── evaluation/
│   ├── feature_engineering/
│   ├── ingestion/
│   ├── model_training/
│   ├── prediction/
│   └── prediction_pipeline/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
Data Processing

The system processes BGP routing data through multiple stages:

Data ingestion
Dataset parsing
Data cleaning
Feature extraction
Feature engineering
Model training
Prediction
Result generation

Large raw and processed datasets are intentionally excluded from the repository. A small sample dataset is provided for demonstration and testing.

Installation

Clone the repository:

git clone https://github.com/Ajmal66/AI-Based-BGP-Hijacking-Detection.git
cd AI-Based-BGP-Hijacking-Detection

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt
Running the Application

Start the Flask application:

python app.py

The application will start locally and provide a web interface for interacting with the BGP hijacking detection system.

Dataset

The project uses BGP routing information and supports processing data associated with:

RIPE RIS
RouteViews
CSV datasets

Large datasets are not included in this repository because of their size. The preprocessing and ingestion modules provide the functionality required to process the datasets.

Results

The system generates prediction and analysis results from the trained machine learning models.

Large generated result files are excluded from the repository to keep the project lightweight and reproducible.

Technologies
Python
Flask
Pandas
NumPy
Scikit-learn
TensorFlow
Keras
Joblib
BGP data processing tools
HTML/CSS/JavaScript
Project Purpose

This project was developed as a Final Year Project to investigate the application of artificial intelligence and machine learning techniques for detecting potential BGP hijacking events.

Future Improvements

Potential future improvements include:

Real-time BGP monitoring
Live routing-feed integration
Improved anomaly detection
Additional machine learning models
Real-time alerting
Larger and more diverse training datasets
Improved visualization and analytics
Author

Ajmal Sadiq

Final Year Cybersecurity Project

GitHub: Ajmal66
