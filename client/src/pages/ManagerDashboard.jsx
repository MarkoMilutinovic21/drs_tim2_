import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { flightAPI, airlineAPI } from '../services/api';
import {
  formatDateTime,
  formatCurrency,
  formatFlightStatus,
  getStatusBadgeClass
} from '../utils/formatters';
import {
  validateRequired,
  validatePositiveNumber,
  validateFutureDate
} from '../utils/validators';
import './ManagerDashboard.css';

const ManagerDashboard = () => {
  const [flights, setFlights] = useState([]);
  const [airlines, setAirlines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAirlineModal, setShowAirlineModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    airline_id: '',
    distance_km: '',
    duration_minutes: '',
    departure_time: '',
    departure_airport: '',
    arrival_airport: '',
    ticket_price: ''
  });
  const [formErrors, setFormErrors] = useState({});
  const [airlineFormData, setAirlineFormData] = useState({
    name: '',
    code: '',
    country: '',
    description: '',
    logo_url: ''
  });
  const [airlineErrors, setAirlineErrors] = useState({});

  const { user } = useAuth();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    await Promise.all([loadFlights(), loadAirlines()]);
    setLoading(false);
  };

  const loadFlights = async () => {
    try {
      const response = await flightAPI.getAll();
      setFlights(response.data.flights);
    } catch (err) {
      console.error('Failed to load flights:', err);
    }
  };

  const loadAirlines = async () => {
    try {
      const response = await airlineAPI.getAll();
      setAirlines(response.data.airlines);
    } catch (err) {
      console.error('Failed to load airlines:', err);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      airline_id: '',
      distance_km: '',
      duration_minutes: '',
      departure_time: '',
      departure_airport: '',
      arrival_airport: '',
      ticket_price: ''
    });
    setFormErrors({});
  };

  const resetAirlineForm = () => {
    setAirlineFormData({
      name: '',
      code: '',
      country: '',
      description: '',
      logo_url: ''
    });
    setAirlineErrors({});
  };

  const validateForm = () => {
    const errors = {};

    const nameValidation = validateRequired(formData.name, 'Flight name');
    if (!nameValidation.valid) errors.name = nameValidation.message;

    const airlineValidation = validateRequired(formData.airline_id, 'Airline');
    if (!airlineValidation.valid) errors.airline_id = airlineValidation.message;

    const distanceValidation = validatePositiveNumber(formData.distance_km, 'Distance');
    if (!distanceValidation.valid) errors.distance_km = distanceValidation.message;

    const durationValidation = validatePositiveNumber(formData.duration_minutes, 'Duration');
    if (!durationValidation.valid) errors.duration_minutes = durationValidation.message;

    const dateValidation = validateFutureDate(formData.departure_time, 'Departure time');
    if (!dateValidation.valid) errors.departure_time = dateValidation.message;

    const depAirportValidation = validateRequired(formData.departure_airport, 'Departure airport');
    if (!depAirportValidation.valid) errors.departure_airport = depAirportValidation.message;

    const arrAirportValidation = validateRequired(formData.arrival_airport, 'Arrival airport');
    if (!arrAirportValidation.valid) errors.arrival_airport = arrAirportValidation.message;

    const priceValidation = validatePositiveNumber(formData.ticket_price, 'Ticket price');
    if (!priceValidation.valid) errors.ticket_price = priceValidation.message;

    return errors;
  };

  const validateAirlineForm = () => {
    const errors = {};

    const nameValidation = validateRequired(airlineFormData.name, 'Airline name');
    if (!nameValidation.valid) errors.name = nameValidation.message;

    const codeValidation = validateRequired(airlineFormData.code, 'Airline code');
    if (!codeValidation.valid) errors.code = codeValidation.message;

    const countryValidation = validateRequired(airlineFormData.country, 'Country');
    if (!countryValidation.valid) errors.country = countryValidation.message;

    return errors;
  };

  const handleCreateFlight = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    try {
      const departureISO = new Date(formData.departure_time).toISOString();
      const flightData = {
        ...formData,
        airline_id: parseInt(formData.airline_id),
        distance_km: parseInt(formData.distance_km),
        duration_minutes: parseInt(formData.duration_minutes),
        ticket_price: parseFloat(formData.ticket_price),
        departure_time: departureISO,
        created_by: user.id
      };

      await flightAPI.create(flightData);
      setSuccessMessage('Flight created successfully and sent for approval');
      setShowCreateModal(false);
      resetForm();
      loadFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create flight');
    }
  };

  const handleCreateAirline = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    const errors = validateAirlineForm();
    if (Object.keys(errors).length > 0) {
      setAirlineErrors(errors);
      return;
    }

    try {
      await airlineAPI.create({
        name: airlineFormData.name,
        code: airlineFormData.code,
        country: airlineFormData.country,
        description: airlineFormData.description || null,
        logo_url: airlineFormData.logo_url || null
      });
      setSuccessMessage('Airline created successfully');
      setShowAirlineModal(false);
      resetAirlineForm();
      loadAirlines();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create airline');
    }
  };

  const handleUpdateFlight = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    try {
      const departureISO = new Date(formData.departure_time).toISOString();
      const updateData = {
        name: formData.name,
        distance_km: parseInt(formData.distance_km),
        duration_minutes: parseInt(formData.duration_minutes),
        departure_time: departureISO,
        departure_airport: formData.departure_airport,
        arrival_airport: formData.arrival_airport,
        ticket_price: parseFloat(formData.ticket_price)
      };

      await flightAPI.update(selectedFlight.id, updateData);
      setSuccessMessage('Flight updated and resubmitted for approval');
      setShowEditModal(false);
      setSelectedFlight(null);
      resetForm();
      loadFlights();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update flight');
    }
  };

  const openEditModal = (flight) => {
    const toLocalInputValue = (dateString) => {
      const date = new Date(dateString);
      const pad = (value) => String(value).padStart(2, '0');
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
    };

    setSelectedFlight(flight);
    setFormData({
      name: flight.name,
      airline_id: flight.airline_id,
      distance_km: flight.distance_km,
      duration_minutes: flight.duration_minutes,
      departure_time: toLocalInputValue(flight.departure_time),
      departure_airport: flight.departure_airport,
      arrival_airport: flight.arrival_airport,
      ticket_price: flight.ticket_price
    });
    setShowEditModal(true);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleAirlineChange = (e) => {
    const { name, value } = e.target;
    setAirlineFormData((prev) => ({ ...prev, [name]: value }));
    if (airlineErrors[name]) {
      setAirlineErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  if (loading) {
    return (
      <div className="manager-dashboard">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="manager-dashboard">
      <div className="page-header">
        <div>
          <h1>Manager Dashboard</h1>
          <p>Manage flights</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={() => setShowAirlineModal(true)}>
            Create Airline
          </button>
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            Create New Flight
          </button>
        </div>
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

      {/* Flights Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">My Flights ({flights.length})</h2>
        </div>

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
              {flights.map((flight) => (
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
                    {flight.status === 'REJECTED' && (
                      <button
                        className="btn btn-warning btn-sm"
                        onClick={() => openEditModal(flight)}
                      >
                        Edit & Resubmit
                      </button>
                    )}
                    {flight.status === 'REJECTED' && flight.rejection_reason && (
                      <div className="rejection-reason">
                        Reason: {flight.rejection_reason}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create Flight Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create New Flight</h2>
              <button className="modal-close" onClick={() => { setShowCreateModal(false); resetForm(); }}>
                ×
              </button>
            </div>

            <form onSubmit={handleCreateFlight}>
              <div className="modal-body">
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Flight Name</label>
                    <input
                      type="text"
                      name="name"
                      className="form-input"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="e.g., BEG-NYC-001"
                    />
                    {formErrors.name && <div className="form-error">{formErrors.name}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Airline</label>
                    <select
                      name="airline_id"
                      className="form-select"
                      value={formData.airline_id}
                      onChange={handleChange}
                    >
                      <option value="">Select airline</option>
                      {airlines.map((airline) => (
                        <option key={airline.id} value={airline.id}>
                          {airline.name} ({airline.code})
                        </option>
                      ))}
                    </select>
                    {formErrors.airline_id && <div className="form-error">{formErrors.airline_id}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Departure Airport</label>
                    <input
                      type="text"
                      name="departure_airport"
                      className="form-input"
                      value={formData.departure_airport}
                      onChange={handleChange}
                      placeholder="Belgrade Nikola Tesla"
                    />
                    {formErrors.departure_airport && <div className="form-error">{formErrors.departure_airport}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Arrival Airport</label>
                    <input
                      type="text"
                      name="arrival_airport"
                      className="form-input"
                      value={formData.arrival_airport}
                      onChange={handleChange}
                      placeholder="JFK New York"
                    />
                    {formErrors.arrival_airport && <div className="form-error">{formErrors.arrival_airport}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Distance (km)</label>
                    <input
                      type="number"
                      name="distance_km"
                      className="form-input"
                      value={formData.distance_km}
                      onChange={handleChange}
                      min="1"
                    />
                    {formErrors.distance_km && <div className="form-error">{formErrors.distance_km}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Duration (minutes)</label>
                    <input
                      type="number"
                      name="duration_minutes"
                      className="form-input"
                      value={formData.duration_minutes}
                      onChange={handleChange}
                      min="1"
                    />
                    {formErrors.duration_minutes && <div className="form-error">{formErrors.duration_minutes}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Departure Time</label>
                    <input
                      type="datetime-local"
                      name="departure_time"
                      className="form-input"
                      value={formData.departure_time}
                      onChange={handleChange}
                    />
                    {formErrors.departure_time && <div className="form-error">{formErrors.departure_time}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Ticket Price ($)</label>
                    <input
                      type="number"
                      name="ticket_price"
                      className="form-input"
                      value={formData.ticket_price}
                      onChange={handleChange}
                      min="0.01"
                      step="0.01"
                    />
                    {formErrors.ticket_price && <div className="form-error">{formErrors.ticket_price}</div>}
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => { setShowCreateModal(false); resetForm(); }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Flight
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Airline Modal */}
      {showAirlineModal && (
        <div className="modal-overlay" onClick={() => setShowAirlineModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create Airline</h2>
              <button className="modal-close" onClick={() => { setShowAirlineModal(false); resetAirlineForm(); }}>
                ×
              </button>
            </div>

            <form onSubmit={handleCreateAirline}>
              <div className="modal-body">
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Name</label>
                    <input
                      type="text"
                      name="name"
                      className="form-input"
                      value={airlineFormData.name}
                      onChange={handleAirlineChange}
                    />
                    {airlineErrors.name && <div className="form-error">{airlineErrors.name}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Code</label>
                    <input
                      type="text"
                      name="code"
                      className="form-input"
                      value={airlineFormData.code}
                      onChange={handleAirlineChange}
                      placeholder="e.g., JU"
                    />
                    {airlineErrors.code && <div className="form-error">{airlineErrors.code}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Country</label>
                    <input
                      type="text"
                      name="country"
                      className="form-input"
                      value={airlineFormData.country}
                      onChange={handleAirlineChange}
                    />
                    {airlineErrors.country && <div className="form-error">{airlineErrors.country}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Logo URL (optional)</label>
                    <input
                      type="url"
                      name="logo_url"
                      className="form-input"
                      value={airlineFormData.logo_url}
                      onChange={handleAirlineChange}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Description (optional)</label>
                  <textarea
                    name="description"
                    className="form-textarea"
                    rows="3"
                    value={airlineFormData.description}
                    onChange={handleAirlineChange}
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => { setShowAirlineModal(false); resetAirlineForm(); }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Airline
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Flight Modal (same structure as Create) */}
      {showEditModal && selectedFlight && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Edit Flight: {selectedFlight.name}</h2>
              <button className="modal-close" onClick={() => { setShowEditModal(false); setSelectedFlight(null); resetForm(); }}>
                ×
              </button>
            </div>

            <form onSubmit={handleUpdateFlight}>
              <div className="modal-body">
                {/* Same form fields as Create Modal */}
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Flight Name</label>
                    <input
                      type="text"
                      name="name"
                      className="form-input"
                      value={formData.name}
                      onChange={handleChange}
                    />
                    {formErrors.name && <div className="form-error">{formErrors.name}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Airline</label>
                    <select
                      name="airline_id"
                      className="form-select"
                      value={formData.airline_id}
                      onChange={handleChange}
                      disabled
                    >
                      {airlines.map((airline) => (
                        <option key={airline.id} value={airline.id}>
                          {airline.name} ({airline.code})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Departure Airport</label>
                    <input
                      type="text"
                      name="departure_airport"
                      className="form-input"
                      value={formData.departure_airport}
                      onChange={handleChange}
                    />
                    {formErrors.departure_airport && <div className="form-error">{formErrors.departure_airport}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Arrival Airport</label>
                    <input
                      type="text"
                      name="arrival_airport"
                      className="form-input"
                      value={formData.arrival_airport}
                      onChange={handleChange}
                    />
                    {formErrors.arrival_airport && <div className="form-error">{formErrors.arrival_airport}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Distance (km)</label>
                    <input
                      type="number"
                      name="distance_km"
                      className="form-input"
                      value={formData.distance_km}
                      onChange={handleChange}
                      min="1"
                    />
                    {formErrors.distance_km && <div className="form-error">{formErrors.distance_km}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Duration (minutes)</label>
                    <input
                      type="number"
                      name="duration_minutes"
                      className="form-input"
                      value={formData.duration_minutes}
                      onChange={handleChange}
                      min="1"
                    />
                    {formErrors.duration_minutes && <div className="form-error">{formErrors.duration_minutes}</div>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Departure Time</label>
                    <input
                      type="datetime-local"
                      name="departure_time"
                      className="form-input"
                      value={formData.departure_time}
                      onChange={handleChange}
                    />
                    {formErrors.departure_time && <div className="form-error">{formErrors.departure_time}</div>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Ticket Price ($)</label>
                    <input
                      type="number"
                      name="ticket_price"
                      className="form-input"
                      value={formData.ticket_price}
                      onChange={handleChange}
                      min="0.01"
                      step="0.01"
                    />
                    {formErrors.ticket_price && <div className="form-error">{formErrors.ticket_price}</div>}
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => { setShowEditModal(false); setSelectedFlight(null); resetForm(); }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Update & Resubmit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManagerDashboard;
