import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAssignments } from '../api/assignments';
import { getExams } from '../api/exams';
import { generatePlan } from '../api/plan';
import './GeneratePlan.css';

const GeneratePlan = () => {
  const navigate = useNavigate();
  const [assignments, setAssignments] = useState([]);
  const [exams, setExams] = useState([]);
  const [formData, setFormData] = useState({
    available_hours_per_day: 3,
    start_date: new Date().toISOString().split('T')[0]
    // end_date will be auto-calculated from latest assignment/exam deadline
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [assignmentsData, examsData] = await Promise.all([
        getAssignments().catch(() => []),
        getExams().catch(() => [])
      ]);
      setAssignments(assignmentsData || []);
      setExams(examsData || []);
    } catch (err) {
      console.error('Failed to fetch data:', err);
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

    if (assignments.length === 0 && exams.length === 0) {
      setError('Please add at least one assignment or exam before generating a plan.');
      setLoading(false);
      return;
    }

    try {
      const data = await generatePlan(formData);
      setResult(data);
      console.log('Plan generated successfully:', data);
      // Show success message and suggest viewing the plan
      if (data && data.plan && data.plan.length > 0) {
        console.log(`Generated plan has ${data.plan.length} days`);
      }
    } catch (err) {
      console.error('Error generating plan:', err);
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
              <small style={{ color: '#666', fontSize: '12px' }}>
                End date will be automatically calculated from your latest assignment or exam deadline
              </small>
            </div>
          </div>

          {error && <div className="alert alert-warning">{error}</div>}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || (assignments.length === 0 && exams.length === 0)}
          >
            {loading ? 'Generating...' : 'Generate Study Plan'}
          </button>
        </form>
      </div>

      {assignments.length === 0 && exams.length === 0 && (
        <div className="alert alert-info">
          Please add assignments or exams first before generating a plan.
        </div>
      )}

      {(assignments.length > 0 || exams.length > 0) && (
        <div className="alert alert-info">
          <p>You have {assignments.length} assignment(s) and {exams.length} exam(s).</p>
          <p>The scheduler will automatically extend the plan until the latest assignment due date or exam date.</p>
          <p>Assignments will be prioritized before their due dates, then time will be allocated for exam preparation.</p>
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
            <p>Study plan generated successfully!</p>
            <p>Plans saved: Check the backend console for details.</p>
            <p>Go to the "View Plan" page to see your schedule.</p>
            <button 
              className="btn btn-primary" 
              onClick={() => navigate('/view-plan')}
              style={{ marginTop: '10px' }}
            >
              View Plan Now
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GeneratePlan;

