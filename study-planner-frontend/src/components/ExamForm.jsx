import { useState, useEffect } from 'react';
import { createExam } from '../api/exams';
import { getSubjects } from '../api/subjects';
import './ExamForm.css';

const ExamForm = ({ onSuccess, initialData = null }) => {
  const [subjects, setSubjects] = useState([]);
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    subject_name: initialData?.subject_name || '',
    exam_date: initialData?.exam_date || '',
    difficulty: initialData?.difficulty || 'medium',
    past_score: initialData?.past_score || 0,
    chapters: initialData?.chapters || 0
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
        setFormData((prev) => ({
            ...prev,
            [name]:
                type === "number"
                    ? parseFloat(value) || 0
                    : isNaN(parseInt(value))
                        ? value
                        : parseInt(value) || 0,
        }));
    };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createExam(formData);
      if (onSuccess) onSuccess();
      // Reset form
      setFormData({
        name: '',
        subject_name: '',
        exam_date: '',
        difficulty: 'medium',
        past_score: 0,
        chapters: 0
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create exam');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="exam-form">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="input-group">
            <label>Exam Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="e.g., Midterm Exam"
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
        </div>

        <div className="form-row">
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
        </div>

        {error && <div className="alert alert-warning">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save Exam'}
        </button>
      </form>
    </div>
  );
};

export default ExamForm;


