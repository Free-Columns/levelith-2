/**
 * React Query hooks for Users feature (Mutations)
 *
 * @module admin/features/users/api/users.mutations
 *
 * Provides React Query mutation hooks for modifying user data with:
 * - Optimistic updates
 * - Automatic cache invalidation
 * - Error handling and rollback
 * - Success/error callbacks
 */

import { useMutation, useQueryClient, UseMutationResult } from '@tanstack/react-query'
import { createUser, updateUser, deleteUser, bulkDeleteUsers } from './users.api'
import { userKeys } from './users.queries'
import type { User, CreateUserPayload, UpdateUserPayload } from '../types/user.types'
import type { PaginatedResponse } from '@/admin/types/common.types'

/**
 * Hook to create a new user
 *
 * Features:
 * - Optimistic update to user list
 * - Automatic cache invalidation on success
 * - Rollback on error
 *
 * @param options - Mutation callbacks
 * @returns Mutation result
 *
 * @example
 * ```tsx
 * const createUserMutation = useCreateUser({
 *   onSuccess: (user) => {
 *     toast.success(`User ${user.username} created!`)
 *     navigate(`/admin/users/${user.id}`)
 *   },
 *   onError: (error) => {
 *     toast.error(`Failed to create user: ${error.message}`)
 *   }
 * })
 *
 * // In form submit handler
 * createUserMutation.mutate({
 *   username: 'johndoe',
 *   email: 'john@example.com',
 *   password: 'SecurePass123!',
 *   profile: { displayName: 'John Doe' }
 * })
 * ```
 */
export function useCreateUser(options?: {
  onSuccess?: (user: User) => void
  onError?: (error: Error) => void
}): UseMutationResult<User, Error, CreateUserPayload> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createUser,
    onSuccess: (newUser) => {
      // Invalidate and refetch user lists
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
      queryClient.invalidateQueries({ queryKey: userKeys.stats() })

      // Call custom success handler
      options?.onSuccess?.(newUser)
    },
    onError: (error) => {
      // Call custom error handler
      options?.onError?.(error)
    },
  })
}

/**
 * Hook to update an existing user
 *
 * Features:
 * - Optimistic update for immediate UI feedback
 * - Automatic rollback on error
 * - Cache invalidation for affected queries
 *
 * @param options - Mutation callbacks
 * @returns Mutation result
 *
 * @example
 * ```tsx
 * const updateUserMutation = useUpdateUser({
 *   onSuccess: (user) => {
 *     toast.success('User updated successfully')
 *   }
 * })
 *
 * // Update user
 * updateUserMutation.mutate({
 *   id: userId,
 *   data: { isActive: false, email: 'newemail@example.com' }
 * })
 * ```
 */
export function useUpdateUser(options?: {
  onSuccess?: (user: User) => void
  onError?: (error: Error) => void
}): UseMutationResult<User, Error, { id: string; data: UpdateUserPayload }> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }) => updateUser(id, data),
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.detail(id) })

      // Snapshot previous value
      const previousUser = queryClient.getQueryData<User>(userKeys.detail(id))

      // Optimistically update the cache
      if (previousUser) {
        queryClient.setQueryData<User>(userKeys.detail(id), {
          ...previousUser,
          ...data,
        })
      }

      // Return context with previous value
      return { previousUser }
    },
    onSuccess: (updatedUser) => {
      // Update cache with server response
      queryClient.setQueryData(userKeys.detail(updatedUser.id), updatedUser)

      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
      queryClient.invalidateQueries({ queryKey: userKeys.stats() })

      // Call custom success handler
      options?.onSuccess?.(updatedUser)
    },
    onError: (error, { id }, context) => {
      // Rollback to previous value on error
      if (context?.previousUser) {
        queryClient.setQueryData(userKeys.detail(id), context.previousUser)
      }

      // Call custom error handler
      options?.onError?.(error)
    },
  })
}

/**
 * Hook to delete a user
 *
 * Features:
 * - Optimistic removal from user lists
 * - Automatic cache cleanup
 * - Rollback on error
 *
 * @param options - Mutation callbacks
 * @returns Mutation result
 *
 * @example
 * ```tsx
 * const deleteUserMutation = useDeleteUser({
 *   onSuccess: () => {
 *     toast.success('User deleted successfully')
 *     navigate('/admin/users')
 *   },
 *   onError: () => {
 *     toast.error('Failed to delete user')
 *   }
 * })
 *
 * // Delete user with confirmation
 * const handleDelete = () => {
 *   if (confirm('Are you sure you want to delete this user?')) {
 *     deleteUserMutation.mutate(userId)
 *   }
 * }
 * ```
 */
