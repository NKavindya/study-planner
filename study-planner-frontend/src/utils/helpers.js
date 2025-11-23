export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

export const getDaysUntil = (examDate) => {
  if (!examDate) return 999;
  const today = new Date();
  const exam = new Date(examDate);
  const diffTime = exam - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};

export const getPriorityColor = (priority) => {
  const colors = {
    urgent: '#ff4757',
    high: '#ff6348',
    medium: '#ffa502',
    low: '#2ed573'
  };
  return colors[priority] || '#6c757d';
};

