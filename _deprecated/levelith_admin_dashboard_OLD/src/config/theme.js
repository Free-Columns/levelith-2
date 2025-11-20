/**
 * Theme Configuration - Integrated with ONETRUTH
 *
 * This file imports the ONETRUTH configuration from the main frontend
 * and provides theme utilities for the admin dashboard.
 */

// Import ONETRUTH from main frontend config
// For now, we'll replicate the essential values here
// TODO: Set up proper import path when integrating with main frontend

export const ONETRUTH = {
  colors: {
    primary: "#3498db",
    primaryDark: "#2980b9",
    primaryLight: "#5dade2",
    secondary: "#2ecc71",
    secondaryDark: "#27ae60",
    secondaryLight: "#58d68d",
    accent: "#e74c3c",
    accentDark: "#c0392b",
    accentLight: "#ec7063",
    background: "#ecf0f1",
    backgroundDark: "#34495e",
    surface: "#ffffff",
    surfaceDark: "#2c3e50",
    text: "#2c3e50",
    textLight: "#7f8c8d",
    textDark: "#1a252f",
    textInverse: "#ffffff",
    success: "#2ecc71",
    warning: "#f39c12",
    error: "#e74c3c",
    info: "#3498db",
    education: "#9b59b6",
    workplace: "#e67e22",
    skills: "#1abc9c",
    border: "#bdc3c7",
    borderLight: "#ecf0f1",
    divider: "#d5dbdb",
  },

  fonts: {
    heading: '"Montserrat", "Helvetica Neue", Arial, sans-serif',
    body: '"Open Sans", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    monospace: '"Fira Code", "Courier New", Courier, monospace',
    sizes: {
      xs: "0.75rem",
      sm: "0.875rem",
      base: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
    },
    weights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
  },

  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
    "2xl": "3rem",
    "3xl": "4rem",
  },

  borderRadius: {
    none: "0",
    sm: "0.125rem",
    base: "0.25rem",
    md: "0.375rem",
    lg: "0.5rem",
    xl: "0.75rem",
    "2xl": "1rem",
    full: "9999px",
  },

  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    base: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
  },

  gamification: {
    levels: {
      beginner: "#95a5a6",
      intermediate: "#3498db",
      advanced: "#9b59b6",
      expert: "#e67e22",
      master: "#e74c3c",
      legend: "#f39c12",
    },
    achievements: {
      bronze: "#cd7f32",
      silver: "#c0c0c0",
      gold: "#ffd700",
      platinum: "#e5e4e2",
      diamond: "#b9f2ff",
    },
    progress: {
      low: "#e74c3c",
      medium: "#f39c12",
      high: "#2ecc71",
    },
  },

  naics: {
    general: "#95a5a6",
    education: "#9b59b6",
    technology: "#3498db",
    healthcare: "#e74c3c",
    finance: "#27ae60",
    retail: "#e67e22",
    manufacturing: "#34495e",
    services: "#1abc9c",
  },
};

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
