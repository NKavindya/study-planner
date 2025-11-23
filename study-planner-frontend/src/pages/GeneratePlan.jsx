import { useState, useEffect } from 'react';
import { getSubjects } from '../api/subjects';
import { generatePlan } from '../api/plan';
import './GeneratePlan.css';

const GeneratePlan = () => {
  const [subjects, setSubjects] = useState([]);
  const [formData, setFormData] = useState({
    available_hours_per_day: 3,
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
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
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    if (subjects.length === 0) {
      setError('Please add at least one subject before generating a plan.');
      setLoading(false);
      return;
    }

    try {
      const data = await generatePlan(formData);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generate-plan">
      <h1>Generate Study Plan</h1>

      <div className="card">
        <h2>Your Availability</h2>
        <form onSubmit={handleGenerate}>
          <div className="form-row">
            <div className="input-group">
              <label>Available Hours Per Day *</label>
              <input
                type="number"
                name="available_hours_per_day"
                value={formData.available_hours_per_day}
                onChange={handleChange}
                min="1"
                max="12"
                step="0.5"
                required
              />
            </div>

            <div className="input-group">
              <label>Start Date *</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="input-group">
              <label>End Date *</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {error && <div className="alert alert-warning">{error}</div>}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || subjects.length === 0}
          >
            {loading ? 'Generating...' : 'Generate Study Plan'}
          </button>
        </form>
      </div>

      {subjects.length === 0 && (
        <div className="alert alert-info">
          Please add subjects first before generating a plan.
        </div>
      )}

      {result && (
        <div className="card">
          <h2>Plan Generation Results</h2>
          
          {result.clashes && result.clashes.length > 0 && (
            <div className="alert alert-warning">
              <strong>Clashes Detected:</strong>
              <ul>
                {result.clashes.map((clash, idx) => (
                  <li key={idx}>{clash}</li>
                ))}
              </ul>
            </div>
          )}

          {result.rules_triggered && result.rules_triggered.length > 0 && (
            <div className="alert alert-info">
              <strong>Rules Applied:</strong>
              <ul>
                {result.rules_triggered.slice(0, 10).map((rule, idx) => (
                  <li key={idx}>{rule}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="plan-stats">
            <p><strong>Total Hours Needed:</strong> {result.total_hours_needed?.toFixed(1)}h</p>
            <p><strong>Total Available Hours:</strong> {result.total_available_hours?.toFixed(1)}h</p>
          </div>

          <div className="alert alert-success">
            Study plan generated successfully! Check the "View Plan" page to see your schedule.
          </div>
        </div>
      )}
    </div>
  );
};

export default GeneratePlan;

