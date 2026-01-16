import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useSocket } from '../../context/SocketContext';
import { getProfilePictureUrl } from '../../utils/profileHelpers';
import './Navbar.css';

const Navbar = () => {
  const { user, isAuthenticated, logout, isAdmin, isManager } = useAuth();
  const { notifications } = useSocket();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          ✈️ Flight Booking
        </Link>

        <div className="navbar-menu">
          {isAuthenticated() ? (
            <>
              <Link to="/flights" className="navbar-link">
                Flights
              </Link>

              {isManager() && (
                <Link to="/manager" className="navbar-link">
                  Manager Dashboard
                </Link>
              )}

              {isAdmin() && (
                <>
                  <Link to="/admin" className="navbar-link">
                    Admin Dashboard
                  </Link>
                  {notifications.length > 0 && (
                    <div className="notification-badge">
                      {notifications.length}
                    </div>
                  )}
                </>
              )}

              <Link to="/profile" className="navbar-link">
                Profile
              </Link>

              <div className="navbar-user">
                <img
                  src={getProfilePictureUrl(user?.profile_picture)}
                  alt="Profile"
                  className="navbar-avatar"
                />
                <div className="navbar-user-info">
                  <span className="user-name">
                    {user?.first_name} {user?.last_name}
                  </span>
                  <span className="user-role">{user?.role}</span>
                </div>
              </div>

              <button onClick={handleLogout} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Login
              </Link>
              <Link to="/register">
                <button className="btn btn-primary">Register</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
