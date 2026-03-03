import React, { useState } from 'react';
import { recommendCrop } from '../services/api';
import { Sprout, Droplets, ThermometerSun } from 'lucide-react';

const CropRecommendation = ({ t }) => {
  const [formData, setFormData] = useState({
    N: '', P: '', K: '', temperature: '', humidity: '', ph: '', rainfall: ''
  });
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    const processedData = {};
    for (const key in formData) {
      processedData[key] = parseFloat(formData[key]) || 0;
    }

    try {
      const data = await recommendCrop(processedData);
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ error: "Failed to get recommendation." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 md:p-8 rounded-xl shadow-lg border border-green-50 mt-8 mb-16">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-green-800 inline-flex items-center">
          <Sprout className="mr-3 text-green-500" size={36} />
          {t.cropTitle}
        </h2>
        <p className="text-gray-600 mt-2">Enter your soil and weather parameters to get AI-driven advice.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-10">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nitrogen (N) <br/><span className="text-xs text-gray-400">0 - 140</span></label>
              <input type="number" name="N" value={formData.N} onChange={handleChange} min="0" max="140" placeholder="e.g. 90" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phosphorus (P) <br/><span className="text-xs text-gray-400">5 - 145</span></label>
              <input type="number" name="P" value={formData.P} onChange={handleChange} min="5" max="145" placeholder="e.g. 42" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Potassium (K) <br/><span className="text-xs text-gray-400">5 - 205</span></label>
              <input type="number" name="K" value={formData.K} onChange={handleChange} min="5" max="205" placeholder="e.g. 43" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center"><ThermometerSun size={16} className="mr-1 text-orange-500"/> Temp (°C) <span className="ml-1 text-xs text-gray-400">8 - 45</span></label>
              <input type="number" step="0.1" name="temperature" value={formData.temperature} onChange={handleChange} min="8" max="45" placeholder="e.g. 20.8" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center"><Droplets size={16} className="mr-1 text-blue-500"/> Humidity (%) <span className="ml-1 text-xs text-gray-400">14 - 100</span></label>
              <input type="number" step="0.1" name="humidity" value={formData.humidity} onChange={handleChange} min="14" max="100" placeholder="e.g. 82" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Soil pH <span className="ml-1 text-xs text-gray-400">3.5 - 9.9</span></label>
              <input type="number" step="0.1" name="ph" value={formData.ph} onChange={handleChange} min="3.5" max="9.9" placeholder="e.g. 6.5" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center"><Droplets size={16} className="mr-1 text-blue-400"/> Rainfall (mm) <span className="ml-1 text-xs text-gray-400">20 - 298</span></label>
              <input type="number" step="0.1" name="rainfall" value={formData.rainfall} onChange={handleChange} min="20" max="298" placeholder="e.g. 202.9" required className="w-full border border-gray-300 rounded-md p-2 focus:ring-green-500 focus:border-green-500" />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg shadow-md transition-colors disabled:opacity-50 mt-4"
          >
            {isLoading ? "Running AI Models..." : "Get Recommendation"}
          </button>
        </form>

        <div className="bg-green-50 rounded-xl p-6 border border-green-100 flex items-center justify-center">
          {!result ? (
            <div className="text-center text-gray-500">
              <Sprout size={48} className="mx-auto text-green-300 mb-3 opacity-50" />
              <p>Submit your parameters to see AI recommendations here.</p>
            </div>
          ) : result.error ? (
             <div className="text-red-500 text-center">{result.error}</div>
          ) : (
            <div className="w-full space-y-6">
              <div className="bg-white p-5 rounded-lg shadow-sm border border-green-200 text-center">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Recommended Crop</h3>
                <p className="text-3xl font-bold text-green-700 capitalize">{result.recommended_crop}</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm border border-blue-200 text-center">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Fertilizer Suggestion</h3>
                <p className="text-lg font-medium text-blue-700">{result.fertilizer_suggestion}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CropRecommendation;