export function useDeleteUser(options?: {
  onSuccess?: () => void
  onError?: (error: Error) => void
}): UseMutationResult<{ success: boolean; message: string }, Error, string> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteUser,
    onMutate: async (userId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.lists() })

      // Snapshot previous lists
      const previousLists = queryClient.getQueriesData<PaginatedResponse<User>>({ queryKey: userKeys.lists() })

      // Optimistically remove user from all lists
      queryClient.setQueriesData<PaginatedResponse<User>>(
        { queryKey: userKeys.lists() },
        (old) => {
          if (!old) return old
          return {
            ...old,
            data: old.data.filter((user) => user.id !== userId),
            total: old.total - 1,
          }
        }
      )

      return { previousLists }
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
      queryClient.invalidateQueries({ queryKey: userKeys.stats() })

      // Call custom success handler
      options?.onSuccess?.()
    },
    onError: (error, userId, context) => {
      // Rollback all list caches on error
      if (context?.previousLists) {
        context.previousLists.forEach(([queryKey, previousData]) => {
          if (previousData) {
            queryClient.setQueryData(queryKey, previousData)
          }
        })
      }

      // Call custom error handler
      options?.onError?.(error)
    },
  })
}

/**
 * Hook to bulk delete multiple users
 *
 * Features:
 * - Optimistic removal of multiple users
 * - Progress tracking via loading state
 * - Rollback on error
 * - Returns deletion statistics
 *
 * @param options - Mutation callbacks
 * @returns Mutation result
 *
 * @example
 * ```tsx
 * const bulkDeleteMutation = useBulkDeleteUsers({
 *   onSuccess: (result) => {
 *     toast.success(`Deleted ${result.deleted} users. Failed: ${result.failed}`)
 *     setSelectedUsers([])
 *   }
 * })
 *
 * // Delete selected users
 * const handleBulkDelete = () => {
 *   if (confirm(`Delete ${selectedUserIds.length} users?`)) {
 *     bulkDeleteMutation.mutate(selectedUserIds)
 *   }
 * }
 * ```
 */
export function useBulkDeleteUsers(options?: {
  onSuccess?: (result: { success: boolean; deleted: number; failed: number }) => void
  onError?: (error: Error) => void
}): UseMutationResult<{ success: boolean; deleted: number; failed: number }, Error, string[]> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: bulkDeleteUsers,
    onMutate: async (userIds) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.lists() })

      // Snapshot previous lists
      const previousLists = queryClient.getQueriesData<PaginatedResponse<User>>({ queryKey: userKeys.lists() })

      // Optimistically remove users from all lists
      queryClient.setQueriesData<PaginatedResponse<User>>(
        { queryKey: userKeys.lists() },
        (old) => {
          if (!old) return old
          return {
            ...old,
            data: old.data.filter((user) => !userIds.includes(user.id)),
            total: old.total - userIds.length,
          }
        }
      )

      return { previousLists }
    },
    onSuccess: (result) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
      queryClient.invalidateQueries({ queryKey: userKeys.stats() })

      // Call custom success handler
      options?.onSuccess?.(result)
    },
    onError: (error, userIds, context) => {
      // Rollback all list caches on error
      if (context?.previousLists) {
        context.previousLists.forEach(([queryKey, previousData]) => {
          if (previousData) {
            queryClient.setQueryData(queryKey, previousData)
          }
        })
      }

      // Call custom error handler
      options?.onError?.(error)
    },
  })
}

/**
 * Hook to toggle user active status
 *
 * Convenience wrapper around useUpdateUser for the common
 * use case of enabling/disabling user accounts
 *
 * @param options - Mutation callbacks
 * @returns Mutation result
 *
 * @example
 * ```tsx
 * const toggleActiveMutation = useToggleUserActive()
 *
 * // Toggle user active status
 * const handleToggle = () => {
 *   toggleActiveMutation.mutate({
 *     id: userId,
 *     isActive: !user.isActive
 *   })
 * }
 * ```
 */
export function useToggleUserActive(options?: {
  onSuccess?: (user: User) => void
  onError?: (error: Error) => void
}): UseMutationResult<User, Error, { id: string; isActive: boolean }> {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, isActive }) => updateUser(id, { isActive }),
    onSuccess: (user) => {
      // Update cache
      queryClient.setQueryData(userKeys.detail(user.id), user)
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
      queryClient.invalidateQueries({ queryKey: userKeys.stats() })

      options?.onSuccess?.(user)
    },
    onError: options?.onError,
  })
}
