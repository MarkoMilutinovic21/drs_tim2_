import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { userAPI, bookingAPI } from '../services/api';
import { formatDate, formatCurrency, formatDateTime, getStatusBadgeClass, formatBookingStatus } from '../utils/formatters';
import { validatePositiveNumber, validateRequired, validateEmail, validateDateOfBirth } from '../utils/validators';
import { getProfilePictureUrl } from '../utils/profileHelpers';
import './Profile.css';

const Profile = () => {
  const { user, refreshUser } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [showAddBalanceModal, setShowAddBalanceModal] = useState(false);
  const [balanceAmount, setBalanceAmount] = useState('');
  const [showEditModal, setShowEditModal] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    date_of_birth: '',
    gender: '',
    country: '',
    street: '',
    street_number: '',
    profile_picture: null
  });

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

  const handleEditProfile = () => {
    setFormData({
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      email: user.email || '',
      date_of_birth: user.date_of_birth ? user.date_of_birth.split('T')[0] : '',
      gender: user.gender || '',
      country: user.country || '',
      street: user.street || '',
      street_number: user.street_number || '',
      profile_picture: null
    });
    setShowEditModal(true);
    setError('');
    setSuccessMessage('');
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        profile_picture: file
      }));
    }
  };

  const validateProfileForm = () => {
    const validations = [
      validateRequired(formData.first_name, 'First name'),
      validateRequired(formData.last_name, 'Last name'),
      validateRequired(formData.email, 'Email'),
      validateRequired(formData.date_of_birth, 'Date of birth'),
      validateRequired(formData.gender, 'Gender'),
      validateRequired(formData.country, 'Country'),
      validateRequired(formData.street, 'Street'),
      validateRequired(formData.street_number, 'Street number'),
      validateDateOfBirth(formData.date_of_birth)
    ];

    for (const validation of validations) {
      if (!validation.valid) {
        setError(validation.message);
        return false;
      }
    }

    if (!validateEmail(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    return true;
  };

  const handleUpdateProfile = async () => {
    setError('');
    setSuccessMessage('');

    if (!validateProfileForm()) {
      return;
    }

    try {
      // Prepare user data (excluding profile picture)
      const updateData = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        country: formData.country,
        street: formData.street,
        street_number: formData.street_number
      };

      // Update user profile
      await userAPI.update(user.id, updateData);

      // Upload profile picture if selected
      if (formData.profile_picture) {
        await userAPI.uploadProfilePicture(user.id, formData.profile_picture);
      }

      setSuccessMessage('Profile updated successfully');
      setShowEditModal(false);
      await refreshUser();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update profile');
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
            <button className="btn btn-secondary" onClick={handleEditProfile}>
              Edit Profile
            </button>
          </div>
          <div className="profile-info">
            <div className="profile-picture-container">
              <img
                src={getProfilePictureUrl(user.profile_picture)}
                alt="Profile"
                className="profile-picture"
              />
            </div>
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

      {/* Edit Profile Modal */}
      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Edit Profile</h2>
              <button className="modal-close" onClick={() => setShowEditModal(false)}>
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">First Name *</label>
                  <input
                    type="text"
                    className="form-input"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleFormChange}
                    placeholder="Enter first name"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Last Name *</label>
                  <input
                    type="text"
                    className="form-input"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleFormChange}
                    placeholder="Enter last name"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Email *</label>
                  <input
                    type="email"
                    className="form-input"
                    name="email"
                    value={formData.email}
                    onChange={handleFormChange}
                    placeholder="Enter email"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Date of Birth *</label>
                  <input
                    type="date"
                    className="form-input"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleFormChange}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Gender *</label>
                  <select
                    className="form-input"
                    name="gender"
                    value={formData.gender}
                    onChange={handleFormChange}
                  >
                    <option value="">Select gender</option>
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Country *</label>
                  <input
                    type="text"
                    className="form-input"
                    name="country"
                    value={formData.country}
                    onChange={handleFormChange}
                    placeholder="Enter country"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Street *</label>
                  <input
                    type="text"
                    className="form-input"
                    name="street"
                    value={formData.street}
                    onChange={handleFormChange}
                    placeholder="Enter street"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Street Number *</label>
                  <input
                    type="text"
                    className="form-input"
                    name="street_number"
                    value={formData.street_number}
                    onChange={handleFormChange}
                    placeholder="Enter street number"
                  />
                </div>

                <div className="form-group form-group-full">
                  <label className="form-label">Profile Picture (Optional)</label>
                  <input
                    type="file"
                    className="form-input"
                    accept="image/*"
                    onChange={handleFileChange}
                  />
                  {formData.profile_picture && (
                    <small className="form-hint">Selected: {formData.profile_picture.name}</small>
                  )}
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowEditModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleUpdateProfile}>
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
