import axios from 'axios';

const API_BASE_URL = '/api';

export const chatWithBot = async (query, lang) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat/`, { query, lang });
    return response.data;
  } catch (error) {
    console.error("Error communicating with Chatbot:", error);
    return { response: "Sorry, I am having trouble connecting to the server right now." };
  }
};

export const detectDisease = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post(`${API_BASE_URL}/disease/detect`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error("Error detecting disease:", error);
    throw error;
  }
};

export const getWeather = async (city) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/weather/`, { params: { city } });
    return response.data;
  } catch (error) {
    console.error("Error fetching weather:", error);
    throw error;
  }
};

export const recommendCrop = async (soilData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/recommend/`, soilData);
    return response.data;
  } catch (error) {
    console.error("Error fetching crop recommendation:", error);
    throw error;
  }
};
