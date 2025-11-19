/**
 * API Service Abstraction Layer
 *
 * Provides a unified interface for data operations that can work with
 * either mock data (local) or real backend API (server).
 *
 * This service can be easily switched between data sources without
 * changing component code.
 */

import axios from "axios";

// API Configuration
// Production backend URL from Render deployment
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || "https://levelith-backend.onrender.com/api/v1",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
};

// Create axios instance
const apiClient = axios.create(API_CONFIG);

// Request interceptor - add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem("access_token");
        window.location.href = "/login";
      } else if (status === 403) {
        console.error("Forbidden:", data.message || "Access denied");
      } else if (status === 404) {
        console.error("Not found:", data.message || "Resource not found");
      } else if (status >= 500) {
        console.error("Server error:", data.message || "Internal server error");
      }
    } else if (error.request) {
      // Request made but no response
      console.error("Network error: No response from server");
    } else {
      // Error in request setup
      console.error("Request error:", error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * API Service Class
 *
 * Provides methods for all backend API operations.
 * Can be used directly or through DataSourceContext.
 */
class APIService {
  // ==================== AUTHENTICATION ====================

  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Created user object
   */
  async register(userData) {
    const response = await apiClient.post("/auth/register", userData);
    return response.data;
  }

  /**
   * Login user
   * @param {string} username - Username or email
   * @param {string} password - Password
   * @returns {Promise<Object>} Token and user data
   */
  async login(username, password) {
    const response = await apiClient.post("/auth/login", {
      username,
      password,
    });

    // Store token
    if (response.data.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
      if (response.data.refresh_token) {
        localStorage.setItem("refresh_token", response.data.refresh_token);
      }
    }

    return response.data;
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      await apiClient.post("/auth/logout");
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  }

  /**
   * Refresh access token
   * @returns {Promise<Object>} New token data
   */
  async refreshToken() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
      throw new Error("No refresh token available");
    }

    const response = await apiClient.post("/auth/refresh", {
      refresh_token: refreshToken,
    });

    if (response.data.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
    }

    return response.data;
  }

  // ==================== USERS ====================

  /**
   * Get list of users
   * @param {Object} filters - Filter parameters
   * @returns {Promise<Object>} Paginated user list
   */
  async getUsers(filters = {}) {
    const params = {
      page: filters.page || 1,
      page_size: filters.limit || 20,
      search: filters.search,
      active_only: filters.active_only,
      verified_only: filters.verified_only,
    };

    // Remove undefined params
    Object.keys(params).forEach((key) => {
      if (params[key] === undefined) delete params[key];
    });

    const response = await apiClient.get("/users", { params });
    return {
      total: response.data.total,
      limit: response.data.page_size,
      offset: (response.data.page - 1) * response.data.page_size,
      results: response.data.items || response.data.results || [],
    };
  }

  /**
   * Get user by ID
   * @param {string} userId - User ID
   * @returns {Promise<Object>} User object
   */
  async getUserById(userId) {
    const response = await apiClient.get(`/users/${userId}`);
    return response.data;
  }

  /**
   * Create new user
   * @param {Object} userData - User data
   * @returns {Promise<Object>} Created user object
   */
  async createUser(userData) {
    const response = await apiClient.post("/users", userData);
    return response.data;
  }

  /**
   * Update user
   * @param {string} userId - User ID
   * @param {Object} updates - User updates
   * @returns {Promise<Object>} Updated user object
   */
  async updateUser(userId, updates) {
    const response = await apiClient.put(`/users/${userId}`, updates);
    return response.data;
  }

  /**
   * Delete user
   * @param {string} userId - User ID
   * @returns {Promise<Object>} Success message
   */
  async deleteUser(userId) {
    const response = await apiClient.delete(`/users/${userId}`);
    return response.data;
  }

  // ==================== EXPERIENCES ====================

  /**
   * Get list of experiences
   * @param {Object} filters - Filter parameters
   * @returns {Promise<Object>} Paginated experience list
   */
  async getExperiences(filters = {}) {
    const params = {
      page: filters.page || 1,
      page_size: filters.limit || 20,
      user_id: filters.user_id,
      category: filters.category,
      experience_type: filters.experience_type,
      active_only: filters.active_only,
      naics_code: filters.naics_code,
      search: filters.search,
    };

    // Remove undefined params
    Object.keys(params).forEach((key) => {
      if (params[key] === undefined) delete params[key];
    });

    const response = await apiClient.get("/experiences", { params });
    return {
      total: response.data.total,
      limit: response.data.page_size,
      offset: (response.data.page - 1) * response.data.page_size,
      results: response.data.items || response.data.results || [],
    };
  }

  /**
   * Get experience by ID
   * @param {string} experienceId - Experience ID
   * @returns {Promise<Object>} Experience object
   */
  async getExperienceById(experienceId) {
    const response = await apiClient.get(`/experiences/${experienceId}`);
    return response.data;
  }

  /**
   * Create new experience
   * @param {Object} experienceData - Experience data
   * @returns {Promise<Object>} Created experience object
   */
  async createExperience(experienceData) {
    const response = await apiClient.post("/experiences", experienceData);
    return response.data;
  }

  /**
   * Update experience
   * @param {string} experienceId - Experience ID
   * @param {Object} updates - Experience updates
   * @returns {Promise<Object>} Updated experience object
   */
  async updateExperience(experienceId, updates) {
    const response = await apiClient.put(`/experiences/${experienceId}`, updates);
    return response.data;
  }

  /**
   * Delete experience
   * @param {string} experienceId - Experience ID
   * @returns {Promise<Object>} Success message
   */
  async deleteExperience(experienceId) {
    const response = await apiClient.delete(`/experiences/${experienceId}`);
    return response.data;
  }

  // ==================== NAICS CODES ====================

  /**
   * Get list of NAICS codes
   * @param {Object} filters - Filter parameters
   * @returns {Promise<Array>} NAICS codes array
   */
  async getNAICSCodes(filters = {}) {
    const params = {
      search: filters.search,
      industry: filters.industry,
    };

    // Remove undefined params
    Object.keys(params).forEach((key) => {
      if (params[key] === undefined) delete params[key];
    });

    const response = await apiClient.get("/naics", { params });
    return response.data;
  }

  /**
   * Get NAICS code by code
   * @param {string} code - NAICS code
   * @returns {Promise<Object>} NAICS code object
   */
  async getNAICSByCode(code) {
    const response = await apiClient.get(`/naics/${code}`);
    return response.data;
  }

  // ==================== STATISTICS ====================

  /**
   * Get statistics
   * @returns {Promise<Object>} Statistics object
   */
  async getStats() {
    const response = await apiClient.get("/stats");
    return response.data;
  }

  // ==================== BULK OPERATIONS ====================

  /**
   * Bulk create experiences
   * @param {Array} experiences - Array of experience objects
   * @returns {Promise<Object>} Bulk operation result
   */
  async bulkCreateExperiences(experiences) {
    const response = await apiClient.post("/experiences/bulk", {
      experiences,
    });
    return response.data;
  }

  /**
   * Bulk delete experiences
   * @param {Array} experienceIds - Array of experience IDs
   * @returns {Promise<Object>} Bulk operation result
   */
  async bulkDeleteExperiences(experienceIds) {
    const response = await apiClient.delete("/experiences/bulk", {
      data: { ids: experienceIds },
    });
    return response.data;
  }

  /**
   * Bulk update users
   * @param {Array} updates - Array of user update objects
   * @returns {Promise<Object>} Bulk operation result
   */
  async bulkUpdateUsers(updates) {
    const response = await apiClient.put("/users/bulk", {
      updates,
    });
    return response.data;
  }

  // ==================== EXPORT/IMPORT ====================

  /**
   * Export users to CSV
   * @param {Object} filters - Filter parameters
   * @returns {Promise<Blob>} CSV file blob
   */
  async exportUsersCSV(filters = {}) {
    const response = await apiClient.get("/users/export/csv", {
      params: filters,
      responseType: "blob",
    });
    return response.data;
  }

  /**
   * Export experiences to CSV
   * @param {Object} filters - Filter parameters
   * @returns {Promise<Blob>} CSV file blob
   */
  async exportExperiencesCSV(filters = {}) {
    const response = await apiClient.get("/experiences/export/csv", {
      params: filters,
      responseType: "blob",
    });
    return response.data;
  }

  /**
   * Import users from CSV
   * @param {File} file - CSV file
   * @returns {Promise<Object>} Import result
   */
  async importUsersCSV(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post("/users/import/csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }

  /**
   * Import experiences from CSV
   * @param {File} file - CSV file
   * @returns {Promise<Object>} Import result
   */
  async importExperiencesCSV(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post("/experiences/import/csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }
}

// Export singleton instance
const apiService = new APIService();
export default apiService;
