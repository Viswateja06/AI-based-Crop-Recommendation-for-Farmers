import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Chatbot from './components/Chatbot';
import DiseaseDetector from './components/DiseaseDetector';
import AdvisoryDashboard from './components/AdvisoryDashboard';
import CropRecommendation from './components/CropRecommendation';
import { Leaf, Award, Globe, Shield } from 'lucide-react';
import { translations } from './translations';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [language, setLanguage] = useState('en');

  const t = translations[language];

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
      default:
        return (
          <>
            <AdvisoryDashboard t={t} />
            <div className="max-w-4xl mx-auto my-12 bg-green-50 rounded-2xl p-8 border border-green-100 shadow-sm text-center">
               <h2 className="text-3xl font-bold text-green-900 mb-6">{t.empowering}</h2>
               <div className="grid md:grid-cols-3 gap-8">
                  <div className="flex flex-col items-center">
                    <div className="bg-white p-4 rounded-full shadow-sm mb-4 text-green-600"><Leaf size={32} /></div>
                    <h3 className="font-bold text-lg text-gray-800">{t.smartCropTracking}</h3>
                    <p className="text-gray-600 mt-2 text-sm">{t.dataDrivenRecommendations}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="bg-white p-4 rounded-full shadow-sm mb-4 text-green-600"><Shield size={32} /></div>
                    <h3 className="font-bold text-lg text-gray-800">{t.diseaseDefense}</h3>
                    <p className="text-gray-600 mt-2 text-sm">{t.instantDiagnosis}</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="bg-white p-4 rounded-full shadow-sm mb-4 text-green-600"><Globe size={32} /></div>
                    <h3 className="font-bold text-lg text-gray-800">{t.globalTechLocalNeeds}</h3>
                    <p className="text-gray-600 mt-2 text-sm">{t.accessibleInsights}</p>
                  </div>
               </div>
            </div>
          </>
        );
      case 'chatbot':
        return (
          <div className="py-12">
            <h1 className="text-3xl font-bold text-center text-green-800 mb-8">{t.chatbotTitle}</h1>
            <Chatbot t={t} language={language} />
          </div>
        );
      case 'disease':
        return <DiseaseDetector t={t} />;
      case 'recommendation':
        return <CropRecommendation t={t} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#f0fdf4] font-sans pb-12">
      <Navbar setActiveTab={setActiveTab} language={language} setLanguage={setLanguage} t={t} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        {renderContent()}
      </main>

      <footer className="mt-20 border-t border-green-200 py-8 text-center text-green-800 bg-green-50">
        <p className="font-medium flex items-center justify-center">
          <Award size={20} className="mr-2" />
          AI-Based Crop Recommendations for Farmers
        </p>
        <p className="text-sm text-green-600 mt-2">&copy; 2026 Academic Project</p>
      </footer>
    </div>
  );
}

export default App;
