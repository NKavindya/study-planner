import { useState } from 'react';
import { trainModel } from '../api/ml';
import './Settings.css';

const Settings = () => {
  const [training, setTraining] = useState(false);
  const [message, setMessage] = useState(null);

  const handleTrainModel = async () => {
    setTraining(true);
    setMessage(null);
    try {
      const result = await trainModel();
      setMessage({ type: 'success', text: result.message || 'Model trained successfully!' });
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to train model' });
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="settings">
      <h1>Settings</h1>

      <div className="card">
        <h2>ML Model</h2>
        <p>Train or retrain the machine learning model used for predicting study hours.</p>
        <button
          className="btn btn-primary"
          onClick={handleTrainModel}
          disabled={training}
        >
          {training ? 'Training...' : 'Train Model'}
        </button>
        {message && (
          <div className={`alert alert-${message.type === 'success' ? 'success' : 'warning'}`}>
            {message.text}
          </div>
        )}
      </div>

      <div className="card">
        <h2>About</h2>
        <p><strong>Intelligent Study Planner</strong> uses:</p>
        <ul>
          <li>Rule-based logic for clash detection and scheduling</li>
          <li>Machine Learning (Linear Regression) for predicting study hours</li>
          <li>15+ intelligent rules for optimal schedule generation</li>
        </ul>
      </div>

      <div className="card">
        <h2>Command Interface</h2>
        <p>You can interact with the planner using the following commands:</p>
        <div className="command-list">
          <div className="command-item">
            <code>add subject</code>
            <span>Add a new subject to your study plan</span>
          </div>
          <div className="command-item">
            <code>generate plan</code>
            <span>Generate a new study schedule</span>
          </div>
          <div className="command-item">
            <code>view plan</code>
            <span>View your current study schedule</span>
          </div>
          <div className="command-item">
            <code>clear plan</code>
            <span>Clear your current study plan</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;

