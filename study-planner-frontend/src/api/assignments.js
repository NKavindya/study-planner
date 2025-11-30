import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/assignments';

export const getAssignments = async () => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

export const createAssignment = async (assignmentData) => {
  const response = await axios.post(API_BASE_URL, assignmentData);
  return response.data;
};

export const updateAssignment = async (id, assignmentData) => {
  const response = await axios.put(`${API_BASE_URL}/${id}`, assignmentData);
  return response.data;
};

export const deleteAssignment = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/${id}`);
  return response.data;
};


