/**
 * API-specific types and interfaces
 *
 * @module admin/types/api
 */

/**
 * HTTP methods
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

/**
 * API endpoint configuration
 */
export interface ApiEndpoint {
  method: HttpMethod
  path: string
  authenticated?: boolean
}

/**
 * API request options
 */
export interface ApiRequestOptions {
  params?: Record<string, any>
  data?: any
  headers?: Record<string, string>
  timeout?: number
}

/**
 * React Query options
 */
export interface QueryOptions {
  enabled?: boolean
  refetchInterval?: number
  staleTime?: number
  cacheTime?: number
}

/**
 * Mutation options
 */
export interface MutationOptions {
  onSuccess?: (data: any) => void
  onError?: (error: any) => void
  onSettled?: () => void
}
