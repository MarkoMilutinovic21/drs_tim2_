/**
 * Validate email format
 */
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 */
export const validatePassword = (password) => {
  if (!password || password.length < 6) {
    return { valid: false, message: 'Password must be at least 6 characters long' };
  }
  return { valid: true };
};

/**
 * Validate required field
 */
export const validateRequired = (value, fieldName) => {
  if (!value || (typeof value === 'string' && value.trim().length === 0)) {
    return { valid: false, message: `${fieldName} is required` };
  }
  return { valid: true };
};

/**
 * Validate date of birth (must be 18+)
 */
export const validateDateOfBirth = (dob) => {
  if (!dob) {
    return { valid: false, message: 'Date of birth is required' };
  }

  const today = new Date();
  const birthDate = new Date(dob);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }

  if (age < 18) {
    return { valid: false, message: 'You must be at least 18 years old' };
  }

  return { valid: true };
};

/**
 * Validate positive number
 */
export const validatePositiveNumber = (value, fieldName) => {
  const num = Number(value);
  if (isNaN(num) || num <= 0) {
    return { valid: false, message: `${fieldName} must be a positive number` };
  }
  return { valid: true };
};

/**
 * Validate future date
 */
export const validateFutureDate = (dateString, fieldName) => {
  const date = new Date(dateString);
  const now = new Date();
  
  if (date <= now) {
    return { valid: false, message: `${fieldName} must be in the future` };
  }
  
  return { valid: true };
};

/**
 * Validate rating (1-5)
 */
export const validateRating = (rating) => {
  const num = Number(rating);
  if (isNaN(num) || num < 1 || num > 5) {
    return { valid: false, message: 'Rating must be between 1 and 5' };
  }
  return { valid: true };
};