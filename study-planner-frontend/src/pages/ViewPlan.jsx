import { useState, useEffect } from 'react';
import { getWeeklyPlan, clearPlan } from '../api/plan';
import Calendar from '../components/Calendar';
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
      console.log('Fetched plan data:', data);
      if (data && Array.isArray(data)) {
        console.log(`Plan has ${data.length} days`);
        data.forEach((day, idx) => {
          console.log(`Day ${idx}: ${day.day} has ${day.time_slots?.length || 0} slots`);
        });
        setPlan(data);
      } else {
        console.log('Plan data is not an array:', data);
        setPlan([]);
      }
    } catch (err) {
      console.error('Error fetching plan:', err);
      console.error('Error details:', err.response?.data);
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
        <div>
          <button className="btn btn-secondary" onClick={fetchPlan} style={{ marginRight: '8px' }}>
            Refresh
          </button>
          {plan.length > 0 && (
            <button className="btn btn-danger" onClick={handleClear}>
              Clear Plan
            </button>
          )}
        </div>
      </div>

      {error && <div className="alert alert-warning">{error}</div>}

      {plan.length === 0 && !error && (
        <div className="alert alert-info">
          <p>No study plan found. Please generate a plan first.</p>
          <p>Make sure you have added assignments or exams before generating a plan.</p>
        </div>
      )}

      <div className="card" style={{ padding: 0 }}>
        <Calendar plan={plan} />
      </div>

      {/* Debug info - remove in production */}
      {/*{process.env.NODE_ENV === 'development' && plan.length > 0 && (*/}
      {/*  <div className="card" style={{ marginTop: '20px', fontSize: '12px', background: '#f8f9fa' }}>*/}
      {/*    <h4>Debug Info</h4>*/}
      {/*    <pre>{JSON.stringify(plan, null, 2)}</pre>*/}
      {/*  </div>*/}
      {/*)}*/}

      {plan.length > 0 && (
        <div className="card">
          <h3>Plan Summary</h3>
          <p>Your study plan has been generated and optimized using AI rules and ML predictions.</p>
          <p>The scheduler prioritizes assignments before their due dates, then allocates time for exam preparation.</p>
          <p>You can regenerate a new plan anytime from the "Generate Plan" page.</p>
        </div>
      )}
    </div>
  );
};

export default ViewPlan;

