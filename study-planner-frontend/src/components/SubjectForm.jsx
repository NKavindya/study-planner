import { useState } from 'react';
import { createSubject } from '../api/subjects';
import './SubjectForm.css';

const SubjectForm = ({ onSuccess, initialData = null }) => {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    difficulty: initialData?.difficulty || 'medium',
    past_assignments: initialData?.past_assignments || [],
    questionnaire_results: initialData?.questionnaire_results || []
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAddAssignment = () => {
    setFormData(prev => ({
      ...prev,
      past_assignments: [...prev.past_assignments, { name: '', result: '' }]
    }));
  };

  const handleRemoveAssignment = (index) => {
    setFormData(prev => ({
      ...prev,
      past_assignments: prev.past_assignments.filter((_, i) => i !== index)
    }));
  };

  const handleAssignmentChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      past_assignments: prev.past_assignments.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const handleAddQuestionnaire = () => {
    setFormData(prev => ({
      ...prev,
      questionnaire_results: [...prev.questionnaire_results, { name: '', result: '' }]
    }));
  };

  const handleRemoveQuestionnaire = (index) => {
    setFormData(prev => ({
      ...prev,
      questionnaire_results: prev.questionnaire_results.filter((_, i) => i !== index)
    }));
  };

  const handleQuestionnaireChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      questionnaire_results: prev.questionnaire_results.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
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
        past_assignments: [],
        questionnaire_results: []
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create subject');
      console.error('Error:', err);
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

        <div className="form-section">
          <div className="section-header">
            <h3>Past Assignments</h3>
            <button type="button" className="btn btn-secondary" onClick={handleAddAssignment}>
              + Add Assignment
            </button>
          </div>
          {formData.past_assignments.map((assignment, index) => (
            <div key={index} className="form-row assignment-row">
              <div className="input-group">
                <label>Assignment Name</label>
                <input
                  type="text"
                  value={assignment.name}
                  onChange={(e) => handleAssignmentChange(index, 'name', e.target.value)}
                  placeholder="e.g., Assignment 1"
                />
              </div>
              <div className="input-group">
                <label>Result</label>
                <input
                  type="text"
                  value={assignment.result}
                  onChange={(e) => handleAssignmentChange(index, 'result', e.target.value)}
                  placeholder="e.g., 85%"
                />
              </div>
              <button
                type="button"
                className="btn btn-danger"
                onClick={() => handleRemoveAssignment(index)}
              >
                Remove
              </button>
            </div>
          ))}
        </div>

        <div className="form-section">
          <div className="section-header">
            <h3>Questionnaire Results</h3>
            <button type="button" className="btn btn-secondary" onClick={handleAddQuestionnaire}>
              + Add Result
            </button>
          </div>
          {formData.questionnaire_results.map((questionnaire, index) => (
            <div key={index} className="form-row questionnaire-row">
              <div className="input-group">
                <label>Name (e.g., Mid Exam, Quiz)</label>
                <input
                  type="text"
                  value={questionnaire.name}
                  onChange={(e) => handleQuestionnaireChange(index, 'name', e.target.value)}
                  placeholder="e.g., Mid Exam"
                />
              </div>
              <div className="input-group">
                <label>Result</label>
                <input
                  type="text"
                  value={questionnaire.result}
                  onChange={(e) => handleQuestionnaireChange(index, 'result', e.target.value)}
                  placeholder="e.g., 78%"
                />
              </div>
              <button
                type="button"
                className="btn btn-danger"
                onClick={() => handleRemoveQuestionnaire(index)}
              >
                Remove
              </button>
            </div>
          ))}
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
