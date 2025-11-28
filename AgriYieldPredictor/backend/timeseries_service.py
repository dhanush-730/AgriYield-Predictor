import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesService:
    def __init__(self):
        self.models = {}
        self.data = None
        self.load_data()
        self.train_models()
    
    def load_data(self):
        """Load and prepare time series data"""
        print("Loading time series data...")
        df = pd.read_csv("../recommended_time_series_dataset.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        self.data = df.sort_values(['Date', 'Crop_Type']).reset_index(drop=True)
        
    def prepare_crop_data(self, crop_name):
        """Prepare time series data for a specific crop"""
        crop_data = self.data[self.data['Crop_Type'] == crop_name].copy()
        crop_data = crop_data.sort_values('Date')
        
        # Create daily time series by taking mean yield per day
        daily_data = crop_data.groupby('Date')['Crop_Yield'].mean().reset_index()
        daily_data.set_index('Date', inplace=True)
        
        # Fill missing dates with forward fill
        date_range = pd.date_range(start=daily_data.index.min(), 
                                 end=daily_data.index.max(), freq='D')
        daily_data = daily_data.reindex(date_range).fillna(method='ffill')
        
        return daily_data['Crop_Yield']
    
    def train_models(self):
        """Train ARIMA models for all crops"""
        print("Training time series models...")
        crops = self.data['Crop_Type'].unique()
        
        for crop in crops:
            try:
                crop_data = self.prepare_crop_data(crop)
                
                if len(crop_data) < 50:  # Need minimum data
                    continue
                
                # Split data (90% train, 10% test)
                split = int(len(crop_data) * 0.9)
                train_data = crop_data[:split]
                
                # Fit ARIMA model
                model = ARIMA(train_data, order=(1,1,1))
                fitted_model = model.fit()
                
                self.models[crop] = {
                    'model': fitted_model,
                    'last_date': train_data.index[-1],
                    'last_value': train_data.iloc[-1]
                }
                
                print(f"Trained model for {crop}")
                
            except Exception as e:
                print(f"Error training model for {crop}: {str(e)}")
                continue
    
    def predict_future(self, crop_name, days=30):
        """Predict future yield for a specific crop"""
        if crop_name not in self.models:
            raise ValueError(f"No model available for {crop_name}")
        
        model_data = self.models[crop_name]
        model = model_data['model']
        
        # Generate forecast
        forecast = model.forecast(steps=days)
        
        # Create future dates
        last_date = model_data['last_date']
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                                   periods=days, freq='D')
        
        return {
            'dates': future_dates.strftime('%Y-%m-%d').tolist(),
            'predictions': forecast.tolist(),
            'crop': crop_name,
            'forecast_period': days
        }
    
    def get_crop_performance(self, crop_name):
        """Get model performance metrics for a crop"""
        if crop_name not in self.models:
            return None
        
        try:
            crop_data = self.prepare_crop_data(crop_name)
            split = int(len(crop_data) * 0.9)
            train_data = crop_data[:split]
            test_data = crop_data[split:]
            
            model = self.models[crop_name]['model']
            forecast = model.forecast(steps=len(test_data))
            
            # Calculate metrics
            mse = np.mean((test_data - forecast) ** 2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(test_data - forecast))
            
            # Calculate R²
            ss_res = np.sum((test_data - forecast) ** 2)
            ss_tot = np.sum((test_data - np.mean(test_data)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            return {
                'crop': crop_name,
                'rmse': float(rmse),
                'mae': float(mae),
                'r2': float(r2),
                'test_samples': len(test_data)
            }
            
        except Exception as e:
            print(f"Error calculating performance for {crop_name}: {str(e)}")
            return None
    
    def get_available_crops(self):
        """Get list of crops with trained models"""
        return list(self.models.keys())
    
    def get_crop_history(self, crop_name, days=365):
        """Get historical data for a crop"""
        if crop_name not in self.models:
            raise ValueError(f"No data available for {crop_name}")
        
        crop_data = self.prepare_crop_data(crop_name)
        
        # Get last N days of data
        recent_data = crop_data.tail(days)
        
        return {
            'dates': recent_data.index.strftime('%Y-%m-%d').tolist(),
            'values': recent_data.tolist(),
            'crop': crop_name,
            'period_days': len(recent_data)
        }

# Global instance
timeseries_service = TimeSeriesService()
