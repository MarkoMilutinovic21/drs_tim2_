import { createContext, useState, useEffect, useContext } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {   {/*definise sta cuva sve*/}
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Ucita korisnika ako postoji token
  useEffect(() => {
    if (token) {
      loadUser();
    } else {
      setLoading(false);  // niko nije ulogovan
    }
  }, [token]);

  // Listen for role updates from other tabs (admin role change)
  // ako admin azurira role da se i u drugom tabu azurira 
  useEffect(() => {
    const handleStorage = (event) => {
      if (event.key !== 'roleUpdate' || !event.newValue) return;
      try {
        const payload = JSON.parse(event.newValue);
        if (payload?.userId && user?.id === payload.userId) {
          loadUser();
        }
      } catch (err) {
        // ignore invalid payload
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, [user]);

  // Refresh user on focus/visibility change and periodically
  useEffect(() => {
    if (!token) return undefined;

    const handleFocus = () => {
      loadUser();
    };

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        loadUser();
      }
    };

    window.addEventListener('focus', handleFocus);
    document.addEventListener('visibilitychange', handleVisibility);

    const interval = setInterval(() => {
      loadUser();
    }, 20000);    // svakih 20s

    return () => {
      window.removeEventListener('focus', handleFocus);
      document.removeEventListener('visibilitychange', handleVisibility);
      clearInterval(interval);
    };
  }, [token]);

  const loadUser = async () => {    // ucitava korisnika sa servera 
    try {
      const response = await authAPI.getCurrentUser();
      setUser(response.data.user);    // OVDE PAMTI KORISNIKA
    } catch (error) {
      console.error('Failed to load user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token); // trajno u browseru sacuva token
      setToken(access_token); // zapamti token u react stanju
      setUser(user);          // zapamti korisnika
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || error.response?.data?.errors || 'Registration failed'
      };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token'); // uklanja token 
      setToken(null);
      setUser(null);
    }
  };

  // POMOCNE FUKCIJE
  const isAuthenticated = () => {
    return !!token && !!user;
  };

  const hasRole = (role) => {
    return user?.role === role;
  };

  const isAdmin = () => {
    return user?.role === 'ADMINISTRATOR';
  };

  const isManager = () => {
    return user?.role === 'MANAGER';
  };

  const isRegularUser = () => {
    return user?.role === 'KORISNIK';
  };


  // OVO SLUZI ZA DELJENJE SA DRUGIM KOMPONENTAMA - ono sta auth radi 
  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
    hasRole,
    isAdmin,
    isManager,
    isRegularUser,
    refreshUser: loadUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// const { user, isAdmin, login, logout } = useAuth();
// svaka komponenta moze koristiti liniju iznad da pristupi podatcima o korisniku
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
