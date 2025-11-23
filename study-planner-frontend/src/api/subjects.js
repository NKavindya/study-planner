import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/subjects';

export const getSubjects = async () => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

export const createSubject = async (subjectData) => {
  const response = await axios.post(API_BASE_URL, subjectData);
  return response.data;
};

export const updateSubject = async (id, subjectData) => {
  const response = await axios.put(`${API_BASE_URL}/${id}`, subjectData);
  return response.data;
};

export const deleteSubject = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/${id}`);
  return response.data;
};

export const getActiveReminders = async () => {
  const response = await axios.get(`${API_BASE_URL}/reminders/active`);
  return response.data;
};

