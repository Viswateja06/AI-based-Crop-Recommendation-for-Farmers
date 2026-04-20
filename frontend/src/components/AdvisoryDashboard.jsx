import React, { useState, useEffect, useRef } from 'react';
import { getWeather } from '../services/api';
import { CloudRain, Sun, Thermometer, Wind, AlertTriangle, CloudSun, MapPin, Search } from 'lucide-react';
import { allDistricts } from '../data/locations';

const AdvisoryDashboard = ({ t }) => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [city, setCity] = useState('Hyderabad');
  const [showDropdown, setShowDropdown] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const dropdownRef = useRef(null);

  const fetchWeather = async (cityName) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getWeather(cityName);
      setWeatherData(data);
    } catch (err) {
      console.error("Weather fetch failed:", err);
      setError("Failed to fetch weather data. Please try again or check your connection.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;

    const initWeather = () => {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            if (!mounted) return;
            try {
              const { latitude, longitude } = position.coords;
              const res = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`);
              if (res.ok) {
                const data = await res.json();
                const detectedCity = data.city || data.locality || "Hyderabad";
                setCity(detectedCity);
                fetchWeather(detectedCity);
              } else {
                fetchWeather(city);
              }
            } catch (e) {
              fetchWeather(city);
            }
          },
          (error) => {
            console.warn("Geolocation error:", error.message);
            if (mounted) fetchWeather(city);
          },
          { timeout: 5000 } // Stop waiting for geolocation after 5 seconds to prevent infinite load
        );
      } else {
        fetchWeather(city);
      }
    };

    initWeather();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleCityChange = (e) => {
    e.preventDefault();
    fetchWeather(city);
    setShowDropdown(false);
  };

  const handleSelectCity = (selectedCity) => {
    setCity(selectedCity);
    setSearchTerm('');
    setShowDropdown(false);
    fetchWeather(selectedCity);
  };

  const filteredDistricts = allDistricts.filter(d => 
    d.toLowerCase().includes(searchTerm.toLowerCase()) || 
    d.toLowerCase().includes(city.toLowerCase())
  ).slice(0, 50); // Limit to 50 results for performance

  const getWeatherIcon = (temp, rain) => {
    if (rain > 50) return <CloudRain className="text-blue-500 w-16 h-16" />;
    if (temp > 35) return <Sun className="text-yellow-500 w-16 h-16" />;
    return <CloudSun className="text-gray-400 w-16 h-16" />;
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow border border-green-50 mt-8 mb-8">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-green-800 flex items-center">
          <CloudSun className="mr-3 text-green-600" size={28} />
          {t.weatherAdvisory}
        </h2>
        <form onSubmit={handleCityChange} className="flex mt-4 md:mt-0 relative" ref={dropdownRef}>
          <div className="relative flex">
            <input 
              type="text" 
              value={city} 
              onChange={(e) => {
                setCity(e.target.value);
                setSearchTerm(e.target.value);
                setShowDropdown(true);
              }} 
              onFocus={() => setShowDropdown(true)}
              placeholder={t.enterCity} 
              className="border border-gray-300 rounded-l-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-green-500 w-48 sm:w-64"
            />
            <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-r-md text-sm hover:bg-green-700 transition">{t.update}</button>
          </div>
          
          {showDropdown && (
            <div className="absolute top-full mt-1 w-full bg-white border border-green-200 rounded-md shadow-lg max-h-60 overflow-y-auto z-50">
              <div className="p-2 sticky top-0 bg-gray-50 border-b border-gray-200">
                <div className="relative">
                   <Search size={16} className="absolute left-2 top-2.5 text-gray-400" />
                   <input
                     type="text"
                     placeholder={t.searchDistrict}
                     value={searchTerm}
                     onChange={(e) => setSearchTerm(e.target.value)}
                     className="w-full pl-8 pr-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-green-500"
                   />
                </div>
              </div>
              <ul className="py-1">
                {filteredDistricts.length > 0 ? (
                  filteredDistricts.map((district, index) => (
                    <li 
                      key={index}
                      onClick={() => handleSelectCity(district)}
                      className="px-3 py-2 text-sm hover:bg-green-50 cursor-pointer flex items-center text-gray-700"
                    >
                      <MapPin size={14} className="mr-2 text-green-500" />
                      {district}
                    </li>
                  ))
                ) : (
                  <li className="px-3 py-2 text-sm text-gray-500 text-center">{t.noLocationsFound}</li>
                )}
              </ul>
            </div>
          )}
        </form>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
      ) : error ? (
        <div className="text-red-500 bg-red-50 p-4 rounded-md text-center">{error}</div>
      ) : weatherData && (
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-1 bg-gradient-to-br from-blue-50 text-blue-900 border border-blue-100 p-6 rounded-xl flex flex-col items-center justify-center text-center shadow-sm">
            {getWeatherIcon(weatherData.temperature, weatherData.rainfall)}
            <h3 className="text-3xl font-bold mt-4">{weatherData.temperature}°C</h3>
            <p className="text-sm font-medium uppercase tracking-wider text-blue-700 mt-1">{weatherData.city}</p>
          </div>
          
          <div className="md:col-span-2 grid grid-cols-2 gap-4">
             <div className="bg-white border border-gray-100 shadow-sm p-4 rounded-xl flex items-center space-x-4">
               <div className="bg-orange-100 p-3 rounded-full text-orange-600">
                  <Thermometer size={24} />
               </div>
               <div>
                  <p className="text-xs text-gray-500 uppercase tracking-widest font-semibold">{t.temperature}</p>
                  <p className="text-xl font-bold text-gray-800">{weatherData.temperature}°C</p>
               </div>
             </div>
             
             <div className="bg-white border border-gray-100 shadow-sm p-4 rounded-xl flex items-center space-x-4">
               <div className="bg-blue-100 p-3 rounded-full text-blue-600">
                  <Wind size={24} />
               </div>
               <div>
                  <p className="text-xs text-gray-500 uppercase tracking-widest font-semibold">{t.humidity}</p>
                  <p className="text-xl font-bold text-gray-800">{weatherData.humidity}%</p>
               </div>
             </div>

             <div className="bg-white border border-gray-100 shadow-sm p-4 rounded-xl flex items-center space-x-4">
               <div className="bg-cyan-100 p-3 rounded-full text-cyan-600">
                  <CloudRain size={24} />
               </div>
               <div>
                  <p className="text-xs text-gray-500 uppercase tracking-widest font-semibold">{t.rainfall}</p>
                  <p className="text-xl font-bold text-gray-800">{weatherData.rainfall} mm</p>
               </div>
             </div>
             
             <div className={`col-span-1 sm:col-span-2 shadow-sm p-5 rounded-xl border flex items-start space-x-4 ${
                weatherData.advisory.includes('alert') || weatherData.advisory.includes('risk') ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'
             }`}>
               <AlertTriangle className={`mt-0.5 ${weatherData.advisory.includes('alert') ? 'text-red-500' : 'text-green-600'}`} size={24} />
               <div>
                  <p className={`text-xs uppercase tracking-widest font-bold mb-1 ${weatherData.advisory.includes('alert') ? 'text-red-700' : 'text-green-800'}`}>{t.aiAdvisory}</p>
                  <p className={`text-sm md:text-base font-medium ${weatherData.advisory.includes('alert') ? 'text-red-900' : 'text-green-900'}`}>{weatherData.advisory}</p>
               </div>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvisoryDashboard;
