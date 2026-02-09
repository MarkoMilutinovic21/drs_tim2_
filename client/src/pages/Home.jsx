import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const features = [
  {
    id: '01',
    title: 'Easy Booking',
    description: 'Book flights in a few steps with clear status and pricing.'
  },
  {
    id: '02',
    title: 'Real-time Updates',
    description: 'Track flight changes and booking progress without page refresh.'
  },
  {
    id: '03',
    title: 'Secure Payments',
    description: 'Manage account balance with safe payment and booking processing.'
  },
  {
    id: '04',
    title: 'Flight Ratings',
    description: 'Rate completed flights and review experience after each trip.'
  },
  {
    id: '05',
    title: 'Admin Control',
    description: 'Approve requests, manage users, and monitor platform activity.'
  },
  {
    id: '06',
    title: 'Manager Tools',
    description: 'Create and maintain flight schedules with role-based access.'
  }
];

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-page">
      <section className="home-hero">
        <p className="home-eyebrow">Distributed Flight Platform</p>
        <h1 className="hero-title">Welcome to Flight Booking System</h1>
        <p className="hero-subtitle">
          Book flights easily and efficiently with real-time updates and role-based workflows.
        </p>

        {!isAuthenticated() ? (
          <div className="hero-actions">
            <Link to="/register">
              <button className="home-btn home-btn-primary">Get Started</button>
            </Link>
            <Link to="/login">
              <button className="home-btn home-btn-secondary">Login</button>
            </Link>
          </div>
        ) : (
          <div className="hero-actions">
            <Link to="/flights">
              <button className="home-btn home-btn-primary">Browse Flights</button>
            </Link>
          </div>
        )}
      </section>

      <section className="features-section">
        <h2>Platform Features</h2>
        <div className="features-grid">
          {features.map((feature) => (
            <article key={feature.id} className="feature-card">
              <span className="feature-tag">{feature.id}</span>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;
