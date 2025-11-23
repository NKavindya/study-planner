import { useState, useEffect } from 'react';
import { getExams, deleteExam } from '../api/exams';
import ExamForm from '../components/ExamForm';
import { formatDate, getDaysUntil } from '../utils/helpers';
import './AddExams.css';

const AddExams = () => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      const data = await getExams();
      setExams(data);
    } catch (err) {
      console.error('Failed to fetch exams:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this exam?')) {
      try {
        await deleteExam(id);
        fetchExams();
      } catch (err) {
        alert('Failed to delete exam');
      }
    }
  };

  const handleFormSuccess = () => {
    fetchExams();
    setShowForm(false);
  };

  if (loading) {
    return <div className="loading">Loading exams...</div>;
  }

  return (
    <div className="add-exams">
      <div className="page-header">
        <h1>Manage Exams</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Hide Form' : '+ Add New Exam'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Add New Exam</h2>
          <ExamForm onSuccess={handleFormSuccess} />
        </div>
      )}

      <div className="card">
        <h2>All Exams ({exams.length})</h2>
        {exams.length === 0 ? (
          <p>No exams added yet. Add your first exam above!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Exam</th>
                <th>Subject</th>
                <th>Exam Date</th>
                <th>Days Left</th>
                <th>Difficulty</th>
                <th>Chapters</th>
                <th>Past Score</th>
                <th>Recommended Hours</th>
                <th>Priority</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {exams.map(exam => (
                <tr key={exam.id}>
                  <td>{exam.name}</td>
                  <td>{exam.subject_name}</td>
                  <td>{formatDate(exam.exam_date)}</td>
                  <td>{getDaysUntil(exam.exam_date)} days</td>
                  <td>
                    <span className={`badge badge-${exam.difficulty}`}>
                      {exam.difficulty}
                    </span>
                  </td>
                  <td>{exam.chapters}</td>
                  <td>{exam.past_score}%</td>
                  <td>{exam.recommended_hours}h</td>
                  <td>
                    <span className={`badge badge-${exam.priority}`}>
                      {exam.priority}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(exam.id)}
                    >
                      Delete
                    </button>
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

export default AddExams;


