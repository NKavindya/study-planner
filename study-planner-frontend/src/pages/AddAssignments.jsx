import { useState, useEffect } from 'react';
import { getAssignments, deleteAssignment } from '../api/assignments';
import AssignmentForm from '../components/AssignmentForm';
import { formatDate, getDaysUntil } from '../utils/helpers';
import './AddAssignments.css';

const AddAssignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    try {
      const data = await getAssignments();
      setAssignments(data);
    } catch (err) {
      console.error('Failed to fetch assignments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this assignment?')) {
      try {
        await deleteAssignment(id);
        fetchAssignments();
      } catch (err) {
        alert('Failed to delete assignment');
      }
    }
  };

  const handleFormSuccess = () => {
    fetchAssignments();
    setShowForm(false);
  };

  if (loading) {
    return <div className="loading">Loading assignments...</div>;
  }

  return (
    <div className="add-assignments">
      <div className="page-header">
        <h1>Manage Assignments</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Hide Form' : '+ Add New Assignment'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Add New Assignment</h2>
          <AssignmentForm onSuccess={handleFormSuccess} />
        </div>
      )}

      <div className="card">
        <h2>All Assignments ({assignments.length})</h2>
        {assignments.length === 0 ? (
          <p>No assignments added yet. Add your first assignment above!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Assignment</th>
                <th>Subject</th>
                <th>Due Date</th>
                <th>Days Left</th>
                <th>Estimated Hours</th>
                <th>Difficulty</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {assignments.map(assignment => (
                <tr key={assignment.id}>
                  <td>{assignment.name}</td>
                  <td>{assignment.subject_name}</td>
                  <td>{formatDate(assignment.due_date)}</td>
                  <td>{getDaysUntil(assignment.due_date)} days</td>
                  <td>{assignment.estimated_hours}h</td>
                  <td>
                    <span className={`badge badge-${assignment.difficulty}`}>
                      {assignment.difficulty}
                    </span>
                  </td>
                  <td>
                    <span className={`badge badge-${assignment.priority}`}>
                      {assignment.priority}
                    </span>
                  </td>
                  <td>
                    <span className={`badge badge-${assignment.status}`}>
                      {assignment.status}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(assignment.id)}
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

export default AddAssignments;


