import React, { useState, useEffect } from "react";
import "./TimeSeriesPage.css";
import axios from "axios";

const TimeSeriesPage = () => {
  const [availableCrops, setAvailableCrops] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState("");
  const [forecastDays, setForecastDays] = useState(30);
  const [forecastData, setForecastData] = useState(null);
  const [historyData, setHistoryData] = useState(null);
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [activeTab, setActiveTab] = useState("forecast");

  // Load available crops on component mount
  useEffect(() => {
    loadAvailableCrops();
  }, []);

  const loadAvailableCrops = async () => {
    try {
      const response = await axios.get("http://localhost:3001/timeseries/crops");
      setAvailableCrops(response.data.crops);
      if (response.data.crops.length > 0) {
        setSelectedCrop(response.data.crops[0]);
      }
    } catch (error) {
      setErrorMsg("Failed to load available crops: " + error.message);
    }
  };

  const loadForecast = async () => {
    if (!selectedCrop) return;
    
    setLoading(true);
    setErrorMsg("");
    
    try {
      const response = await axios.get(
        `http://localhost:3001/timeseries/forecast/${selectedCrop}?days=${forecastDays}`
      );
      setForecastData(response.data);
    } catch (error) {
      setErrorMsg("Failed to load forecast: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    if (!selectedCrop) return;
    
    setLoading(true);
    setErrorMsg("");
    
    try {
      const response = await axios.get(
        `http://localhost:3001/timeseries/history/${selectedCrop}?days=365`
      );
      setHistoryData(response.data);
    } catch (error) {
      setErrorMsg("Failed to load history: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPerformance = async () => {
    if (!selectedCrop) return;
    
    setLoading(true);
    setErrorMsg("");
    
    try {
      const response = await axios.get(
        `http://localhost:3001/timeseries/performance/${selectedCrop}`
      );
      setPerformanceData(response.data);
    } catch (error) {
      setErrorMsg("Failed to load performance: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (tab === "forecast") {
      loadForecast();
    } else if (tab === "history") {
      loadHistory();
    } else if (tab === "performance") {
      loadPerformance();
    }
  };

  const formatNumber = (num) => {
    return typeof num === 'number' ? num.toFixed(2) : num;
  };

  return (
    <div className="timeseries-bg">
      <div className="timeseries-container">
        <h2 className="timeseries-title">📈 Time Series Crop Yield Prediction</h2>
        <p className="timeseries-desc">
          Analyze historical trends and predict future crop yields using ARIMA time series models.
        </p>

        {/* Controls */}
        <div className="controls-section">
          <div className="control-group">
            <label className="control-label">🌾 Select Crop:</label>
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="control-select"
            >
              <option value="">Select a crop</option>
              {availableCrops.map((crop) => (
                <option key={crop} value={crop}>
                  {crop}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label className="control-label">📅 Forecast Days:</label>
            <input
              type="number"
              value={forecastDays}
              onChange={(e) => setForecastDays(parseInt(e.target.value))}
              className="control-input"
              min="1"
              max="365"
            />
          </div>
        </div>

        {/* Tabs */}
        <div className="tabs-section">
          <button
            className={`tab-button ${activeTab === "forecast" ? "active" : ""}`}
            onClick={() => handleTabChange("forecast")}
          >
            🔮 Forecast
          </button>
          <button
            className={`tab-button ${activeTab === "history" ? "active" : ""}`}
            onClick={() => handleTabChange("history")}
          >
            📊 History
          </button>
          <button
            className={`tab-button ${activeTab === "performance" ? "active" : ""}`}
            onClick={() => handleTabChange("performance")}
          >
            📈 Performance
          </button>
        </div>

        {/* Loading */}
        {loading && (
          <div className="loading-section">
            <div className="loading-spinner"></div>
            <p>Loading data...</p>
          </div>
        )}

        {/* Error */}
        {errorMsg && (
          <div className="error-section">
            <h3 className="error-title">❌ Error</h3>
            <p className="error-message">{errorMsg}</p>
          </div>
        )}

        {/* Forecast Tab */}
        {activeTab === "forecast" && forecastData && (
          <div className="results-section">
            <h3 className="results-title">🔮 {selectedCrop} Yield Forecast</h3>
            <div className="forecast-info">
              <p><strong>Forecast Period:</strong> {forecastData.forecast_period} days</p>
              <p><strong>Start Date:</strong> {forecastData.dates[0]}</p>
              <p><strong>End Date:</strong> {forecastData.dates[forecastData.dates.length - 1]}</p>
            </div>
            
            <div className="forecast-chart">
              <h4>Predicted Yield Values</h4>
              <div className="chart-container">
                {forecastData.predictions.map((value, index) => (
                  <div key={index} className="chart-bar">
                    <div 
                      className="bar" 
                      style={{ 
                        height: `${(value / Math.max(...forecastData.predictions)) * 100}%`,
                        backgroundColor: '#4CAF50'
                      }}
                    ></div>
                    <span className="bar-label">{formatNumber(value)}</span>
                    <span className="date-label">{forecastData.dates[index]}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="forecast-stats">
              <div className="stat-card">
                <h4>Average Predicted Yield</h4>
                <p className="stat-value">
                  {formatNumber(forecastData.predictions.reduce((a, b) => a + b, 0) / forecastData.predictions.length)}
                </p>
              </div>
              <div className="stat-card">
                <h4>Maximum Predicted Yield</h4>
                <p className="stat-value">{formatNumber(Math.max(...forecastData.predictions))}</p>
              </div>
              <div className="stat-card">
                <h4>Minimum Predicted Yield</h4>
                <p className="stat-value">{formatNumber(Math.min(...forecastData.predictions))}</p>
              </div>
            </div>
          </div>
        )}

        {/* History Tab */}
        {activeTab === "history" && historyData && (
          <div className="results-section">
            <h3 className="results-title">📊 {selectedCrop} Historical Data</h3>
            <div className="history-info">
              <p><strong>Period:</strong> Last {historyData.period_days} days</p>
              <p><strong>Data Points:</strong> {historyData.values.length}</p>
            </div>

            <div className="history-chart">
              <h4>Historical Yield Values</h4>
              <div className="chart-container">
                {historyData.values.slice(-30).map((value, index) => (
                  <div key={index} className="chart-bar">
                    <div 
                      className="bar" 
                      style={{ 
                        height: `${(value / Math.max(...historyData.values.slice(-30))) * 100}%`,
                        backgroundColor: '#2196F3'
                      }}
                    ></div>
                    <span className="bar-label">{formatNumber(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="history-stats">
              <div className="stat-card">
                <h4>Average Historical Yield</h4>
                <p className="stat-value">
                  {formatNumber(historyData.values.reduce((a, b) => a + b, 0) / historyData.values.length)}
                </p>
              </div>
              <div className="stat-card">
                <h4>Maximum Historical Yield</h4>
                <p className="stat-value">{formatNumber(Math.max(...historyData.values))}</p>
              </div>
              <div className="stat-card">
                <h4>Minimum Historical Yield</h4>
                <p className="stat-value">{formatNumber(Math.min(...historyData.values))}</p>
              </div>
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === "performance" && performanceData && (
          <div className="results-section">
            <h3 className="results-title">📈 {selectedCrop} Model Performance</h3>
            
            <div className="performance-metrics">
              <div className="metric-card">
                <h4>Root Mean Square Error (RMSE)</h4>
                <p className="metric-value">{formatNumber(performanceData.rmse)}</p>
                <p className="metric-desc">Lower is better</p>
              </div>
              <div className="metric-card">
                <h4>Mean Absolute Error (MAE)</h4>
                <p className="metric-value">{formatNumber(performanceData.mae)}</p>
                <p className="metric-desc">Lower is better</p>
              </div>
              <div className="metric-card">
                <h4>R² Score</h4>
                <p className="metric-value">{formatNumber(performanceData.r2)}</p>
                <p className="metric-desc">Higher is better (0-1)</p>
              </div>
              <div className="metric-card">
                <h4>Test Samples</h4>
                <p className="metric-value">{performanceData.test_samples}</p>
                <p className="metric-desc">Number of test data points</p>
              </div>
            </div>

            <div className="performance-explanation">
              <h4>Performance Interpretation</h4>
              <ul>
                <li><strong>RMSE:</strong> {performanceData.rmse < 25 ? "Excellent" : performanceData.rmse < 35 ? "Good" : "Needs Improvement"}</li>
                <li><strong>R²:</strong> {performanceData.r2 > 0.8 ? "Excellent fit" : performanceData.r2 > 0.6 ? "Good fit" : "Poor fit"}</li>
                <li><strong>Model Quality:</strong> {performanceData.rmse < 25 && performanceData.r2 > 0.6 ? "High Quality" : "Medium Quality"}</li>
              </ul>
            </div>
          </div>
        )}

        {/* No data message */}
        {!loading && !errorMsg && !forecastData && !historyData && !performanceData && (
          <div className="no-data-section">
            <p>Select a crop and click on a tab to view data.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TimeSeriesPage;
