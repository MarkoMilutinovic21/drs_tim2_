import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { userAPI, bookingAPI } from '../services/api';
import { formatDate, formatCurrency, formatDateTime, getStatusBadgeClass, formatBookingStatus } from '../utils/formatters';
import { validatePositiveNumber } from '../utils/validators';
import './Profile.css';

const Profile = () => {
  const { user, refreshUser } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [showAddBalanceModal, setShowAddBalanceModal] = useState(false);
  const [balanceAmount, setBalanceAmount] = useState('');

  useEffect(() => {
    loadUserBookings();
  }, [user]);

  const loadUserBookings = async () => {
    try {
      setLoading(true);
      const response = await bookingAPI.getUserBookings(user.id);
      setBookings(response.data.bookings);
    } catch (err) {
      console.error('Failed to load bookings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddBalance = async () => {
    setError('');
    setSuccessMessage('');

    const validation = validatePositiveNumber(balanceAmount, 'Amount');
    if (!validation.valid) {
      setError(validation.message);
      return;
    }

    try {
      await userAPI.addBalance(user.id, parseFloat(balanceAmount));
      setSuccessMessage(`Successfully added $${balanceAmount} to your account`);
      setShowAddBalanceModal(false);
      setBalanceAmount('');
      await refreshUser();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add balance');
    }
  };

  return (
    <div className="profile-page">
      <div className="page-header">
        <h1>My Profile</h1>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={() => setError('')} className="alert-close">×</button>
        </div>
      )}

      {successMessage && (
        <div className="alert alert-success">
          {successMessage}
          <button onClick={() => setSuccessMessage('')} className="alert-close">×</button>
        </div>
      )}

      <div className="profile-grid">
        {/* User Info Card */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Personal Information</h2>
          </div>
          <div className="profile-info">
            <div className="info-row">
              <span className="info-label">Name:</span>
              <span className="info-value">{user.first_name} {user.last_name}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Email:</span>
              <span className="info-value">{user.email}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Date of Birth:</span>
              <span className="info-value">{formatDate(user.date_of_birth)}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Gender:</span>
              <span className="info-value">{user.gender}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Address:</span>
              <span className="info-value">
                {user.street} {user.street_number}, {user.country}
              </span>
            </div>
            <div className="info-row">
              <span className="info-label">Role:</span>
              <span className="info-value">
                <span className="badge badge-info">{user.role}</span>
              </span>
            </div>
          </div>
        </div>

        {/* Balance Card */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Account Balance</h2>
          </div>
          <div className="balance-content">
            <div className="balance-amount">
              ${formatCurrency(user.account_balance)}
            </div>
            <button
              className="btn btn-primary"
              onClick={() => setShowAddBalanceModal(true)}
            >
              Add Balance
            </button>
          </div>
        </div>
      </div>

      {/* Bookings Section */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">My Bookings</h2>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div className="spinner"></div>
          </div>
        ) : bookings.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--secondary-color)' }}>
            No bookings yet
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Flight</th>
                  <th>Route</th>
                  <th>Departure</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Booked At</th>
                </tr>
              </thead>
              <tbody>
                {bookings.map((booking) => (
                  <tr key={booking.id}>
                    <td>{booking.flight?.name || 'N/A'}</td>
                    <td>
                      {booking.flight?.departure_airport || 'N/A'} → {booking.flight?.arrival_airport || 'N/A'}
                    </td>
                    <td>{formatDateTime(booking.flight?.departure_time)}</td>
                    <td>${formatCurrency(booking.ticket_price)}</td>
                    <td>
                      <span className={`badge ${getStatusBadgeClass(booking.status)}`}>
                        {formatBookingStatus(booking.status)}
                      </span>
                    </td>
                    <td>{formatDateTime(booking.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Balance Modal */}
      {showAddBalanceModal && (
        <div className="modal-overlay" onClick={() => setShowAddBalanceModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Add Balance</h2>
              <button className="modal-close" onClick={() => setShowAddBalanceModal(false)}>
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Amount ($)</label>
                <input
                  type="number"
                  className="form-input"
                  value={balanceAmount}
                  onChange={(e) => setBalanceAmount(e.target.value)}
                  placeholder="Enter amount"
                  min="0.01"
                  step="0.01"
                />
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowAddBalanceModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleAddBalance}>
                Add Balance
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;