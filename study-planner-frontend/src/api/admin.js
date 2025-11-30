import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/admin';

export const clearAllData = async () => {
  const response = await axios.delete(`${API_BASE_URL}/clear-all`);
  return response.data;
};

