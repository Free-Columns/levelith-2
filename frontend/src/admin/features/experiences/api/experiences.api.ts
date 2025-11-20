/**
 * API client methods for Experiences feature
 *
 * @module admin/features/experiences/api
 */

import { api } from '@/lib/api'
import type {
  Experience,
  CreateExperiencePayload,
  UpdateExperiencePayload,
  ExperienceFilterOptions,
  ExperienceStats,
} from '../types/experience.types'
import type { PaginatedResponse, ListQueryParams } from '@/admin/types/common.types'

/**
 * API endpoints for experiences
 */
const ENDPOINTS = {
  EXPERIENCES: '/experiences',
  EXPERIENCE_BY_ID: (id: string) => `/experiences/${id}`,
  EXPERIENCE_STATS: '/experiences/stats',
  USER_EXPERIENCES: (userId: string) => `/users/${userId}/experiences`,
} as const

/**
 * Fetch paginated list of experiences
 *
 * @param params - Query parameters (pagination, search, filters)
 * @returns Paginated experience list
 */
export async function getExperiences(
  params?: ListQueryParams & ExperienceFilterOptions
): Promise<PaginatedResponse<Experience>> {
  return api.get<PaginatedResponse<Experience>>(ENDPOINTS.EXPERIENCES, { params })
}

/**
 * Fetch single experience by ID
 *
 * @param id - Experience ID
 * @returns Experience entity
 */
export async function getExperienceById(id: string): Promise<Experience> {
  return api.get<Experience>(ENDPOINTS.EXPERIENCE_BY_ID(id))
}

/**
 * Fetch experiences for a specific user
 *
 * @param userId - User ID
 * @param params - Query parameters
 * @returns Paginated experience list for user
 */
export async function getExperiencesByUser(
  userId: string,
  params?: ListQueryParams
): Promise<PaginatedResponse<Experience>> {
  return api.get<PaginatedResponse<Experience>>(ENDPOINTS.USER_EXPERIENCES(userId), { params })
}

/**
 * Create new experience
 *
 * @param data - Experience creation payload (polymorphic)
 * @returns Created experience entity
 */
export async function createExperience(data: CreateExperiencePayload): Promise<Experience> {
  return api.post<Experience>(ENDPOINTS.EXPERIENCES, data)
}

/**
 * Update existing experience
 *
 * @param id - Experience ID
 * @param data - Experience update payload (polymorphic)
 * @returns Updated experience entity
 */
export async function updateExperience(id: string, data: UpdateExperiencePayload): Promise<Experience> {
  return api.patch<Experience>(ENDPOINTS.EXPERIENCE_BY_ID(id), data)
}

/**
 * Delete experience
 *
 * @param id - Experience ID
 * @returns Deletion confirmation
 */
export async function deleteExperience(id: string): Promise<{ success: boolean; message: string }> {
  return api.delete<{ success: boolean; message: string }>(ENDPOINTS.EXPERIENCE_BY_ID(id))
}

/**
 * Fetch experience statistics
 *
 * @returns Experience statistics
 */
export async function getExperienceStats(): Promise<ExperienceStats> {
  return api.get<ExperienceStats>(ENDPOINTS.EXPERIENCE_STATS)
}

/**
 * Bulk delete experiences
 *
 * @param ids - Array of experience IDs
 * @returns Deletion result
 */
export async function bulkDeleteExperiences(
  ids: string[]
): Promise<{ success: boolean; deleted: number; failed: number }> {
  return api.post<{ success: boolean; deleted: number; failed: number }>(
    `${ENDPOINTS.EXPERIENCES}/bulk-delete`,
    { ids }
  )
}
