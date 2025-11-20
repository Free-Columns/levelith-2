/**
 * Composite hook for Users feature
 *
 * @module admin/features/users/hooks/useUsers
 *
 * Provides a unified interface for all user-related operations:
 * - Fetching users (with pagination, search, filters)
 * - Creating, updating, deleting users
 * - Bulk operations
 * - Statistics
 *
 * This hook combines queries and mutations into a single, easy-to-use API
 * that handles all the complexity of state management, caching, and updates.
 */

import { useState, useCallback, useMemo } from 'react'
import {
  useUsers as useUsersQuery,
  useUser,
  useUserStats,
  userKeys,
} from '../api/users.queries'
import {
  useCreateUser,
  useUpdateUser,
  useDeleteUser,
  useBulkDeleteUsers,
  useToggleUserActive,
} from '../api/users.mutations'
import type { User, UserFilterOptions, CreateUserPayload, UpdateUserPayload } from '../types/user.types'
import type { ListQueryParams } from '@/admin/types/common.types'

/**
 * Options for useUsers hook
 */
export interface UseUsersOptions {
  /**
   * Initial page number (default: 1)
   */
  initialPage?: number

  /**
   * Initial page size (default: 50)
   */
  initialPageSize?: number

  /**
   * Initial search query
   */
  initialSearch?: string

  /**
   * Initial filter options
   */
  initialFilters?: UserFilterOptions

  /**
   * Callback when user is created
   */
  onUserCreated?: (user: User) => void

  /**
   * Callback when user is updated
   */
  onUserUpdated?: (user: User) => void

  /**
   * Callback when user is deleted
   */
  onUserDeleted?: () => void

  /**
   * Callback when error occurs
   */
  onError?: (error: Error) => void
}

/**
 * Return type of useUsers hook
 */
export interface UseUsersReturn {
  // Query state
  users: User[]
  isLoading: boolean
  isError: boolean
  error: Error | null
  totalUsers: number
  totalPages: number

  // Pagination state
  page: number
  pageSize: number
  setPage: (page: number) => void
  setPageSize: (size: number) => void
  nextPage: () => void
  previousPage: () => void
  goToFirstPage: () => void
  goToLastPage: () => void

  // Search and filter state
  search: string
  setSearch: (search: string) => void
  filters: UserFilterOptions
  setFilters: (filters: UserFilterOptions) => void
  clearFilters: () => void

  // Sorting state
  sortBy: string
  sortOrder: 'asc' | 'desc'
  setSorting: (field: string, order: 'asc' | 'desc') => void

  // Mutations
  createUser: (data: CreateUserPayload) => Promise<User>
  updateUser: (id: string, data: UpdateUserPayload) => Promise<User>
  deleteUser: (id: string) => Promise<void>
  bulkDeleteUsers: (ids: string[]) => Promise<void>
  toggleUserActive: (id: string, isActive: boolean) => Promise<User>

  // Mutation states
  isCreating: boolean
  isUpdating: boolean
  isDeleting: boolean

  // Refetch
  refetch: () => void
}

/**
 * Unified hook for user management
 *
 * Provides a complete interface for managing users with pagination,
 * search, filtering, and CRUD operations.
 *
 * @param options - Configuration options
 * @returns User management interface
 *
 * @example
 * ```tsx
 * function UsersPage() {
 *   const {
 *     users,
 *     isLoading,
 *     page,
 *     pageSize,
 *     totalPages,
 *     setPage,
 *     search,
 *     setSearch,
 *     createUser,
 *     deleteUser,
 *     isCreating,
 *   } = useUsers({
 *     initialPageSize: 25,
 *     onUserCreated: (user) => {
 *       toast.success(`User ${user.username} created!`)
 *     },
 *     onError: (error) => {
 *       toast.error(error.message)
 *     }
 *   })
 *
 *   // Use the data and functions in your component...
 * }
 * ```
 */
