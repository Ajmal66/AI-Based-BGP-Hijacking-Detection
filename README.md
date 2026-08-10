# AI-Based BGP Hijacking Detection System

> An AI/ML-based system for detecting and analyzing potential BGP hijacking events using BGP routing data, feature engineering, and machine learning models.

---

## 📌 Overview

**Border Gateway Protocol (BGP)** is the protocol used to exchange routing information between Autonomous Systems (ASes) on the Internet.

BGP hijacking occurs when unauthorized or malicious routing announcements cause Internet traffic to be incorrectly redirected.

This project develops an **AI/ML-based BGP hijacking detection system** that processes BGP routing information, extracts meaningful features, trains machine learning models, and identifies potential hijacking events through a Flask-based web application.

---

## 🎯 Objectives

The main objectives of this project are to:

- Process and analyze BGP routing data
- Clean and preprocess routing datasets
- Extract meaningful BGP features
- Engineer features for machine learning
- Generate synthetic BGP hijacking scenarios
- Train multiple machine learning models
- Detect potential BGP hijacking events
- Provide a web-based interface for dataset analysis
- Generate prediction and analysis results

---

## 🔄 System Architecture

```text
                         BGP Routing Data
                                │
                                ▼
                    ┌─────────────────────┐
                    │    Data Ingestion   │
                    │ RIPE / RouteViews / │
                    │        CSV          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Preprocessing  │
                    │ Cleaning & Parsing  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Feature Engineering │
                    │ BGP Feature         │
                    │ Extraction          │
                    └──────────┬──────────┘
                               │
                               ▼
                  ┌──────────────────────────┐
                  │     Model Training       │
                  │                          │
                  │  Random Forest           │
                  │  Support Vector Machine  │
                  │  LSTM                    │
                  └────────────┬─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Prediction Pipeline │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ BGP Hijacking Detection  │
                 └────────────┬─────────────┘
                              │
                              ▼
                     Results & Analysis
```

---

## 🤖 Machine Learning Models

The project includes multiple machine learning approaches for BGP hijacking detection.

### 🌲 Random Forest

A tree-based supervised learning algorithm used to classify BGP routing observations using engineered routing features.

### 📈 Support Vector Machine (SVM)

A supervised machine learning algorithm used to classify routing observations based on extracted BGP characteristics.

### 🧠 Long Short-Term Memory (LSTM)

A deep learning model designed to process sequential information and identify patterns within BGP routing data.

---

## 🔍 BGP Features

The system works with routing-related features such as:

- Prefix
- Prefix length
- Peer IP
- Peer ASN
- Origin ASN
- AS path
- AS path length
- Unique AS count
- Next hop
- Local preference
- MED
- AS-path prepending indicator
- Origin position
- Origin-at-end indicator
- Event type
- Classification label

---

## 📊 Data Processing Pipeline

The system processes BGP data through the following stages:

```text
Raw BGP Data
     │
     ▼
Data Ingestion
     │
     ▼
Data Parsing
     │
     ▼
Data Cleaning
     │
     ▼
Feature Extraction
     │
     ▼
Feature Engineering
     │
     ▼
Model Training
     │
     ▼
Prediction
     │
     ▼
Evaluation & Results
```

---

## 📁 Project Structure

| Directory / File | Description |
|---|---|
| 📂 `app/` | Flask web application components |
| 📂 `src/data_preprocessing/` | Dataset cleaning, loading, and preprocessing |
| 📂 `src/ingestion/` | BGP data ingestion and parsing |
| 📂 `src/feature_engineering/` | BGP feature extraction and feature construction |
| 📂 `src/model_training/` | Machine learning model training scripts |
| 📂 `src/prediction/` | BGP hijacking prediction and detection logic |
| 📂 `src/prediction_pipeline/` | Dataset upload and prediction processing pipeline |
| 📂 `src/evaluation/` | Model evaluation and performance metrics |
| 📂 `models/` | Trained machine learning model files |
| 📂 `datasets/sample/` | Small sample dataset for demonstration and testing |
| 📂 `datasets/raw/` | Original BGP datasets, excluded because of size |
| 📂 `datasets/processed/` | Processed datasets, excluded because of size |
| 📂 `results/` | Generated prediction and analysis results |
| 📄 `app.py` | Main Flask application entry point |
| 📄 `requirements.txt` | Python dependencies |
| 📄 `.gitignore` | Files excluded from version control |
| 📄 `README.md` | Project documentation |

---

## 🛠️ Technologies

### Programming Language

- Python

### Web Framework

- Flask

### Machine Learning

- Scikit-learn
- TensorFlow
- Keras
- Joblib

### Data Processing

- Pandas
- NumPy

### BGP Data

- RIPE RIS
- RouteViews
- CSV-based BGP datasets

### Visualization & Analysis

- Matplotlib
- Plotly

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ajmal66/AI-Based-BGP-Hijacking-Detection.git
```

### 2. Enter the project directory

```bash
cd AI-Based-BGP-Hijacking-Detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application provides a web-based interface for interacting with the BGP hijacking detection system.

---

## 📂 Dataset

The project supports BGP routing data from sources and formats including:

- RIPE RIS
- RouteViews
- CSV datasets

Because raw and processed BGP datasets can be very large, they are **not included in this repository**.

A small sample dataset is provided for demonstration and testing.

```text
datasets/
├── sample/
├── raw/
└── processed/
```

The preprocessing and ingestion modules can be used to process the required datasets.

---

## 📈 Results

The system generates prediction and analysis results after processing BGP routing data through the detection pipeline.

Large generated result files are intentionally excluded from the repository to keep the project lightweight and manageable.

Results can be reproduced by running the appropriate preprocessing, prediction, and evaluation components.

---

## 🔐 Repository & Data Management

Large or generated files are excluded from version control, including:

- Raw BGP datasets
- Processed datasets
- Generated prediction results
- Application logs
- User-uploaded files
- Python cache files
- Local environment files

This keeps the repository focused on the **source code, models, configuration, and reproducible sample data**.

---

## 🚀 Future Improvements

Future development may include:

- Real-time BGP monitoring
- Live routing-feed integration
- Automated hijacking alerts
- Improved anomaly detection
- Additional machine learning models
- Larger and more diverse training datasets
- Real-time visualization
- Improved prediction analytics
- Automated notification mechanisms

---

## 🎓 Academic Project


This project was developed as a **Final Year Project** in the field of:

**Cybersecurity | Network Security | BGP Security | Artificial Intelligence | Machine Learning**

### Academic Achievement

🏆 **Grade: A**

The project was successfully evaluated and awarded an **A grade** as part of the university's Final Year Project assessment..



---

## 👨‍💻 Author

### Ajmal Sadiq

Cybersecurity Student | Network Security | Ethical Hacking | AI/ML

GitHub: [@Ajmal66](https://github.com/Ajmal66)

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
