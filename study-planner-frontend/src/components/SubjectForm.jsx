import { useState } from 'react';
import { createSubject } from '../api/subjects';
import './SubjectForm.css';

const SubjectForm = ({ onSuccess, initialData = null }) => {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    difficulty: initialData?.difficulty || 'medium',
    exam_date: initialData?.exam_date || '',
    past_score: initialData?.past_score || 0,
    chapters: initialData?.chapters || 0,
    has_assignment: initialData?.has_assignment || false,
    has_exam: initialData?.has_exam || true,
    last_week_hours: initialData?.last_week_hours || 0
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createSubject(formData);
      if (onSuccess) onSuccess();
      // Reset form
      setFormData({
        name: '',
        difficulty: 'medium',
        exam_date: '',
        past_score: 0,
        chapters: 0,
        has_assignment: false,
        has_exam: true,
        last_week_hours: 0
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create subject');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="subject-form">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="input-group">
            <label>Subject Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="e.g., Mathematics"
            />
          </div>

          <div className="input-group">
            <label>Difficulty *</label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
              required
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label>Exam Date *</label>
            <input
              type="date"
              name="exam_date"
              value={formData.exam_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Past Score (0-100)</label>
            <input
              type="number"
              name="past_score"
              value={formData.past_score}
              onChange={handleChange}
              min="0"
              max="100"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label>Number of Chapters</label>
            <input
              type="number"
              name="chapters"
              value={formData.chapters}
              onChange={handleChange}
              min="0"
            />
          </div>

          <div className="input-group">
            <label>Hours Studied Last Week</label>
            <input
              type="number"
              name="last_week_hours"
              value={formData.last_week_hours}
              onChange={handleChange}
              min="0"
              step="0.5"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="input-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="has_assignment"
                checked={formData.has_assignment}
                onChange={handleChange}
              />
              Has Assignment
            </label>
          </div>

          <div className="input-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="has_exam"
                checked={formData.has_exam}
                onChange={handleChange}
              />
              Has Exam
            </label>
          </div>
        </div>

        {error && <div className="alert alert-warning">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save Subject'}
        </button>
      </form>
    </div>
  );
};

export default SubjectForm;

