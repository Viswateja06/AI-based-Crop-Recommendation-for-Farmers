import React, { useState } from 'react';
import { Leaf, Menu, X } from 'lucide-react';

const Navbar = ({ setActiveTab, language, setLanguage, t }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    setIsOpen(false);
  };

  return (
    <nav className="bg-green-700 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Leaf className="h-8 w-8 mr-2 text-green-300" />
            <span className="font-bold text-2xl tracking-tight">GreenPulse India</span>
          </div>
          
          <div className="flex items-center sm:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-green-100 hover:text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            >
              {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
            </button>
          </div>

          <div className="hidden sm:flex sm:items-center sm:space-x-4">
            <button onClick={() => handleTabClick('dashboard')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none">{t.dashboard}</button>
            <button onClick={() => handleTabClick('chatbot')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none">{t.aiChat}</button>
            <button onClick={() => handleTabClick('disease')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none">{t.diseaseDetect}</button>
            <button onClick={() => handleTabClick('recommendation')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none">{t.cropRec}</button>
            <div className="pl-2 border-l border-green-500">
               <select 
                 value={language} 
                 onChange={(e) => setLanguage(e.target.value)}
                 className="bg-green-700 text-sm font-medium text-white border-0 outline-none focus:ring-0 cursor-pointer"
               >
                  <option value="en">English</option>
                  <option value="hi">हिंदी (Hindi)</option>
                  <option value="kn">ಕನ್ನಡ (Kannada)</option>
                  <option value="ml">മലയാളം (Malayalam)</option>
                  <option value="mr">मराठी (Marathi)</option>
                  <option value="or">ଓଡ଼ିଆ (Odia)</option>
                  <option value="ta">தமிழ் (Tamil)</option>
                  <option value="te">తెలుగు (Telugu)</option>
               </select>
            </div>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="sm:hidden bg-green-800 border-t border-green-600 animate-in slide-in-from-top-2">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <button onClick={() => handleTabClick('dashboard')} className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white hover:bg-green-600 transition focus:outline-none">{t.dashboard}</button>
            <button onClick={() => handleTabClick('chatbot')} className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white hover:bg-green-600 transition focus:outline-none">{t.aiChat}</button>
            <button onClick={() => handleTabClick('disease')} className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white hover:bg-green-600 transition focus:outline-none">{t.diseaseDetect}</button>
            <button onClick={() => handleTabClick('recommendation')} className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white hover:bg-green-600 transition focus:outline-none">{t.cropRec}</button>
            <div className="px-3 py-2 border-t border-green-600 mt-2">
               <select 
                 value={language} 
                 onChange={(e) => setLanguage(e.target.value)}
                 className="w-full bg-green-700 text-base font-medium text-white border border-green-600 rounded-md p-2 outline-none focus:ring-0 cursor-pointer"
               >
                  <option value="en">English</option>
                  <option value="hi">हिंदी (Hindi)</option>
                  <option value="kn">ಕನ್ನಡ (Kannada)</option>
                  <option value="ml">മലയാളം (Malayalam)</option>
                  <option value="mr">मराठी (Marathi)</option>
                  <option value="or">ଓଡ଼ିଆ (Odia)</option>
                  <option value="ta">தமிழ் (Tamil)</option>
                  <option value="te">తెలుగు (Telugu)</option>
               </select>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
