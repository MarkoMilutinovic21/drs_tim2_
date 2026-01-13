import { format, parseISO } from 'date-fns';

/**
 * Format date to readable string
 */
export const formatDate = (dateString) => {
  if (!dateString) return '';
  try {
    return format(parseISO(dateString), 'dd.MM.yyyy');
  } catch (error) {
    return dateString;
  }
};

/**
 * Format datetime to readable string
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return '';
  try {
    return format(parseISO(dateString), 'dd.MM.yyyy HH:mm');
  } catch (error) {
    return dateString;
  }
};

/**
 * Format time only
 */
export const formatTime = (dateString) => {
  if (!dateString) return '';
  try {
    return format(parseISO(dateString), 'HH:mm');
  } catch (error) {
    return dateString;
  }
};

/**
 * Format currency
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '0.00';
  return Number(amount).toFixed(2);
};

/**
 * Format flight status to readable string
 */
export const formatFlightStatus = (status) => {
  const statusMap = {
    'PENDING': 'Pending Approval',
    'APPROVED': 'Approved',
    'REJECTED': 'Rejected',
    'CANCELLED': 'Cancelled',
    'ONGOING': 'In Progress',
    'COMPLETED': 'Completed'
  };
  return statusMap[status] || status;
};

/**
 * Format booking status to readable string
 */
export const formatBookingStatus = (status) => {
  const statusMap = {
    'PENDING': 'Pending',
    'PROCESSING': 'Processing',
    'COMPLETED': 'Completed',
    'CANCELLED': 'Cancelled',
    'REFUNDED': 'Refunded'
  };
  return statusMap[status] || status;
};

/**
 * Get status badge class
 */
export const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'APPROVED':
    case 'COMPLETED':
      return 'badge-success';
    case 'PENDING':
    case 'PROCESSING':
      return 'badge-warning';
    case 'REJECTED':
    case 'CANCELLED':
    case 'REFUNDED':
      return 'badge-danger';
    case 'ONGOING':
      return 'badge-info';
    default:
      return 'badge-info';
  }
};