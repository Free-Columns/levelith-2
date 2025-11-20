/**
 * Theme Configuration - Integrated with ONETRUTH
 *
 * This file imports the ONETRUTH configuration from the main frontend
 * and provides theme utilities for the admin dashboard.
 */

// Import ONETRUTH from main frontend config
import { ONETRUTH } from '../../config/ONETRUTH';

/**
 * Get category color from ONETRUTH
 */
export const getCategoryColor = (category) => {
  const colors = {
    education: ONETRUTH.colors.education,
    workplace: ONETRUTH.colors.workplace,
    skills: ONETRUTH.colors.skills,
  };
  return colors[category] || ONETRUTH.colors.text;
};

/**
 * Get NAICS industry color
 */
export const getNAICSColor = (industry) => {
  return ONETRUTH.naics[industry] || ONETRUTH.naics.general;
};

/**
 * Get status color
 */
export const getStatusColor = (status) => {
  const colors = {
    success: ONETRUTH.colors.success,
    warning: ONETRUTH.colors.warning,
    error: ONETRUTH.colors.error,
    info: ONETRUTH.colors.info,
    active: ONETRUTH.colors.success,
    inactive: ONETRUTH.colors.error,
  };
  return colors[status] || ONETRUTH.colors.text;
};

export default ONETRUTH;
