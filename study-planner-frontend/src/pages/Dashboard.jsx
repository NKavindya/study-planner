import { useState, useEffect } from 'react';
import { getSubjects } from '../api/subjects';
import { getWeeklyPlan } from '../api/plan';
import ReminderBanner from '../components/ReminderBanner';
import { formatDate, getDaysUntil } from '../utils/helpers';
import './Dashboard.css';

const Dashboard = () => {
  const [subjects, setSubjects] = useState([]);
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalSubjects: 0,
    upcomingExams: 0,
    urgentSubjects: 0
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [subjectsData, planData] = await Promise.all([
        getSubjects(),
        getWeeklyPlan()
      ]);
      setSubjects(subjectsData);
      setPlan(planData);

      // Calculate stats
      const today = new Date();
      const upcomingExams = subjectsData.filter(subj => {
        const days = getDaysUntil(subj.exam_date);
        return days >= 0 && days <= 7;
      }).length;

      const urgentSubjects = subjectsData.filter(
        subj => subj.priority === 'urgent'
      ).length;

      setStats({
        totalSubjects: subjectsData.length,
        upcomingExams,
        urgentSubjects
      });
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <ReminderBanner />

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.totalSubjects}</h3>
          <p>Total Subjects</p>
        </div>
        <div className="stat-card">
          <h3>{stats.upcomingExams}</h3>
          <p>Upcoming Exams (7 days)</p>
        </div>
        <div className="stat-card">
          <h3>{stats.urgentSubjects}</h3>
          <p>Urgent Subjects</p>
        </div>
      </div>

      <div className="card">
        <h2>Recent Subjects</h2>
        {subjects.length === 0 ? (
          <p>No subjects added yet. Add subjects to get started!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Difficulty</th>
                <th>Exam Date</th>
                <th>Days Left</th>
                <th>Priority</th>
                <th>Recommended Hours</th>
              </tr>
            </thead>
            <tbody>
              {subjects.slice(0, 5).map(subject => (
                <tr key={subject.id}>
                  <td>{subject.name}</td>
                  <td>
                    <span className={`badge badge-${subject.difficulty}`}>
                      {subject.difficulty}
                    </span>
                  </td>
                  <td>{formatDate(subject.exam_date)}</td>
                  <td>{getDaysUntil(subject.exam_date)} days</td>
                  <td>
                    <span className={`badge badge-${subject.priority}`}>
                      {subject.priority}
                    </span>
                  </td>
                  <td>{subject.recommended_hours}h</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

