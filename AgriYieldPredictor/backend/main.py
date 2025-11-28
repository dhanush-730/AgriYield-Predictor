from fastapi import FastAPI, HTTPException
from models.YieldPrediction import YieldPrediction
from utils import get_weather_condition, get_crop_type, get_soil_type
from timeseries_service import timeseries_service
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware

pipeline = joblib.load("final_yield_pipeline.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health-check")
def health_check():
    return "Working"

@app.get("/crop_types")
def get_crop_types():
    return get_crop_type()

@app.get("/soil_types")
def get_soil_types():
    return get_soil_type()

@app.get("/weather_conditions")
def get_weather_conditions():
    return get_weather_condition()

@app.post("/predict")
def predict(yieldPrediction: YieldPrediction):
    sample = pd.DataFrame([yieldPrediction.dict()])
    prediction = pipeline.predict(sample)
    # Return the prediction as a float
    return {"predicted_yield": float(prediction[0])}

# Time Series Endpoints
@app.get("/timeseries/crops")
def get_timeseries_crops():
    """Get list of crops available for time series prediction"""
    try:
        crops = timeseries_service.get_available_crops()
        return {"crops": crops}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/timeseries/forecast/{crop_name}")
def get_timeseries_forecast(crop_name: str, days: int = 30):
    """Get time series forecast for a specific crop"""
    try:
        if days < 1 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        forecast = timeseries_service.predict_future(crop_name, days)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/timeseries/performance/{crop_name}")
def get_timeseries_performance(crop_name: str):
    """Get model performance metrics for a specific crop"""
    try:
        performance = timeseries_service.get_crop_performance(crop_name)
        if performance is None:
            raise HTTPException(status_code=404, detail=f"No performance data available for {crop_name}")
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/timeseries/history/{crop_name}")
def get_timeseries_history(crop_name: str, days: int = 365):
    """Get historical data for a specific crop"""
    try:
        if days < 1 or days > 3650:  # Max 10 years
            raise HTTPException(status_code=400, detail="Days must be between 1 and 3650")
        
        history = timeseries_service.get_crop_history(crop_name, days)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/timeseries/summary")
def get_timeseries_summary():
    """Get summary of all available time series models"""
    try:
        crops = timeseries_service.get_available_crops()
        summary = []
        
        for crop in crops:
            performance = timeseries_service.get_crop_performance(crop)
            if performance:
                summary.append(performance)
        
        # Sort by RMSE (lower is better)
        summary.sort(key=lambda x: x['rmse'])
        
        return {
            "total_crops": len(summary),
            "crop_performance": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))