export function useUsers(options: UseUsersOptions = {}): UseUsersReturn {
  // Destructure options with defaults
  const {
    initialPage = 1,
    initialPageSize = 50,
    initialSearch = '',
    initialFilters = {},
    onUserCreated,
    onUserUpdated,
    onUserDeleted,
    onError,
  } = options

  // Local state for pagination, search, and filters
  const [page, setPage] = useState(initialPage)
  const [pageSize, setPageSize] = useState(initialPageSize)
  const [search, setSearch] = useState(initialSearch)
  const [filters, setFilters] = useState<UserFilterOptions>(initialFilters)
  const [sortBy, setSortBy] = useState('createdAt')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  // Build query params
  const queryParams = useMemo<ListQueryParams & UserFilterOptions>(
    () => ({
      page,
      pageSize,
      search: search || undefined,
      sortBy,
      sortOrder,
      ...filters,
    }),
    [page, pageSize, search, sortBy, sortOrder, filters]
  )

  // Fetch users query
  const usersQuery = useUsersQuery(queryParams)

  // Mutations
  const createMutation = useCreateUser({
    onSuccess: onUserCreated,
    onError,
  })

  const updateMutation = useUpdateUser({
    onSuccess: onUserUpdated,
    onError,
  })

  const deleteMutation = useDeleteUser({
    onSuccess: onUserDeleted,
    onError,
  })

  const bulkDeleteMutation = useBulkDeleteUsers({
    onSuccess: () => {
      onUserDeleted?.()
    },
    onError,
  })

  const toggleActiveMutation = useToggleUserActive({
    onSuccess: onUserUpdated,
    onError,
  })

  // Pagination handlers
  const nextPage = useCallback(() => {
    if (usersQuery.data && page < usersQuery.data.totalPages) {
      setPage((prev) => prev + 1)
    }
  }, [page, usersQuery.data])

  const previousPage = useCallback(() => {
    if (page > 1) {
      setPage((prev) => prev - 1)
    }
  }, [page])

  const goToFirstPage = useCallback(() => {
    setPage(1)
  }, [])

  const goToLastPage = useCallback(() => {
    if (usersQuery.data) {
      setPage(usersQuery.data.totalPages)
    }
  }, [usersQuery.data])

  // Sorting handler
  const setSorting = useCallback((field: string, order: 'asc' | 'desc') => {
    setSortBy(field)
    setSortOrder(order)
    setPage(1) // Reset to first page on sort change
  }, [])

  // Clear filters handler
  const clearFilters = useCallback(() => {
    setFilters({})
    setSearch('')
    setPage(1)
  }, [])

  // Mutation wrapper functions with promise interface
  const createUser = useCallback(
    async (data: CreateUserPayload): Promise<User> => {
      return new Promise((resolve, reject) => {
        createMutation.mutate(data, {
          onSuccess: resolve,
          onError: reject,
        })
      })
    },
    [createMutation]
  )

  const updateUser = useCallback(
    async (id: string, data: UpdateUserPayload): Promise<User> => {
      return new Promise((resolve, reject) => {
        updateMutation.mutate(
          { id, data },
          {
            onSuccess: resolve,
            onError: reject,
          }
        )
      })
    },
    [updateMutation]
  )

  const deleteUser = useCallback(
    async (id: string): Promise<void> => {
      return new Promise((resolve, reject) => {
        deleteMutation.mutate(id, {
          onSuccess: () => resolve(),
          onError: reject,
        })
      })
    },
    [deleteMutation]
  )

  const bulkDeleteUsers = useCallback(
    async (ids: string[]): Promise<void> => {
      return new Promise((resolve, reject) => {
        bulkDeleteMutation.mutate(ids, {
          onSuccess: () => resolve(),
          onError: reject,
        })
      })
    },
    [bulkDeleteMutation]
  )

  const toggleUserActive = useCallback(
    async (id: string, isActive: boolean): Promise<User> => {
      return new Promise((resolve, reject) => {
        toggleActiveMutation.mutate(
          { id, isActive },
          {
            onSuccess: resolve,
            onError: reject,
          }
        )
      })
    },
    [toggleActiveMutation]
  )

  // Return unified interface
  return {
    // Query state
    users: usersQuery.data?.data ?? [],
    isLoading: usersQuery.isLoading,
    isError: usersQuery.isError,
    error: usersQuery.error,
    totalUsers: usersQuery.data?.total ?? 0,
    totalPages: usersQuery.data?.totalPages ?? 1,

    // Pagination
    page,
    pageSize,
    setPage,
    setPageSize,
    nextPage,
    previousPage,
    goToFirstPage,
    goToLastPage,

    // Search and filters
    search,
    setSearch,
    filters,
    setFilters,
    clearFilters,

    // Sorting
    sortBy,
    sortOrder,
    setSorting,

    // Mutations
    createUser,
    updateUser,
    deleteUser,
    bulkDeleteUsers,
    toggleUserActive,

    // Mutation states
    isCreating: createMutation.isPending,
    isUpdating: updateMutation.isPending,
    isDeleting: deleteMutation.isPending || bulkDeleteMutation.isPending,

    // Refetch
    refetch: usersQuery.refetch,
  }
}

/**
 * Export individual hooks for granular usage
 */
export { useUser, useUserStats, userKeys }
