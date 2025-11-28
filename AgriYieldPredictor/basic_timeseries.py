import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv('AgriYieldPredictor/recommended_time_series_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Get all unique crops
crops = df['Crop_Type'].unique()
print(f"Found {len(crops)} crops: {list(crops)}")

results = {}

# Process each crop
for crop in crops:
    print(f"\nProcessing {crop}...")
    
    # Get crop data and create time series
    crop_data = df[df['Crop_Type'] == crop].copy()
    crop_data = crop_data.sort_values('Date')
    daily_yield = crop_data.groupby('Date')['Crop_Yield'].mean()
    
    # Split data (80% train, 20% test)
    split = int(len(daily_yield) * 0.8)
    train = daily_yield[:split]
    test = daily_yield[split:]
    
    # Fit simple ARIMA model
    model = ARIMA(train, order=(1,1,1))
    fitted = model.fit()
    
    # Make predictions
    forecast = fitted.forecast(steps=len(test))
    
    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(test, forecast))
    results[crop] = rmse
    print(f"{crop} RMSE: {rmse:.4f}")

# Print summary
print("\n" + "="*50)
print("TIME SERIES MODEL RESULTS FOR ALL CROPS")
print("="*50)
for crop, rmse in results.items():
    print(f"{crop:12}: RMSE = {rmse:.4f}")

# Find best and worst performing crops
best_crop = min(results, key=results.get)
worst_crop = max(results, key=results.get)
print(f"\nBest performing crop: {best_crop} (RMSE: {results[best_crop]:.4f})")
print(f"Worst performing crop: {worst_crop} (RMSE: {results[worst_crop]:.4f})")

# Plot results for top 3 crops
top_crops = sorted(results.items(), key=lambda x: x[1])[:3]

plt.figure(figsize=(15, 10))
for i, (crop, rmse) in enumerate(top_crops, 1):
    # Get crop data
    crop_data = df[df['Crop_Type'] == crop].copy()
    crop_data = crop_data.sort_values('Date')
    daily_yield = crop_data.groupby('Date')['Crop_Yield'].mean()
    
    # Split data
    split = int(len(daily_yield) * 0.8)
    train = daily_yield[:split]
    test = daily_yield[split:]
    
    # Fit model and predict
    model = ARIMA(train, order=(1,1,1))
    fitted = model.fit()
    forecast = fitted.forecast(steps=len(test))
    
    # Plot
    plt.subplot(2, 2, i)
    plt.plot(train.index, train.values, label='Training', color='blue', alpha=0.7)
    plt.plot(test.index, test.values, label='Actual', color='green')
    plt.plot(test.index, forecast, label='ARIMA Forecast', color='red', linestyle='--')
    plt.title(f'{crop} Yield Prediction (RMSE: {rmse:.3f})')
    plt.xlabel('Date')
    plt.ylabel('Crop Yield')
    plt.legend()
    plt.xticks(rotation=45)

# Add summary plot
plt.subplot(2, 2, 4)
crop_names = list(results.keys())
rmse_values = list(results.values())
bars = plt.bar(range(len(crop_names)), rmse_values, color='skyblue')
plt.title('RMSE Comparison - All Crops')
plt.xlabel('Crops')
plt.ylabel('RMSE')
plt.xticks(range(len(crop_names)), crop_names, rotation=45)
plt.tight_layout()

# Add value labels on bars
for i, (bar, rmse) in enumerate(zip(bars, rmse_values)):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
             f'{rmse:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('AgriYieldPredictor/all_crops_timeseries.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nSimple time series model completed for all crops!")
