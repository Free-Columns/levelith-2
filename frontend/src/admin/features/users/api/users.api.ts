/**
 * API client methods for Users feature
 *
 * @module admin/features/users/api
 */

import { api } from '@/lib/api'
import type { User, CreateUserPayload, UpdateUserPayload, UserFilterOptions, UserStats } from '../types/user.types'
import type { PaginatedResponse, ListQueryParams } from '@/admin/types/common.types'

/**
 * API endpoints for users
 */
const ENDPOINTS = {
  USERS: '/users',
  USER_BY_ID: (id: string) => `/users/${id}`,
  USER_STATS: '/users/stats',
} as const

/**
 * Fetch paginated list of users
 *
 * @param params - Query parameters (pagination, search, filters)
 * @returns Paginated user list
 */
export async function getUsers(
  params?: ListQueryParams & UserFilterOptions
): Promise<PaginatedResponse<User>> {
  return api.get<PaginatedResponse<User>>(ENDPOINTS.USERS, { params })
}

/**
 * Fetch single user by ID
 *
 * @param id - User ID
 * @returns User entity
 */
export async function getUserById(id: string): Promise<User> {
  return api.get<User>(ENDPOINTS.USER_BY_ID(id))
}

/**
 * Create new user
 *
 * @param data - User creation payload
 * @returns Created user entity
 */
export async function createUser(data: CreateUserPayload): Promise<User> {
  return api.post<User>(ENDPOINTS.USERS, data)
}

/**
 * Update existing user
 *
 * @param id - User ID
 * @param data - User update payload
 * @returns Updated user entity
 */
export async function updateUser(id: string, data: UpdateUserPayload): Promise<User> {
  return api.patch<User>(ENDPOINTS.USER_BY_ID(id), data)
}

/**
 * Delete user
 *
 * @param id - User ID
 * @returns Deletion confirmation
 */
export async function deleteUser(id: string): Promise<{ success: boolean; message: string }> {
  return api.delete<{ success: boolean; message: string }>(ENDPOINTS.USER_BY_ID(id))
}

/**
 * Fetch user statistics
 *
 * @returns User statistics
 */
export async function getUserStats(): Promise<UserStats> {
  return api.get<UserStats>(ENDPOINTS.USER_STATS)
}

/**
 * Bulk delete users
 *
 * @param ids - Array of user IDs
 * @returns Deletion result
 */
export async function bulkDeleteUsers(
  ids: string[]
): Promise<{ success: boolean; deleted: number; failed: number }> {
  return api.post<{ success: boolean; deleted: number; failed: number }>(`${ENDPOINTS.USERS}/bulk-delete`, { ids })
}
