import { useState, useEffect } from 'react';
import { createAssignment } from '../api/assignments';
import { getSubjects } from '../api/subjects';
import './AssignmentForm.css';

const AssignmentForm = ({ onSuccess, initialData = null }) => {
  const [subjects, setSubjects] = useState([]);
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    subject_name: initialData?.subject_name || '',
    due_date: initialData?.due_date || '',
    estimated_hours: initialData?.estimated_hours || 0,
    difficulty: initialData?.difficulty || 'medium',
    status: initialData?.status || 'pending'
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const data = await getSubjects();
      setSubjects(data);
    } catch (err) {
      console.error('Failed to fetch subjects:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createAssignment(formData);
      if (onSuccess) onSuccess();
      // Reset form
      setFormData({
        name: '',
        subject_name: '',
        due_date: '',
        estimated_hours: 0,
        difficulty: 'medium',
        status: 'pending'
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create assignment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assignment-form">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="input-group">
            <label>Assignment Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="e.g., Research Paper"
            />
          </div>

          <div className="input-group">
            <label>Subject *</label>
            <select
              name="subject_name"
              value={formData.subject_name}
              onChange={handleChange}
              required
            >
              <option value="">Select a subject</option>
              {subjects.map(subject => (
                <option key={subject.id} value={subject.name}>
                  {subject.name}
                </option>
              ))}
            </select>
            {subjects.length === 0 && (
              <small>No subjects available. Please add subjects first.</small>
            )}
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label>Due Date *</label>
            <input
              type="date"
              name="due_date"
              value={formData.due_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Estimated Hours *</label>
            <input
              type="number"
              name="estimated_hours"
              value={formData.estimated_hours}
              onChange={handleChange}
              min="0"
              step="0.5"
              required
              placeholder="e.g., 5.5"
            />
            <small>How many hours do you estimate this assignment will take?</small>
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label>Difficulty</label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="input-group">
            <label>Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>

        {error && <div className="alert alert-warning">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save Assignment'}
        </button>
      </form>
    </div>
  );
};

export default AssignmentForm;


