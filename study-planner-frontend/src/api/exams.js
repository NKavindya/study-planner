import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/exams';

export const getExams = async () => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

export const createExam = async (examData) => {
  const response = await axios.post(API_BASE_URL, examData);
  return response.data;
};

export const updateExam = async (id, examData) => {
  const response = await axios.put(`${API_BASE_URL}/${id}`, examData);
  return response.data;
};

export const deleteExam = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/${id}`);
  return response.data;
};


