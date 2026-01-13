import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  validateEmail,
  validatePassword,
  validateRequired,
  validateDateOfBirth
} from '../utils/validators';
import './Auth.css';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
    date_of_birth: '',
    gender: 'M',
    country: '',
    street: '',
    street_number: '',
    account_balance: '0'
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const [success, setSuccess] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    // First name
    const firstNameValidation = validateRequired(formData.first_name, 'First name');
    if (!firstNameValidation.valid) {
      newErrors.first_name = firstNameValidation.message;
    }

    // Last name
    const lastNameValidation = validateRequired(formData.last_name, 'Last name');
    if (!lastNameValidation.valid) {
      newErrors.last_name = lastNameValidation.message;
    }

    // Email
    const emailValidation = validateRequired(formData.email, 'Email');
    if (!emailValidation.valid) {
      newErrors.email = emailValidation.message;
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Password
    const passwordValidation = validatePassword(formData.password);
    if (!passwordValidation.valid) {
      newErrors.password = passwordValidation.message;
    }

    // Confirm password
    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }

    // Date of birth
    const dobValidation = validateDateOfBirth(formData.date_of_birth);
    if (!dobValidation.valid) {
      newErrors.date_of_birth = dobValidation.message;
    }

    // Country
    const countryValidation = validateRequired(formData.country, 'Country');
    if (!countryValidation.valid) {
      newErrors.country = countryValidation.message;
    }

    // Street
    const streetValidation = validateRequired(formData.street, 'Street');
    if (!streetValidation.valid) {
      newErrors.street = streetValidation.message;
    }

    // Street number
    const streetNumberValidation = validateRequired(formData.street_number, 'Street number');
    if (!streetNumberValidation.valid) {
      newErrors.street_number = streetNumberValidation.message;
    }

    // Account balance
    const balance = parseFloat(formData.account_balance);
    if (isNaN(balance) || balance < 0) {
      newErrors.account_balance = 'Account balance must be a positive number';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setGeneralError('');

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);

    // Remove confirm_password before sending
    const { confirm_password, ...registerData } = formData;

    const result = await register(registerData);

    if (result.success) {
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } else {
      if (typeof result.error === 'string') {
        setGeneralError(result.error);
      } else if (Array.isArray(result.error)) {
        setGeneralError(result.error.join(', '));
      }
    }

    setLoading(false);
  };

  if (success) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="auth-card">
            <div className="alert alert-success">
              <h3>Registration Successful!</h3>
              <p>Redirecting to login page...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <h2 className="auth-title">Register</h2>
          <p className="auth-subtitle">Create your account to start booking flights.</p>

          {generalError && (
            <div className="alert alert-error">
              {generalError}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">First Name</label>
                <input
                  type="text"
                  name="first_name"
                  className="form-input"
                  value={formData.first_name}
                  onChange={handleChange}
                  placeholder="John"
                />
                {errors.first_name && <div className="form-error">{errors.first_name}</div>}
              </div>

              <div className="form-group">
                <label className="form-label">Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  className="form-input"
                  value={formData.last_name}
                  onChange={handleChange}
                  placeholder="Doe"
                />
                {errors.last_name && <div className="form-error">{errors.last_name}</div>}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Email</label>
              <input
                type="email"
                name="email"
                className="form-input"
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
              />
              {errors.email && <div className="form-error">{errors.email}</div>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  name="password"
                  className="form-input"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                />
                {errors.password && <div className="form-error">{errors.password}</div>}
              </div>

              <div className="form-group">
                <label className="form-label">Confirm Password</label>
                <input
                  type="password"
                  name="confirm_password"
                  className="form-input"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  placeholder="••••••••"
                />
                {errors.confirm_password && <div className="form-error">{errors.confirm_password}</div>}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Date of Birth</label>
                <input
                  type="date"
                  name="date_of_birth"
                  className="form-input"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                />
                {errors.date_of_birth && <div className="form-error">{errors.date_of_birth}</div>}
              </div>

              <div className="form-group">
                <label className="form-label">Gender</label>
                <select
                  name="gender"
                  className="form-select"
                  value={formData.gender}
                  onChange={handleChange}
                >
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Country</label>
              <input
                type="text"
                name="country"
                className="form-input"
                value={formData.country}
                onChange={handleChange}
                placeholder="Serbia"
              />
              {errors.country && <div className="form-error">{errors.country}</div>}
            </div>

            <div className="form-row">
              <div className="form-group" style={{ flex: 2 }}>
                <label className="form-label">Street</label>
                <input
                  type="text"
                  name="street"
                  className="form-input"
                  value={formData.street}
                  onChange={handleChange}
                  placeholder="Main Street"
                />
                {errors.street && <div className="form-error">{errors.street}</div>}
              </div>

              <div className="form-group" style={{ flex: 1 }}>
                <label className="form-label">Number</label>
                <input
                  type="text"
                  name="street_number"
                  className="form-input"
                  value={formData.street_number}
                  onChange={handleChange}
                  placeholder="123"
                />
                {errors.street_number && <div className="form-error">{errors.street_number}</div>}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Initial Account Balance</label>
              <input
                type="number"
                name="account_balance"
                className="form-input"
                value={formData.account_balance}
                onChange={handleChange}
                placeholder="0.00"
                min="0"
                step="0.01"
              />
              {errors.account_balance && <div className="form-error">{errors.account_balance}</div>}
              <small style={{ color: '#666', fontSize: '0.85rem' }}>Enter your starting account balance (optional, defaults to 0)</small>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={loading}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>

          <div className="auth-footer">
            <p>
              Already have an account?{' '}
              <Link to="/login" className="auth-link">
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;