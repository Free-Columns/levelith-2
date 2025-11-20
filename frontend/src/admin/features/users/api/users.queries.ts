/**
 * React Query hooks for Users feature (Queries)
 *
 * @module admin/features/users/api/users.queries
 *
 * Provides React Query hooks for fetching user data with automatic:
 * - Caching
 * - Background refetching
 * - Loading and error states
 * - Pagination support
 */

import { useQuery, UseQueryResult } from '@tanstack/react-query'
import { getUsers, getUserById, getUserStats } from './users.api'
import type { User, UserFilterOptions, UserStats } from '../types/user.types'
import type { PaginatedResponse, ListQueryParams } from '@/admin/types/common.types'

/**
 * Query keys for user-related queries
 * Organized hierarchically for easy invalidation
 */
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters?: ListQueryParams & UserFilterOptions) => [...userKeys.lists(), { filters }] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
  stats: () => [...userKeys.all, 'stats'] as const,
} as const

/**
 * Hook to fetch paginated list of users
 *
 * Features:
 * - Server-side pagination
 * - Search by username/email
 * - Filter by active/verified status
 * - Automatic refetching on param changes
 *
 * @param params - Query parameters (pagination, search, filters)
 * @returns Query result with paginated users
 *
 * @example
 * ```tsx
 * const { data, isLoading, error } = useUsers({
 *   page: 1,
 *   pageSize: 50,
 *   search: 'john',
 *   isActive: true
 * })
 * ```
 */
export function useUsers(
  params?: ListQueryParams & UserFilterOptions
): UseQueryResult<PaginatedResponse<User>, Error> {
  return useQuery({
    queryKey: userKeys.list(params),
    queryFn: () => getUsers(params),
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

/**
 * Hook to fetch single user by ID
 *
 * Features:
 * - Automatic caching by user ID
 * - Returns user with experiences
 * - Refetches on window focus
 *
 * @param id - User ID
 * @param options - Additional query options
 * @returns Query result with user details
 *
 * @example
 * ```tsx
 * const { data: user, isLoading } = useUser(userId, {
 *   enabled: !!userId  // Only fetch if ID exists
 * })
 * ```
 */
export function useUser(
  id: string,
  options?: { enabled?: boolean }
): UseQueryResult<User, Error> {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => getUserById(id),
    enabled: options?.enabled ?? !!id,
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

/**
 * Hook to fetch user statistics
 *
 * Features:
 * - Dashboard metrics (total, active, verified, recent)
 * - Automatic background refetching
 * - Long stale time (data doesn't change frequently)
 *
 * @returns Query result with user statistics
 *
 * @example
 * ```tsx
 * const { data: stats } = useUserStats()
 *
 * console.log(stats.totalUsers)    // 150
 * console.log(stats.activeUsers)   // 142
 * console.log(stats.recentSignups) // 12
 * ```
 */
export function useUserStats(): UseQueryResult<UserStats, Error> {
  return useQuery({
    queryKey: userKeys.stats(),
    queryFn: getUserStats,
    staleTime: 1000 * 60 * 10, // 10 minutes (stats don't change often)
    refetchInterval: 1000 * 60 * 5, // Refetch every 5 minutes in background
  })
}

/**
 * Hook to fetch users with custom query configuration
 *
 * Useful for advanced scenarios where you need more control over
 * the query behavior (retry logic, error handling, etc.)
 *
 * @param params - Query parameters
 * @param queryOptions - Custom React Query options
 * @returns Query result with users
 *
 * @example
 * ```tsx
 * const { data } = useUsersQuery(
 *   { page: 1, pageSize: 10 },
 *   {
 *     retry: 3,
 *     retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
 *     onError: (error) => toast.error('Failed to fetch users')
 *   }
 * )
 * ```
 */
export function useUsersQuery(
  params?: ListQueryParams & UserFilterOptions,
  queryOptions?: {
    retry?: number | boolean
    retryDelay?: number | ((attemptIndex: number) => number)
    onError?: (error: Error) => void
    onSuccess?: (data: PaginatedResponse<User>) => void
  }
): UseQueryResult<PaginatedResponse<User>, Error> {
  return useQuery({
    queryKey: userKeys.list(params),
    queryFn: () => getUsers(params),
    staleTime: 1000 * 60 * 5,
    ...queryOptions,
  })
}
