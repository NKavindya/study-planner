import { useState, useEffect } from 'react';
import { getActiveReminders } from '../api/subjects';
import './ReminderBanner.css';

const ReminderBanner = () => {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReminders();
    const interval = setInterval(fetchReminders, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const fetchReminders = async () => {
    try {
      const data = await getActiveReminders();
      setReminders(data);
    } catch (err) {
      console.error('Failed to fetch reminders:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return null;

  if (reminders.length === 0) {
    return null;
  }

  return (
    <div className="reminder-banner">
      <h4>📢 Reminders</h4>
      <ul>
        {reminders.map(reminder => (
          <li key={reminder.id}>
            {reminder.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReminderBanner;

