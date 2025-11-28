import React, { useState } from "react";
import FormPage from "./FormPage";
import TimeSeriesPage from "./TimeSeriesPage";
import './FormPage.css';

function App() {
  const [activePage, setActivePage] = useState("prediction");

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="nav-bar">
        <div className="nav-container">
          <h1 className="nav-title">🌱 AgriYield Predictor</h1>
          <div className="nav-buttons">
            <button 
              className={`nav-button ${activePage === "prediction" ? "active" : ""}`}
              onClick={() => setActivePage("prediction")}
            >
              🚀 Yield Prediction
            </button>
            <button 
              className={`nav-button ${activePage === "timeseries" ? "active" : ""}`}
              onClick={() => setActivePage("timeseries")}
            >
              📈 Time Series Analysis
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {activePage === "prediction" && <FormPage />}
        {activePage === "timeseries" && <TimeSeriesPage />}
      </main>
    </div>
  );
}

export default App;
