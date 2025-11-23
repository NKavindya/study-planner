import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/ml';

export const trainModel = async () => {
  const response = await axios.post(`${API_BASE_URL}/train`);
  return response.data;
};

export const predictHours = async (pastScore, difficulty, chapters, daysLeft) => {
  const response = await axios.post(`${API_BASE_URL}/predict`, null, {
    params: {
      past_score: pastScore,
      difficulty: difficulty,
      chapters: chapters,
      days_left: daysLeft
    }
  });
  return response.data;
};

