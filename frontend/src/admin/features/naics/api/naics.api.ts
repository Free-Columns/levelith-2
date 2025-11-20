/**
 * API client methods for NAICS feature
 *
 * @module admin/features/naics/api
 */

import { api } from '@/lib/api'
import type {
  NAICS,
  CreateNAICSPayload,
  UpdateNAICSPayload,
  NAICSFilterOptions,
  NAICSStats,
  NAICSNode,
} from '../types/naics.types'
import type { PaginatedResponse, ListQueryParams } from '@/admin/types/common.types'

/**
 * API endpoints for NAICS
 */
const ENDPOINTS = {
  NAICS: '/naics',
  NAICS_BY_ID: (id: string) => `/naics/${id}`,
  NAICS_BY_CODE: (code: string) => `/naics/code/${code}`,
  NAICS_STATS: '/naics/stats',
  NAICS_HIERARCHY: '/naics/hierarchy',
  NAICS_SEARCH: '/naics/search',
} as const

/**
 * Fetch paginated list of NAICS codes
 *
 * @param params - Query parameters (pagination, search, filters)
 * @returns Paginated NAICS list
 */
export async function getNAICSCodes(
  params?: ListQueryParams & NAICSFilterOptions
): Promise<PaginatedResponse<NAICS>> {
  return api.get<PaginatedResponse<NAICS>>(ENDPOINTS.NAICS, { params })
}

/**
 * Fetch single NAICS by ID
 *
 * @param id - NAICS ID
 * @returns NAICS entity
 */
export async function getNAICSById(id: string): Promise<NAICS> {
  return api.get<NAICS>(ENDPOINTS.NAICS_BY_ID(id))
}

/**
 * Fetch single NAICS by code
 *
 * @param code - NAICS code (6 digits)
 * @returns NAICS entity
 */
export async function getNAICSByCode(code: string): Promise<NAICS> {
  return api.get<NAICS>(ENDPOINTS.NAICS_BY_CODE(code))
}

/**
 * Search NAICS codes by title/description
 *
 * @param query - Search query
 * @param params - Additional query parameters
 * @returns Matching NAICS codes
 */
export async function searchNAICS(
  query: string,
  params?: Partial<ListQueryParams>
): Promise<PaginatedResponse<NAICS>> {
  return api.get<PaginatedResponse<NAICS>>(ENDPOINTS.NAICS_SEARCH, {
    params: { q: query, ...params },
  })
}

/**
 * Fetch NAICS hierarchy tree
 *
 * @param rootCode - Optional root code to start from
 * @returns NAICS hierarchy tree
 */
export async function getNAICSHierarchy(rootCode?: string): Promise<NAICSNode[]> {
  return api.get<NAICSNode[]>(ENDPOINTS.NAICS_HIERARCHY, {
    params: rootCode ? { root: rootCode } : undefined,
  })
}

/**
 * Create new NAICS code (admin only)
 *
 * @param data - NAICS creation payload
 * @returns Created NAICS entity
 */
export async function createNAICS(data: CreateNAICSPayload): Promise<NAICS> {
  return api.post<NAICS>(ENDPOINTS.NAICS, data)
}

/**
 * Update existing NAICS (tags, category, notes only)
 *
 * @param id - NAICS ID
 * @param data - NAICS update payload
 * @returns Updated NAICS entity
 */
export async function updateNAICS(id: string, data: UpdateNAICSPayload): Promise<NAICS> {
  return api.patch<NAICS>(ENDPOINTS.NAICS_BY_ID(id), data)
}

/**
 * Delete NAICS code (soft delete)
 *
 * @param id - NAICS ID
 * @returns Deletion confirmation
 */
export async function deleteNAICS(id: string): Promise<{ success: boolean; message: string }> {
  return api.delete<{ success: boolean; message: string }>(ENDPOINTS.NAICS_BY_ID(id))
}

/**
 * Fetch NAICS statistics
 *
 * @returns NAICS statistics
 */
export async function getNAICSStats(): Promise<NAICSStats> {
  return api.get<NAICSStats>(ENDPOINTS.NAICS_STATS)
}
