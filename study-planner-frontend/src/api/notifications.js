import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/notifications';

export const getNotifications = async (unreadOnly = false) => {
  const response = await axios.get(API_BASE_URL, {
    params: { unread_only: unreadOnly }
  });
  return response.data;
};

export const getUnreadCount = async () => {
  const response = await axios.get(`${API_BASE_URL}/unread/count`);
  return response.data;
};

export const markNotificationRead = async (id) => {
  const response = await axios.post(`${API_BASE_URL}/${id}/read`);
  return response.data;
};

export const markAllNotificationsRead = async () => {
  const response = await axios.post(`${API_BASE_URL}/read-all`);
  return response.data;
};

export const deleteNotification = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/${id}`);
  return response.data;
};


