import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

// childeren - stranica koje je unutar njega npr flights
// requiredRole je uloga neophodna za pristup 
const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, hasRole, loading } = useAuth();

  if (loading) {                                // da li ucitava josuvek...
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated()) {                       // da li je ulogovan
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && !hasRole(requiredRole)) {   // provera uloge
    return <Navigate to="/flights" replace />;
  }

  return children;
};

export default ProtectedRoute;
