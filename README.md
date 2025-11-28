
# 🌾 AgriYieldPredictor

AgriYieldPredictor is a machine-learning–based application designed to predict crop yields using a trained ML pipeline and generate time-series trend visualizations. The project includes a backend prediction service, forecasting scripts, and utilities to support analysis and visualization.

---

## 📌 Key Features

### 🤖 ML-Based Yield Prediction
- Uses trained pipeline: **`final_yield_pipeline.pkl`**
- Prediction handled by **`YieldPrediction.py`**
- Processes input features and returns yield values
- Supports real-time predictions through backend server

### 📈 Time-Series Trend Forecasting
- Implemented in **`timeseries_service.py`** and **`basic_timeseries.py`**
- Generates future trend lines for crop production
- Creates visualization outputs saved into the project

### 🖥️ Backend Service
- Backend server controlled by **`start_server.py`**
- Handles API-based predictions and communication with frontend
- Utility processing via **`output_utils.py`**

### 📊 Data Analysis
- Exploratory and analytical notebook: **`Crop_Yield_Analysis.ipynb`**
- Helps understand dataset patterns and feature relationships

---

## 🗂️ Project Structure

AgriYieldPredictor/
│
├── Analysis/
│ └── Crop_Yield_Analysis.ipynb
│
├── Backend/
│ ├── YieldPrediction.py
│ ├── timeseries_service.py
│ ├── start_server.py
│ └── utils/
│ └── output_utils.py
│
├── Dataset/
│ └── yield_1.csv
│
├── Frontend/
│ └── (frontend files and UI assets)
│
├── Scripts/
│ └── basic_timeseries.py
│
├── model/
│ └── final_yield_pipeline.pkl
│
└── Visuals/
└── (generated plots and graphs)


---

## 🚀 Getting Started

### Install Requirements
```bash
pip install -r requirements.txt

Run Backend Prediction Server
python Backend/start_server.py

Run Yield Prediction Manually
python Backend/YieldPrediction.py

Generate Time-Series Forecast Plot
python Scripts/basic_timeseries.py


Outputs will be saved in the Visuals/ directory.

🛠️ Technologies Used

Python

scikit-learn

Pandas

NumPy

Matplotlib

Custom ML Pipelines

Backend server (Python)
