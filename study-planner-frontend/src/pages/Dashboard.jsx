import { useState, useEffect } from 'react';
import { getSubjects } from '../api/subjects';
import { getExams } from '../api/exams';
import { getAssignments } from '../api/assignments';
import { getWeeklyPlan } from '../api/plan';
import ReminderBanner from '../components/ReminderBanner';
import { getDaysUntil } from '../utils/helpers';
import './Dashboard.css';

const Dashboard = () => {
  const [subjects, setSubjects] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [exams, setExams] = useState([]);
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalSubjects: 0,
    upcomingExams: 0,
    upcomingAssignments: 0
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [subjectsData, examsData, assignmentsData, planData] = await Promise.all([
        getSubjects(),
        getExams().catch(() => []),
        getAssignments().catch(() => []),
        getWeeklyPlan().catch(() => [])
      ]);
      setSubjects(subjectsData);
      setExams(examsData || []);
      setAssignments(assignmentsData || []);
      setPlan(planData || []);

      // Calculate stats based on exams and assignments
      const today = new Date();
      const upcomingExams = (examsData || []).filter(exam => {
        const days = getDaysUntil(exam.exam_date);
        return days >= 0 && days <= 7;
      }).length;

      const upcomingAssignments = (assignmentsData || []).filter(assgn => {
        const days = getDaysUntil(assgn.due_date);
        return days >= 0 && days <= 7;
      }).length;

      setStats({
        totalSubjects: subjectsData.length,
        upcomingExams,
        upcomingAssignments
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
          <h3>{stats.upcomingAssignments}</h3>
          <p>Upcoming Assignments (7 days)</p>
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
                <th>Recommended Hours</th>
                <th>Past Assignments</th>
                <th>Questionnaire Results</th>
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
                  <td>{subject.recommended_hours}h</td>
                  <td>
                    {subject.past_assignments && subject.past_assignments.length > 0 ? (
                      <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px' }}>
                        {subject.past_assignments.slice(0, 2).map((item, idx) => (
                          <li key={idx}>{item.name}: {item.result}</li>
                        ))}
                      </ul>
                    ) : 'N/A'}
                  </td>
                  <td>
                    {subject.questionnaire_results && subject.questionnaire_results.length > 0 ? (
                      <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px' }}>
                        {subject.questionnaire_results.slice(0, 2).map((item, idx) => (
                          <li key={idx}>{item.name}: {item.result}</li>
                        ))}
                      </ul>
                    ) : 'N/A'}
                  </td>
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
