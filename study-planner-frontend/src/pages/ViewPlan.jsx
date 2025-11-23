import { useState, useEffect } from 'react';
import { getWeeklyPlan, clearPlan } from '../api/plan';
import StudyPlanTable from '../components/StudyPlanTable';
import Loader from '../components/Loader';
import './ViewPlan.css';

const ViewPlan = () => {
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getWeeklyPlan();
      if (data && Array.isArray(data)) {
        setPlan(data);
      } else {
        setPlan([]);
      }
    } catch (err) {
      console.error('Error fetching plan:', err);
      setError(err.response?.data?.detail || 'Failed to load study plan. Please generate a plan first.');
      setPlan([]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear the study plan?')) {
      try {
        await clearPlan();
        fetchPlan();
      } catch (err) {
        alert('Failed to clear plan');
      }
    }
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="view-plan">
      <div className="page-header">
        <h1>View Study Plan</h1>
        {plan.length > 0 && (
          <button className="btn btn-danger" onClick={handleClear}>
            Clear Plan
          </button>
        )}
      </div>

      {error && <div className="alert alert-warning">{error}</div>}

      <div className="card">
        <StudyPlanTable plan={plan} />
      </div>

      {plan.length > 0 && (
        <div className="card">
          <h3>Plan Summary</h3>
          <p>Your study plan has been generated and optimized using AI rules and ML predictions.</p>
          <p>You can regenerate a new plan anytime from the "Generate Plan" page.</p>
        </div>
      )}
    </div>
  );
};

export default ViewPlan;

