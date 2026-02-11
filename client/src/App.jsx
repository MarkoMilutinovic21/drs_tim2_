import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { SocketProvider } from './context/SocketContext';
import ProtectedRoute from './components/Common/ProtectedRoute';
import Navbar from './components/Common/Navbar';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Flights from './pages/Flights';
import Profile from './pages/Profile';
import AdminDashboard from './pages/AdminDashboard';
import ManagerDashboard from './pages/ManagerDashboard';

const AppShell = () => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';

  return (
    <div className="app">
      <Navbar />
      <main className={`main-content ${isAuthPage ? 'main-content-auth' : ''}`}> {/*ako je ulogovan dodaj mu main content auth*/}
        <div key={location.pathname} className="route-transition"> {/*react ga koristi za promenu ruta kao animaciju neku nesto */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes - korisnik mora biti ulogovan/odredjen role za upotrebu odredjenih resursa*/}
            {/* tipa admin ce imati admin stranicu...*/}
            <Route
              path="/flights"
              element={
                <ProtectedRoute>
                  <Flights />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute requiredRole="ADMINISTRATOR">
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/manager"
              element={
                <ProtectedRoute requiredRole="MANAGER">
                  <ManagerDashboard />
                </ProtectedRoute>
              }
            />

            {/* Catch all - ako se ne poklapa sa nekom od prethodno navedenih ruta, samo idi na pocetnu str*/}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

// omotac ovi unutar imaju pristup spoljasnjima
function App() {  
  return (
    <Router>
      <AuthProvider>
        <SocketProvider>
          <AppShell />
        </SocketProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
