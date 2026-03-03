import React from 'react';
import { Leaf } from 'lucide-react';

const Navbar = ({ setActiveTab, language, setLanguage, t }) => {
  return (
    <nav className="bg-green-700 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between h-auto sm:h-16 py-3 sm:py-0">
          <div className="flex items-center justify-center sm:justify-start">
            <Leaf className="h-8 w-8 mr-2 text-green-300" />
            <span className="font-bold text-2xl tracking-tight hidden sm:block">GreenPulse India</span>
            <span className="font-bold text-xl tracking-tight sm:hidden">GreenPulse India</span>
          </div>
          <div className="flex pt-4 sm:pt-0 items-center overflow-x-auto hide-scrollbar space-x-1 sm:space-x-4">
            <button onClick={() => setActiveTab('dashboard')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none whitespace-nowrap">{t.dashboard}</button>
            <button onClick={() => setActiveTab('chatbot')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none whitespace-nowrap">{t.aiChat}</button>
            <button onClick={() => setActiveTab('disease')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none whitespace-nowrap">{t.diseaseDetect}</button>
            <button onClick={() => setActiveTab('recommendation')} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-green-600 transition focus:outline-none whitespace-nowrap">{t.cropRec}</button>
            <div className="pl-2 border-l border-green-500">
               <select 
                 value={language} 
                 onChange={(e) => setLanguage(e.target.value)}
                 className="bg-green-700 text-sm font-medium text-white border-0 outline-none focus:ring-0 cursor-pointer"
               >
                  <option value="en">English</option>
                  <option value="hi">हिंदी (Hindi)</option>
                  <option value="te">తెలుగు (Telugu)</option>
               </select>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
