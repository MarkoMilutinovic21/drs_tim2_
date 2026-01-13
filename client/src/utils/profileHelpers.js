import defaultAvatar from '../assets/default-avatar.svg';

const SERVER_URL = 'http://localhost:5000';

/**
 * Get profile picture URL for a user
 * @param {string|null} profilePicture - Profile picture filename from user object
 * @returns {string} URL to profile picture or default avatar
 */
export const getProfilePictureUrl = (profilePicture) => {
  if (!profilePicture) {
    return defaultAvatar;
  }
  return `${SERVER_URL}/uploads/${profilePicture}`;
};

export default {
  getProfilePictureUrl
};
