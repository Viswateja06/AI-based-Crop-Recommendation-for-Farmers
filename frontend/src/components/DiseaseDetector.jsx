import React, { useState } from 'react';
import { detectDisease } from '../services/api';
import { UploadCloud, CheckCircle } from 'lucide-react';

const DiseaseDetector = ({ t }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    try {
      const data = await detectDisease(selectedFile);
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ error: "Failed to analyze image." });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 md:p-8 rounded-xl shadow-lg border border-green-50 mt-8">
      <h2 className="text-2xl font-bold text-green-800 mb-6 flex items-center">
        <UploadCloud className="mr-3 text-green-600" size={32} />
        {t.diseaseTitle}
      </h2>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-green-300 rounded-xl bg-green-50 hover:bg-green-100 transition-colors">
          {preview ? (
            <img src={preview} alt="Crop Preview" className="w-full max-h-64 rounded-lg object-contain mb-4" />
          ) : (
            <div className="text-center py-12">
              <UploadCloud className="mx-auto h-12 w-12 text-green-400 mb-4" />
              <p className="text-sm text-gray-600">Click to upload a leaf image</p>
            </div>
          )}
          
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange} 
            className="w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-green-50 file:text-green-700
              hover:file:bg-green-100"
          />
        </div>

        <div className="flex flex-col justify-center">
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isAnalyzing}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed mb-6"
          >
            {isAnalyzing ? "Analyzing Request..." : "Detect Disease"}
          </button>

          {result && !result.error && (
            <div className="bg-white border border-green-200 rounded-lg p-5 shadow-sm">
              <h3 className="text-lg font-bold text-green-800 mb-4 flex items-center">
                <CheckCircle className="mr-2 text-green-500" size={20} />
                Analysis Complete
              </h3>
              <div className="space-y-3 text-sm">
                <p><span className="font-semibold text-gray-700">Condition:</span> <span className="text-red-600 font-medium">{result.disease}</span></p>
                <p><span className="font-semibold text-gray-700">Treatment:</span> {result.treatment}</p>
                <p><span className="font-semibold text-gray-700">Suggested Pesticide:</span> {result.pesticide}</p>
              </div>
            </div>
          )}

          {result && result.error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
              {result.error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiseaseDetector;
