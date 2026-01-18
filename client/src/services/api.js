import axios from 'axios';

const SERVER_URL = 'http://localhost:5000';
const FLIGHT_SERVICE_URL = 'http://localhost:5001';

// Create axios instance for Server
const serverAPI = axios.create({
  baseURL: SERVER_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Create axios instance for Flight Service
const flightServiceAPI = axios.create({
  baseURL: FLIGHT_SERVICE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
const addAuthToken = (config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

serverAPI.interceptors.request.use(addAuthToken);
flightServiceAPI.interceptors.request.use(addAuthToken);

// Handle 401 errors (unauthorized)
const handleUnauthorized = (error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }
  return Promise.reject(error);
};

serverAPI.interceptors.response.use((response) => response, handleUnauthorized);
flightServiceAPI.interceptors.response.use((response) => response, handleUnauthorized);

// ==================== AUTH API ====================
export const authAPI = {
  login: (email, password) =>
    serverAPI.post('/api/auth/login', { email, password }),
  
  register: (userData) =>
    serverAPI.post('/api/auth/register', userData),
  
  logout: () =>
    serverAPI.post('/api/auth/logout'),
  
  getCurrentUser: () =>
    serverAPI.get('/api/auth/me'),
  
  refreshToken: () =>
    serverAPI.post('/api/auth/refresh')
};

// ==================== USER API ====================
export const userAPI = {
  getAll: (page = 1, perPage = 20) =>
    serverAPI.get(`/api/users?page=${page}&per_page=${perPage}`),
  
  getById: (userId) =>
    serverAPI.get(`/api/users/${userId}`),
  
  update: (userId, userData) =>
    serverAPI.put(`/api/users/${userId}`, userData),
  
  delete: (userId) =>
    serverAPI.delete(`/api/users/${userId}`),
  
  changePassword: (userId, oldPassword, newPassword) =>
    serverAPI.put(`/api/users/${userId}/password`, {
      old_password: oldPassword,
      new_password: newPassword
    }),
  
  updateRole: (userId, newRole) =>
    serverAPI.put(`/api/users/${userId}/role`, { new_role: newRole }),
  
  addBalance: (userId, amount) =>
    serverAPI.post(`/api/users/${userId}/balance`, { amount }),
  
  uploadProfilePicture: (userId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return serverAPI.post(`/api/users/${userId}/profile-picture`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};

// ==================== AIRLINE API ====================
export const airlineAPI = {
  create: (airlineData) =>
    serverAPI.post('/api/airlines', airlineData),
  
  getAll: (activeOnly = true) =>
    serverAPI.get(`/api/airlines?active_only=${activeOnly}`),
  
  getById: (airlineId) =>
    serverAPI.get(`/api/airlines/${airlineId}`),
  
  update: (airlineId, airlineData) =>
    serverAPI.put(`/api/airlines/${airlineId}`, airlineData),
  
  delete: (airlineId) =>
    serverAPI.delete(`/api/airlines/${airlineId}`)
};

// ==================== FLIGHT API ====================
export const flightAPI = {
  create: (flightData) =>
    flightServiceAPI.post('/api/flights', flightData),
  
  getAll: (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.name) params.append('name', filters.name);
    if (filters.airline_id) params.append('airline_id', filters.airline_id);
    if (filters.status) params.append('status', filters.status);
    return flightServiceAPI.get(`/api/flights?${params.toString()}`);
  },
  
  getByTabs: () =>
    flightServiceAPI.get('/api/flights/tabs'),
  
  getPending: () =>
    flightServiceAPI.get('/api/flights/pending'),
  
  getById: (flightId) =>
    flightServiceAPI.get(`/api/flights/${flightId}`),
  
  approve: (flightId) =>
    flightServiceAPI.post(`/api/flights/${flightId}/approve`, { action: 'approve' }),
  
  reject: (flightId, reason) =>
    flightServiceAPI.post(`/api/flights/${flightId}/approve`, {
      action: 'reject',
      rejection_reason: reason
    }),
  
  update: (flightId, flightData) =>
    flightServiceAPI.put(`/api/flights/${flightId}`, flightData),
  
  cancel: (flightId) =>
    flightServiceAPI.post(`/api/flights/${flightId}/cancel`),
  
  delete: (flightId) =>
    flightServiceAPI.delete(`/api/flights/${flightId}`),

  generateReport: (reportType, adminId) =>
    flightServiceAPI.post('/api/flights/report', {
      report_type: reportType,
      admin_id: adminId
    })
};

// ==================== BOOKING API ====================
export const bookingAPI = {
  create: (flightId, userId) =>
    flightServiceAPI.post('/api/bookings', {
      flight_id: flightId,
      user_id: userId
    }),
  
  getById: (bookingId) =>
    flightServiceAPI.get(`/api/bookings/${bookingId}`),
  
  getUserBookings: (userId) =>
    flightServiceAPI.get(`/api/bookings/user/${userId}`),
  
  getFlightBookings: (flightId) =>
    flightServiceAPI.get(`/api/bookings/flight/${flightId}`)
};

// ==================== RATING API ====================
export const ratingAPI = {
  create: (flightId, userId, rating, comment = null) =>
    flightServiceAPI.post('/api/ratings', {
      flight_id: flightId,
      user_id: userId,
      rating,
      comment
    }),
  
  getById: (ratingId) =>
    flightServiceAPI.get(`/api/ratings/${ratingId}`),
  
  getFlightRatings: (flightId) =>
    flightServiceAPI.get(`/api/ratings/flight/${flightId}`),
  
  getAll: () =>
    flightServiceAPI.get('/api/ratings')
};

export default {
  authAPI,
  userAPI,
  airlineAPI,
  flightAPI,
  bookingAPI,
  ratingAPI
};
