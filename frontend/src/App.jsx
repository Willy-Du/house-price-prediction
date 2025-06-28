import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    LotArea: '',
    OverallQual: '',
    YearBuilt: '',
    Neighborhood: '',
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setPrediction(null);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          LotArea: Number(formData.LotArea),
          OverallQual: Number(formData.OverallQual),
          YearBuilt: Number(formData.YearBuilt),
          Neighborhood: formData.Neighborhood,
        }),
      });

      if (!res.ok) {
        throw new Error('Prediction failed');
      }

      const data = await res.json();
      setPrediction(data.estimated_price);
    } catch (err) {
      setError('Could not get prediction. Check backend is running and input is valid.');
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>🏡 House Price Estimator</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Lot Area:</label>
          <input type="number" name="LotArea" value={formData.LotArea} onChange={handleChange} required />
        </div>
        <div>
          <label>Overall Quality (1-10):</label>
          <input type="number" name="OverallQual" value={formData.OverallQual} onChange={handleChange} required />
        </div>
        <div>
          <label>Year Built:</label>
          <input type="number" name="YearBuilt" value={formData.YearBuilt} onChange={handleChange} required />
        </div>
        <div>
          <label>Neighborhood:</label>
          <input type="text" name="Neighborhood" value={formData.Neighborhood} onChange={handleChange} required />
        </div>
        <button type="submit" style={{ marginTop: 10 }}>Estimate Price</button>
      </form>

      {prediction && (
        <div style={{ marginTop: 20, fontSize: 18 }}>
          Estimated price: <strong>${prediction.toLocaleString()}</strong>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default App;