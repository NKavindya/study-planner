import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import AddSubjects from './pages/AddSubjects';
import AddAssignments from './pages/AddAssignments';
import AddExams from './pages/AddExams';
import GeneratePlan from './pages/GeneratePlan';
import ViewPlan from './pages/ViewPlan';
import Settings from './pages/Settings';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/add-subjects" element={<AddSubjects />} />
            <Route path="/add-assignments" element={<AddAssignments />} />
            <Route path="/add-exams" element={<AddExams />} />
            <Route path="/generate-plan" element={<GeneratePlan />} />
            <Route path="/view-plan" element={<ViewPlan />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

