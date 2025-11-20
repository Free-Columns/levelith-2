/**
 * Common types used across the admin dashboard
 *
 * @module admin/types/common
 */

/**
 * Standard API response wrapper
 */
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

/**
 * Paginated API response
 */
export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

/**
 * Standard error response from API
 */
export interface ApiError {
  message: string
  code?: string
  details?: Record<string, any>
}

/**
 * Common query parameters for list endpoints
 */
export interface ListQueryParams {
  page?: number
  pageSize?: number
  search?: string
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

/**
 * Status types for entities
 */
export type EntityStatus = 'active' | 'inactive' | 'deleted'

/**
 * Date range filter
 */
export interface DateRange {
  from?: string
  to?: string
}

/**
 * Generic filter options
 */
export interface FilterOptions {
  search?: string
  status?: EntityStatus
  dateRange?: DateRange
  [key: string]: any
}
