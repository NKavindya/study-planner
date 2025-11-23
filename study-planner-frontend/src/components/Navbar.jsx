import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h2>📚 Intelligent Study Planner</h2>
        </div>
        <div className="navbar-links">
          <Link to="/" className={isActive('/')}>
            Dashboard
          </Link>
          <Link to="/add-subjects" className={isActive('/add-subjects')}>
            Add Subjects
          </Link>
          <Link to="/generate-plan" className={isActive('/generate-plan')}>
            Generate Plan
          </Link>
          <Link to="/view-plan" className={isActive('/view-plan')}>
            View Plan
          </Link>
          <Link to="/settings" className={isActive('/settings')}>
            Settings
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

