import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/planner';

export const generatePlan = async (planData) => {
  const response = await axios.post(`${API_BASE_URL}/generate`, planData);
  return response.data;
};

export const getWeeklyPlan = async () => {
  const response = await axios.get(`${API_BASE_URL}/weekly`);
  return response.data;
};

export const clearPlan = async () => {
  const response = await axios.delete(`${API_BASE_URL}/clear`);
  return response.data;
};

