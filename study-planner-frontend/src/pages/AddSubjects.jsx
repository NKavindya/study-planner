import { useState, useEffect } from 'react';
import { getSubjects, deleteSubject } from '../api/subjects';
import SubjectForm from '../components/SubjectForm';
import './AddSubjects.css';

const AddSubjects = () => {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const data = await getSubjects();
      setSubjects(data);
    } catch (err) {
      console.error('Failed to fetch subjects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this subject?')) {
      try {
        await deleteSubject(id);
        fetchSubjects();
      } catch (err) {
        alert('Failed to delete subject');
      }
    }
  };

  const handleFormSuccess = () => {
    fetchSubjects();
    setShowForm(false);
  };

  if (loading) {
    return <div className="loading">Loading subjects...</div>;
  }

  return (
    <div className="add-subjects">
      <div className="page-header">
        <h1>Manage Subjects</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Hide Form' : '+ Add New Subject'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Add New Subject</h2>
          <SubjectForm onSuccess={handleFormSuccess} />
        </div>
      )}

      <div className="card">
        <h2>All Subjects ({subjects.length})</h2>
        {subjects.length === 0 ? (
          <p>No subjects added yet. Add your first subject above!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Subject Name</th>
                <th>Difficulty</th>
                <th>Recommended Hours</th>
                <th>Past Assignments</th>
                <th>Questionnaire Results</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {subjects.map(subject => (
                <tr key={subject.id}>
                  <td>{subject.name}</td>
                  <td>
                    <span className={`badge badge-${subject.difficulty}`}>
                      {subject.difficulty}
                    </span>
                  </td>
                  <td>{subject.recommended_hours}h</td>
                  <td>
                    {subject.past_assignments && subject.past_assignments.length > 0 ? (
                      <ul style={{ margin: 0, paddingLeft: '20px' }}>
                        {subject.past_assignments.map((item, idx) => (
                          <li key={idx}>{item.name}: {item.result}</li>
                        ))}
                      </ul>
                    ) : 'N/A'}
                  </td>
                  <td>
                    {subject.questionnaire_results && subject.questionnaire_results.length > 0 ? (
                      <ul style={{ margin: 0, paddingLeft: '20px' }}>
                        {subject.questionnaire_results.map((item, idx) => (
                          <li key={idx}>{item.name}: {item.result}</li>
                        ))}
                      </ul>
                    ) : 'N/A'}
                  </td>
                  <td>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(subject.id)}
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

export default AddSubjects;
