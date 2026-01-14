import { useState, useEffect } from 'react';
import { useSocket } from '../context/SocketContext';
import { flightAPI, ratingAPI, userAPI } from '../services/api';
import {
  formatDateTime,
  formatCurrency,
  formatFlightStatus,
  getStatusBadgeClass
} from '../utils/formatters';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [pendingFlights, setPendingFlights] = useState([]);
  const [approvedFlights, setApprovedFlights] = useState([]);
  const [ratings, setRatings] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [rejectionReason, setRejectionReason] = useState('');
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newRole, setNewRole] = useState('');

  const { notifications, removeNotification } = useSocket();

  useEffect(() => {
    loadData();
  }, []);

  // Reload pending flights when notification arrives
  useEffect(() => {
    if (notifications.length > 0) {
      loadPendingFlights();
    }
  }, [notifications]);

  const loadData = async () => {
    setLoading(true);
    await Promise.all([loadPendingFlights(), loadApprovedFlights(), loadUsers(), loadRatings()]);
    setLoading(false);
  };

  const loadPendingFlights = async () => {
    try {
      const response = await flightAPI.getPending();
      setPendingFlights(response.data.flights);
    } catch (err) {
      console.error('Failed to load pending flights:', err);
    }
  };

  const loadApprovedFlights = async () => {
    try {
      const response = await flightAPI.getAll({ status: 'APPROVED' });
      setApprovedFlights(response.data.flights);
    } catch (err) {
      console.error('Failed to load approved flights:', err);
    }
  };

  const loadRatings = async () => {
    try {
      const response = await ratingAPI.getAll();
      setRatings(response.data.ratings);
    } catch (err) {
      console.error('Failed to load ratings:', err);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await userAPI.getAll(1, 100);
      setUsers(response.data.users);
    } catch (err) {
      console.error('Failed to load users:', err);
    }
  };

  const handleApproveFlight = async (flightId) => {
    setError('');
    setSuccessMessage('');

    try {
      await flightAPI.approve(flightId);
      setSuccessMessage('Flight approved successfully');
      loadPendingFlights();
      loadApprovedFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to approve flight');
    }
  };

  const handleRejectFlight = async () => {
    if (!rejectionReason.trim()) {
      setError('Rejection reason is required');
      return;
    }

    setError('');
    setSuccessMessage('');

    try {
      await flightAPI.reject(selectedFlight.id, rejectionReason);
      setSuccessMessage('Flight rejected successfully');
      setShowRejectModal(false);
      setSelectedFlight(null);
      setRejectionReason('');
      loadPendingFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to reject flight');
    }
  };

  const handleCancelFlight = async (flightId) => {
    if (!window.confirm('Cancel this flight?')) {
      return;
    }

    setError('');
    setSuccessMessage('');

    try {
      await flightAPI.cancel(flightId);
      setSuccessMessage('Flight cancelled successfully');
      loadApprovedFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to cancel flight');
    }
  };

  const handleDeleteFlight = async (flightId) => {
    if (!window.confirm('Delete this flight?')) {
      return;
    }

    setError('');
    setSuccessMessage('');

    try {
      await flightAPI.delete(flightId);
      setSuccessMessage('Flight deleted successfully');
      loadApprovedFlights();
      loadPendingFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete flight');
    }
  };

  const openRejectModal = (flight) => {
    setSelectedFlight(flight);
    setShowRejectModal(true);
    setRejectionReason('');
  };

  const handleUpdateRole = async () => {
    if (!newRole) {
      setError('Please select a role');
      return;
    }

    setError('');
    setSuccessMessage('');

    try {
      await userAPI.updateRole(selectedUser.id, newRole);
      setSuccessMessage(`User role updated to ${newRole}`);
      setShowRoleModal(false);
      setSelectedUser(null);
      setNewRole('');
      loadUsers();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update role');
    }
  };

  const openRoleModal = (user) => {
    setSelectedUser(user);
    setNewRole(user.role);
    setShowRoleModal(true);
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    setError('');
    setSuccessMessage('');

    try {
      await userAPI.delete(userId);
      setSuccessMessage('User deleted successfully');
      loadUsers();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete user');
    }
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <p>Manage flights and users</p>
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

      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="notifications-panel">
          <h3>Recent Notifications ({notifications.length})</h3>
          <div className="notifications-list">
            {notifications.slice(0, 5).map((notif, index) => (
              <div key={index} className="notification-item">
                <span>{notif.message}</span>
                <button
                  className="notification-dismiss"
                  onClick={() => removeNotification(index)}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pending Flights */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Pending Flights ({pendingFlights.length})</h2>
        </div>

        {pendingFlights.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--secondary-color)' }}>
            No pending flights
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Route</th>
                  <th>Departure</th>
                  <th>Duration</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {pendingFlights.map((flight) => (
                  <tr key={flight.id}>
                    <td>{flight.name}</td>
                    <td>{flight.departure_airport} → {flight.arrival_airport}</td>
                    <td>{formatDateTime(flight.departure_time)}</td>
                    <td>{flight.duration_minutes} min</td>
                    <td>${formatCurrency(flight.ticket_price)}</td>
                    <td>
                      <span className={`badge ${getStatusBadgeClass(flight.status)}`}>
                        {formatFlightStatus(flight.status)}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="btn btn-success btn-sm"
                          onClick={() => handleApproveFlight(flight.id)}
                        >
                          Approve
                        </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => openRejectModal(flight)}
                        >
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Approved Flights */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Approved Flights ({approvedFlights.length})</h2>
        </div>

        {approvedFlights.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--secondary-color)' }}>
            No approved flights
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Route</th>
                  <th>Departure</th>
                  <th>Duration</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {approvedFlights.map((flight) => (
                  <tr key={flight.id}>
                    <td>{flight.name}</td>
                    <td>{flight.departure_airport} → {flight.arrival_airport}</td>
                    <td>{formatDateTime(flight.departure_time)}</td>
                    <td>{flight.duration_minutes} min</td>
                    <td>${formatCurrency(flight.ticket_price)}</td>
                    <td>
                      <span className={`badge ${getStatusBadgeClass(flight.status)}`}>
                        {formatFlightStatus(flight.status)}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        {flight.is_upcoming && (
                          <button
                            className="btn btn-warning btn-sm"
                            onClick={() => handleCancelFlight(flight.id)}
                          >
                            Cancel
                          </button>
                        )}
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteFlight(flight.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Users Management */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Users Management ({users.length})</h2>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Balance</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.first_name} {user.last_name}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className="badge badge-info">{user.role}</span>
                  </td>
                  <td>${formatCurrency(user.account_balance)}</td>
                  <td>{formatDateTime(user.created_at)}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="btn btn-warning btn-sm"
                        onClick={() => openRoleModal(user)}
                      >
                        Change Role
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Ratings */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Flight Ratings ({ratings.length})</h2>
        </div>

        {ratings.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--secondary-color)' }}>
            No ratings yet
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Flight</th>
                  <th>User</th>
                  <th>Rating</th>
                  <th>Comment</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                {ratings.map((rating) => (
                  <tr key={rating.id}>
                    <td>
                      {rating.flight?.name || `Flight #${rating.flight_id}`}
                    </td>
                    <td>{rating.user_email || `User #${rating.user_id}`}</td>
                    <td>{rating.rating}/5</td>
                    <td>{rating.comment || '-'}</td>
                    <td>{formatDateTime(rating.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Reject Flight Modal */}
      {showRejectModal && selectedFlight && (
        <div className="modal-overlay" onClick={() => setShowRejectModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Reject Flight: {selectedFlight.name}</h2>
              <button className="modal-close" onClick={() => setShowRejectModal(false)}>
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Rejection Reason</label>
                <textarea
                  className="form-textarea"
                  rows="4"
                  value={rejectionReason}
                  onChange={(e) => setRejectionReason(e.target.value)}
                  placeholder="Enter reason for rejection..."
                />
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowRejectModal(false)}>
                Cancel
              </button>
              <button className="btn btn-danger" onClick={handleRejectFlight}>
                Reject Flight
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Change Role Modal */}
      {showRoleModal && selectedUser && (
        <div className="modal-overlay" onClick={() => setShowRoleModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Change Role: {selectedUser.first_name} {selectedUser.last_name}</h2>
              <button className="modal-close" onClick={() => setShowRoleModal(false)}>
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Select New Role</label>
                <select
                  className="form-select"
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value)}
                >
                  <option value="KORISNIK">KORISNIK (User)</option>
                  <option value="MANAGER">MANAGER (Manager)</option>
                  <option value="ADMINISTRATOR">ADMINISTRATOR (Admin)</option>
                </select>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowRoleModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleUpdateRole}>
                Update Role
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
