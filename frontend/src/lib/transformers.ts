/**
 * API Response Transformation Utilities
 *
 * @module lib/transformers
 *
 * Provides utilities for transforming API responses between snake_case (backend)
 * and camelCase (frontend) naming conventions.
 *
 * Features:
 * - Deep object transformation
 * - Array handling
 * - Nested object support
 * - Type preservation
 * - Null/undefined handling
 */

/**
 * Convert string from snake_case to camelCase
 *
 * @param str - String in snake_case format
 * @returns String in camelCase format
 *
 * @example
 * snakeToCamel('user_name') // 'userName'
 * snakeToCamel('is_active') // 'isActive'
 * snakeToCamel('created_at') // 'createdAt'
 */
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
}

/**
 * Convert string from camelCase to snake_case
 *
 * @param str - String in camelCase format
 * @returns String in snake_case format
 *
 * @example
 * camelToSnake('userName') // 'user_name'
 * camelToSnake('isActive') // 'is_active'
 * camelToSnake('createdAt') // 'created_at'
 */
export function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
}

/**
 * Check if value is a plain object (not array, not null, not Date, etc.)
 *
 * @param obj - Value to check
 * @returns True if value is a plain object
 */
function isPlainObject(obj: any): boolean {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    !Array.isArray(obj) &&
    !(obj instanceof Date) &&
    !(obj instanceof RegExp)
  )
}

/**
 * Transform object keys from snake_case to camelCase
 *
 * Recursively transforms all keys in nested objects and arrays.
 * Preserves non-object values and special types (Date, null, etc.).
 *
 * @param obj - Object with snake_case keys
 * @returns Object with camelCase keys
 *
 * @example
 * ```typescript
 * const input = {
 *   user_name: 'john',
 *   is_active: true,
 *   profile_data: {
 *     first_name: 'John',
 *     last_name: 'Doe'
 *   },
 *   created_at: '2025-01-01T00:00:00Z'
 * }
 *
 * const output = keysToCamel(input)
 * // {
 * //   userName: 'john',
 * //   isActive: true,
 * //   profileData: {
 * //     firstName: 'John',
 * //     lastName: 'Doe'
 * //   },
 * //   createdAt: '2025-01-01T00:00:00Z'
 * // }
 * ```
 */
export function keysToCamel<T = any>(obj: any): T {
  if (Array.isArray(obj)) {
    return obj.map((item) => keysToCamel(item)) as T
  }

  if (!isPlainObject(obj)) {
    return obj
  }

  const result: any = {}

  for (const [key, value] of Object.entries(obj)) {
    const camelKey = snakeToCamel(key)
    result[camelKey] = isPlainObject(value) || Array.isArray(value) ? keysToCamel(value) : value
  }

  return result as T
}

/**
 * Transform object keys from camelCase to snake_case
 *
 * Recursively transforms all keys in nested objects and arrays.
 * Preserves non-object values and special types (Date, null, etc.).
 *
 * @param obj - Object with camelCase keys
 * @returns Object with snake_case keys
 *
 * @example
 * ```typescript
 * const input = {
 *   userName: 'john',
 *   isActive: true,
 *   profileData: {
 *     firstName: 'John',
 *     lastName: 'Doe'
 *   }
 * }
 *
 * const output = keysToSnake(input)
 * // {
 * //   user_name: 'john',
 * //   is_active: true,
 * //   profile_data: {
 * //     first_name: 'John',
 * //     last_name: 'Doe'
 * //   }
 * // }
 * ```
 */
export function keysToSnake<T = any>(obj: any): T {
  if (Array.isArray(obj)) {
    return obj.map((item) => keysToSnake(item)) as T
  }

  if (!isPlainObject(obj)) {
    return obj
  }

  const result: any = {}

  for (const [key, value] of Object.entries(obj)) {
    const snakeKey = camelToSnake(key)
    result[snakeKey] = isPlainObject(value) || Array.isArray(value) ? keysToSnake(value) : value
  }

  return result as T
}

/**
 * Transform paginated response from backend format to frontend format
 *
 * Backend format:
 * - items: array of data
 * - total, page, page_size, total_pages
 *
 * Frontend format:
 * - data: array of transformed data
 * - total, page, pageSize, totalPages
 *
 * @param response - Backend paginated response
 * @returns Frontend paginated response
 *
 * @example
 * ```typescript
 * const backendResponse = {
 *   items: [{ user_name: 'john', is_active: true }],
 *   total: 100,
 *   page: 1,
 *   page_size: 50,
 *   total_pages: 2
 * }
 *
 * const frontendResponse = transformPaginatedResponse(backendResponse)
 * // {
 * //   data: [{ userName: 'john', isActive: true }],
 * //   total: 100,
 * //   page: 1,
 * //   pageSize: 50,
 * //   totalPages: 2
 * // }
 * ```
 */
export function transformPaginatedResponse<T = any>(response: any): {
  data: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
} {
  // Handle both formats: { items, ... } or direct array
  const items = response.items || response.data || response

  return {
    data: Array.isArray(items) ? items.map((item: any) => keysToCamel<T>(item)) : [],
    total: response.total || 0,
    page: response.page || 1,
    pageSize: response.page_size || response.pageSize || 50,
    totalPages: response.total_pages || response.totalPages || 1,
  }
}
