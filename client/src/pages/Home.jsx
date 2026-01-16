import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1 className="hero-title">Welcome to Flight Booking System</h1>
        <p className="hero-subtitle">
          Book your flights easily and efficiently with our distributed system
        </p>

        {!isAuthenticated() ? (
          <div className="hero-actions">
            <Link to="/register">
              <button className="btn btn-primary btn-large">
                Get Started
              </button>
            </Link>
            <Link to="/login">
              <button className="btn btn-secondary btn-large">
                Login
              </button>
            </Link>
          </div>
        ) : (
          <div className="hero-actions">
            <Link to="/flights">
              <button className="btn btn-primary btn-large">
                Browse Flights
              </button>
            </Link>
          </div>
        )}
      </div>

      <div className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">✈️</div>
            <h3>Easy Booking</h3>
            <p>Book flights with just a few clicks and secure payment</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⏱️</div>
            <h3>Real-time Updates</h3>
            <p>Track your flight status in real-time with live updates</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">💳</div>
            <h3>Secure Payments</h3>
            <p>Safe and secure payment processing with account balance</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⭐</div>
            <h3>Rate Flights</h3>
            <p>Share your experience and rate completed flights</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🛠️</div>
            <h3>Admin Dashboard</h3>
            <p>Comprehensive management tools for administrators</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📅</div>
            <h3>Flight Management</h3>
            <p>Managers can create and manage flight schedules</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
