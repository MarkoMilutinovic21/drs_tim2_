import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { flightAPI, bookingAPI, ratingAPI, airlineAPI } from '../services/api';
import { useFlightTimer } from '../hooks/useFlightTimer';
import {
  formatDateTime,
  formatCurrency,
  formatFlightStatus,
  getStatusBadgeClass
} from '../utils/formatters';
import './Flights.css';

const Flights = () => {
  const [activeTab, setActiveTab] = useState('upcoming');
  const [flights, setFlights] = useState({
    upcoming: [],
    ongoing: [],
    completed_cancelled: []
  });
  const [airlines, setAirlines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [searchName, setSearchName] = useState('');
  const [selectedAirline, setSelectedAirline] = useState('');
  const [bookingLoading, setBookingLoading] = useState({});
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [ratingData, setRatingData] = useState({ rating: 5, comment: '' });

  const { user } = useAuth();

  useEffect(() => {
    loadFlights();
    loadAirlines();
    // Refresh flights every 30 seconds
    const interval = setInterval(loadFlights, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadFlights = async () => {
    try {
      setLoading(true);
      const response = await flightAPI.getByTabs();
      setFlights(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load flights');
      console.error(err);
    } finally {
      setLoading(false);
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

  const handleBookFlight = async (flightId) => {
    setBookingLoading((prev) => ({ ...prev, [flightId]: true }));
    setError('');
    setSuccessMessage('');

    try {
      const response = await bookingAPI.create(flightId, user.id);
      setSuccessMessage('Booking is being processed! Check back in a few moments.');
      
      // Refresh flights after 6 seconds (after async processing)
      setTimeout(() => {
        loadFlights();
      }, 6000);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to book flight';
      setError(errorMsg);
    } finally {
      setBookingLoading((prev) => ({ ...prev, [flightId]: false }));
    }
  };

  const handleRateFlight = (flight) => {
    setSelectedFlight(flight);
    setShowRatingModal(true);
    setRatingData({ rating: 5, comment: '' });
  };

  const submitRating = async () => {
    if (!selectedFlight) return;

    try {
      await ratingAPI.create(
        selectedFlight.id,
        user.id,
        ratingData.rating,
        ratingData.comment
      );
      setSuccessMessage('Rating submitted successfully!');
      setShowRatingModal(false);
      setSelectedFlight(null);
      loadFlights();
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to submit rating';
      setError(errorMsg);
    }
  };

  const FlightCard = ({ flight }) => {
    const { formatTime, isOngoing } = useFlightTimer(flight);

    return (
      <div className="flight-card">
        <div className="flight-header">
          <h3 className="flight-name">{flight.name}</h3>
          <span className={`badge ${getStatusBadgeClass(flight.status)}`}>
            {formatFlightStatus(flight.status)}
          </span>
        </div>

        <div className="flight-details">
          <div className="flight-route">
            <div className="airport">
              <span className="airport-label">From</span>
              <span className="airport-name">{flight.departure_airport}</span>
            </div>
            <div className="flight-arrow">✈️</div>
            <div className="airport">
              <span className="airport-label">To</span>
              <span className="airport-name">{flight.arrival_airport}</span>
            </div>
          </div>

          <div className="flight-info-grid">
            <div className="info-item">
              <span className="info-label">Departure</span>
              <span className="info-value">{formatDateTime(flight.departure_time)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Duration</span>
              <span className="info-value">{flight.duration_minutes} min</span>
            </div>
            <div className="info-item">
              <span className="info-label">Distance</span>
              <span className="info-value">{flight.distance_km} km</span>
            </div>
            <div className="info-item">
              <span className="info-label">Price</span>
              <span className="info-value price">${formatCurrency(flight.ticket_price)}</span>
            </div>
          </div>

          {isOngoing && (
            <div className="flight-timer">
              <span className="timer-icon">⏱️</span>
              <span className="timer-text">Time Remaining: {formatTime()}</span>
            </div>
          )}
        </div>

        <div className="flight-actions">
          {activeTab === 'upcoming' && (
            <button
              className="btn btn-primary"
              onClick={() => handleBookFlight(flight.id)}
              disabled={bookingLoading[flight.id]}
            >
              {bookingLoading[flight.id] ? 'Booking...' : 'Book Flight'}
            </button>
          )}

          {activeTab === 'completed_cancelled' && flight.status === 'COMPLETED' && (
            <button
              className="btn btn-warning"
              onClick={() => handleRateFlight(flight)}
            >
              Rate Flight
            </button>
          )}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flights-page">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading flights...</p>
      </div>
    );
  }

  const nameFilter = searchName.trim().toLowerCase();
  const airlineFilter = selectedAirline ? parseInt(selectedAirline, 10) : null;

  const currentFlights = (flights[activeTab] || []).filter((flight) => {
    if (nameFilter && !flight.name.toLowerCase().includes(nameFilter)) {
      return false;
    }
    if (airlineFilter && flight.airline_id !== airlineFilter) {
      return false;
    }
    return true;
  });

  return (
    <div className="flights-page">
      <div className="page-header">
        <h1>Flights</h1>
        <p>Browse and book available flights</p>
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

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'upcoming' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('upcoming')}
        >
          Upcoming ({flights.upcoming.length})
        </button>
        <button
          className={`tab ${activeTab === 'ongoing' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('ongoing')}
        >
          In Progress ({flights.ongoing.length})
        </button>
        <button
          className={`tab ${activeTab === 'completed_cancelled' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('completed_cancelled')}
        >
          Completed / Cancelled ({flights.completed_cancelled.length})
        </button>
      </div>

      <div className="filters">
        <input
          type="text"
          className="form-input"
          placeholder="Search by flight name..."
          value={searchName}
          onChange={(e) => setSearchName(e.target.value)}
        />
        <select
          className="form-select"
          value={selectedAirline}
          onChange={(e) => setSelectedAirline(e.target.value)}
        >
          <option value="">All airlines</option>
          {airlines.map((airline) => (
            <option key={airline.id} value={airline.id}>
              {airline.name} ({airline.code})
            </option>
          ))}
        </select>
      </div>

      <div className="flights-grid">
        {currentFlights.length === 0 ? (
          <div className="empty-state">
            <p>No flights in this category</p>
          </div>
        ) : (
          currentFlights.map((flight) => <FlightCard key={flight.id} flight={flight} />)
        )}
      </div>

      {/* Rating Modal */}
      {showRatingModal && selectedFlight && (
        <div className="modal-overlay" onClick={() => setShowRatingModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Rate Flight: {selectedFlight.name}</h2>
              <button className="modal-close" onClick={() => setShowRatingModal(false)}>
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Rating (1-5)</label>
                <div className="rating-stars">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span
                      key={star}
                      className={`star ${ratingData.rating >= star ? 'star-filled' : ''}`}
                      onClick={() => setRatingData({ ...ratingData, rating: star })}
                    >
                      ★
                    </span>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Comment (optional)</label>
                <textarea
                  className="form-textarea"
                  rows="4"
                  value={ratingData.comment}
                  onChange={(e) => setRatingData({ ...ratingData, comment: e.target.value })}
                  placeholder="Share your experience..."
                />
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowRatingModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={submitRating}>
                Submit Rating
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Flights;
