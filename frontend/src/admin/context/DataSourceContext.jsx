/**
 * Data Source Context
 *
 * Manages data source (local mock vs server API) and provides
 * data access methods throughout the application.
 */

import React, { createContext, useContext, useState, useCallback } from "react";
import {
  mockUsers,
  mockExperiences,
  naicsCodes,
  generateMockUsers,
  generateMockExperiences,
  getStatistics,
} from "../data/mockData";
import apiService from "../services/apiService";

const DataSourceContext = createContext();

export const DATA_SOURCES = {
  LOCAL: "local",
  SERVER: "server",
};

export const DataSourceProvider = ({ children }) => {
  const [dataSource, setDataSource] = useState(DATA_SOURCES.LOCAL);
  const [localUsers, setLocalUsers] = useState(mockUsers);
  const [localExperiences, setLocalExperiences] = useState(mockExperiences);

  // Data Source Switcher
  const switchDataSource = useCallback((source) => {
    setDataSource(source);
  }, []);

  // ==================== USER CRUD OPERATIONS ====================

  const getUsers = useCallback(
    async (filters = {}) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        let filtered = [...localUsers];

        if (filters.active_only) {
          filtered = filtered.filter((u) => u.is_active);
        }
        if (filters.verified_only) {
          filtered = filtered.filter((u) => u.is_verified);
        }
        if (filters.search) {
          const search = filters.search.toLowerCase();
          filtered = filtered.filter(
            (u) =>
              u.username.toLowerCase().includes(search) ||
              u.email.toLowerCase().includes(search) ||
              u.profile_data.display_name.toLowerCase().includes(search)
          );
        }

        const offset = filters.offset || 0;
        const limit = filters.limit || 20;

        return {
          total: filtered.length,
          limit,
          offset,
          results: filtered.slice(offset, offset + limit),
        };
      } else {
        // Server API call
        return await apiService.getUsers(filters);
      }
    },
    [dataSource, localUsers]
  );

  const getUserById = useCallback(
    async (userId) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        const user = localUsers.find((u) => u.id === userId);
        if (!user) {
          throw new Error("User not found");
        }
        return user;
      } else {
        // Server API call
        return await apiService.getUserById(userId);
      }
    },
    [dataSource, localUsers]
  );

  const createUser = useCallback(
    async (userData) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        const newUser = {
          id: `user_${Math.random().toString(36).substr(2, 9)}`,
          ...userData,
          password_hash: "hashed_password_placeholder",
          experiences: [],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          last_login: null,
        };
        setLocalUsers((prev) => [...prev, newUser]);
        return newUser;
      } else {
        // Server API call
        return await apiService.createUser(userData);
      }
    },
    [dataSource]
  );

  const updateUser = useCallback(
    async (userId, updates) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        setLocalUsers((prev) =>
          prev.map((user) =>
            user.id === userId
              ? { ...user, ...updates, updated_at: new Date().toISOString() }
              : user
          )
        );
        const updatedUser = localUsers.find((u) => u.id === userId);
        return { ...updatedUser, ...updates };
      } else {
        // Server API call
        return await apiService.updateUser(userId, updates);
      }
    },
    [dataSource, localUsers]
  );

  const deleteUser = useCallback(
    async (userId) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        setLocalUsers((prev) => prev.filter((user) => user.id !== userId));
        // Also delete user's experiences
        setLocalExperiences((prev) =>
          prev.filter((exp) => exp.user_id !== userId)
        );
        return { message: "User deleted successfully" };
      } else {
        // Server API call
        return await apiService.deleteUser(userId);
      }
    },
    [dataSource]
  );

  // ==================== EXPERIENCE CRUD OPERATIONS ====================

  const getExperiences = useCallback(
    async (filters = {}) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        let filtered = [...localExperiences];

        if (filters.user_id) {
          filtered = filtered.filter((e) => e.user_id === filters.user_id);
        }
        if (filters.category) {
          filtered = filtered.filter((e) => e.category === filters.category);
        }
        if (filters.experience_type) {
          filtered = filtered.filter(
            (e) => e.experience_type === filters.experience_type
          );
        }
        if (filters.active_only) {
          filtered = filtered.filter((e) => !e.end_date);
        }
        if (filters.naics_code) {
          filtered = filtered.filter((e) => e.naics_code === filters.naics_code);
        }
        if (filters.search) {
          const search = filters.search.toLowerCase();
          filtered = filtered.filter(
            (e) =>
              e.title.toLowerCase().includes(search) ||
              e.description.toLowerCase().includes(search)
          );
        }

        const offset = filters.offset || 0;
        const limit = filters.limit || 20;

        return {
          total: filtered.length,
          limit,
          offset,
          results: filtered.slice(offset, offset + limit),
        };
      } else {
        // Server API call
        return await apiService.getExperiences(filters);
      }
    },
    [dataSource, localExperiences]
  );

  const getExperienceById = useCallback(
    async (expId) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        const exp = localExperiences.find((e) => e.id === expId);
        if (!exp) {
          throw new Error("Experience not found");
        }
        return exp;
      } else {
        // Server API call
        return await apiService.getExperienceById(expId);
      }
    },
    [dataSource, localExperiences]
  );

  const createExperience = useCallback(
    async (expData) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        const newExp = {
          id: `exp_${Math.random().toString(36).substr(2, 9)}`,
          ...expData,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        setLocalExperiences((prev) => [...prev, newExp]);

        // Add to user's experience array
        setLocalUsers((prev) =>
          prev.map((user) =>
            user.id === newExp.user_id
              ? { ...user, experiences: [...user.experiences, newExp.id] }
              : user
          )
        );

        return newExp;
      } else {
        // Server API call
        return await apiService.createExperience(expData);
      }
    },
    [dataSource]
  );

  const updateExperience = useCallback(
    async (expId, updates) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        setLocalExperiences((prev) =>
          prev.map((exp) =>
            exp.id === expId
              ? { ...exp, ...updates, updated_at: new Date().toISOString() }
              : exp
          )
        );
        const updatedExp = localExperiences.find((e) => e.id === expId);
        return { ...updatedExp, ...updates };
      } else {
        // Server API call
        return await apiService.updateExperience(expId, updates);
      }
    },
    [dataSource, localExperiences]
  );

  const deleteExperience = useCallback(
    async (expId) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        const exp = localExperiences.find((e) => e.id === expId);
        if (exp) {
          // Remove from user's experience array
          setLocalUsers((prev) =>
            prev.map((user) =>
              user.id === exp.user_id
                ? {
                    ...user,
                    experiences: user.experiences.filter((id) => id !== expId),
                  }
                : user
            )
          );
        }
        setLocalExperiences((prev) => prev.filter((exp) => exp.id !== expId));
        return { message: "Experience deleted successfully" };
      } else {
        // Server API call
        return await apiService.deleteExperience(expId);
      }
    },
    [dataSource, localExperiences]
  );

  // ==================== NAICS OPERATIONS ====================

  const getNAICSCodes = useCallback(
    async (filters = {}) => {
      let filtered = [...naicsCodes];

      if (filters.search) {
        const search = filters.search.toLowerCase();
        filtered = filtered.filter(
          (n) =>
            n.code.includes(search) ||
            n.title.toLowerCase().includes(search) ||
            n.description.toLowerCase().includes(search)
        );
      }

      if (filters.industry) {
        filtered = filtered.filter((n) => n.industry === filters.industry);
      }

      return filtered;
    },
    []
  );

  const getNAICSByCode = useCallback(async (code) => {
    const naics = naicsCodes.find((n) => n.code === code);
    if (!naics) {
      throw new Error("NAICS code not found");
    }
    return naics;
  }, []);

  // ==================== STATISTICS ====================

  const getStats = useCallback(async () => {
    if (dataSource === DATA_SOURCES.LOCAL) {
      return getStatistics();
    } else {
      // Server API call
      return await apiService.getStats();
    }
  }, [dataSource]);

  // ==================== SEED DATABASE ====================

  const seedUsers = useCallback(
    async (userCount = 50) => {
      if (dataSource === DATA_SOURCES.LOCAL) {
        // For local data source, generate mock users
        const newUsers = generateMockUsers(userCount);
        const newExperiences = generateMockExperiences(userCount);
        setLocalUsers((prev) => [...prev, ...newUsers]);
        setLocalExperiences((prev) => [...prev, ...newExperiences]);
        return {
          success: true,
          message: `Successfully seeded ${userCount} users locally`,
          statistics: {
            users_created: userCount,
            experiences_created: newExperiences.length,
            average_experiences_per_user: (newExperiences.length / userCount).toFixed(1)
          }
        };
      } else {
        // Server API call
        return await apiService.seedUsers(userCount);
      }
    },
    [dataSource]
  );

  const value = {
    // Data source
    dataSource,
    switchDataSource,

    // User operations
    getUsers,
    getUserById,
    createUser,
    updateUser,
    deleteUser,
    seedUsers,

    // Experience operations
    getExperiences,
    getExperienceById,
    createExperience,
    updateExperience,
    deleteExperience,

    // NAICS operations
    getNAICSCodes,
    getNAICSByCode,

    // Statistics
    getStats,
  };

  return (
    <DataSourceContext.Provider value={value}>
      {children}
    </DataSourceContext.Provider>
  );
};

export const useDataSource = () => {
  const context = useContext(DataSourceContext);
  if (!context) {
    throw new Error("useDataSource must be used within DataSourceProvider");
  }
  return context;
};

export default DataSourceContext;
