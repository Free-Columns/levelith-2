/**
 * UsersTable Component
 *
 * @module admin/features/users/components/UsersTable
 *
 * Comprehensive data table for user management with:
 * - TanStack Table v8 integration
 * - Server-side pagination
 * - Search and filtering
 * - Column sorting
 * - Row selection
 * - CRUD operations
 * - Loading and error states
 */

import { useMemo, useState } from 'react'
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
  type RowSelectionState,
} from '@tanstack/react-table'
import { useUsers } from '../hooks/useUsers'
import type { User } from '../types/user.types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { LoadingSpinner } from '@/admin/components/custom/LoadingSpinner'
import { Pagination } from '@/admin/components/custom/Pagination'
import { ConfirmDialog } from '@/admin/components/custom/ConfirmDialog'

/**
 * Props for UsersTable component
 */
export interface UsersTableProps {
  /**
   * Callback when user is clicked for viewing details
   */
  onViewUser?: (user: User) => void

  /**
   * Callback when user is clicked for editing
   */
  onEditUser?: (user: User) => void

  /**
   * Initial page size (default: 50)
   */
  initialPageSize?: number

  /**
   * Whether to show bulk actions (default: true)
   */
  showBulkActions?: boolean

  /**
   * Whether to show search bar (default: true)
   */
  showSearch?: boolean

  /**
   * Whether to show filters (default: true)
   */
  showFilters?: boolean
}

/**
 * UsersTable Component
 *
 * Full-featured data table for managing users with pagination,
 * search, filtering, sorting, and CRUD operations.
 *
 * @example
 * ```tsx
 * <UsersTable
 *   onViewUser={(user) => navigate(`/admin/users/${user.id}`)}
 *   onEditUser={(user) => setEditingUser(user)}
 *   initialPageSize={25}
 * />
 * ```
 */
export function UsersTable({
  onViewUser,
  onEditUser,
  initialPageSize = 50,
  showBulkActions = true,
  showSearch = true,
  showFilters = true,
}: UsersTableProps) {
  // Row selection state
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({})

  // Delete confirmation dialog state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false)
  const [userToDelete, setUserToDelete] = useState<User | null>(null)
  const [bulkDeleteConfirmOpen, setBulkDeleteConfirmOpen] = useState(false)

  // Filter state
  const [activeFilter, setActiveFilter] = useState<boolean | undefined>(undefined)
  const [verifiedFilter, setVerifiedFilter] = useState<boolean | undefined>(undefined)

  // Use the composite hook for all user operations
  const {
    users,
    isLoading,
    isError,
    error,
    totalUsers,
    totalPages,
    page,
    pageSize,
    setPage,
    setPageSize,
    nextPage,
    previousPage,
    search,
    setSearch,
    filters,
    setFilters,
    sortBy,
    sortOrder,
    setSorting,
    deleteUser,
    bulkDeleteUsers,
    toggleUserActive,
    isDeleting,
  } = useUsers({
    initialPageSize,
    initialFilters: {},
    onUserDeleted: () => {
      setRowSelection({})
      setDeleteConfirmOpen(false)
      setBulkDeleteConfirmOpen(false)
      setUserToDelete(null)
    },
    onError: (error) => {
      console.error('User operation error:', error)
      alert(`Error: ${error.message}`)
    },
  })

  // Update filters when filter dropdowns change
  useMemo(() => {
    setFilters({
      isActive: activeFilter,
      isVerified: verifiedFilter,
    })
  }, [activeFilter, verifiedFilter, setFilters])

  // Define table columns
  const columns = useMemo<ColumnDef<User>[]>(
    () => [
      // Selection column
      ...(showBulkActions
        ? [
            {
              id: 'select',
              header: ({ table }) => (
                <input
                  type="checkbox"
                  checked={table.getIsAllRowsSelected()}
                  indeterminate={table.getIsSomeRowsSelected()}
                  onChange={table.getToggleAllRowsSelectedHandler()}
                  aria-label="Select all users"
                />
              ),
              cell: ({ row }) => (
                <input
                  type="checkbox"
                  checked={row.getIsSelected()}
                  onChange={row.getToggleSelectedHandler()}
                  aria-label={`Select user ${row.original.username}`}
                />
              ),
              enableSorting: false,
              enableHiding: false,
            } as ColumnDef<User>,
          ]
        : []),

      // Username column with avatar
      {
        accessorKey: 'username',
        header: 'Username',
        cell: ({ row }) => {
          const user = row.original
          const avatarUrl = user.profile?.avatarUrl
          const displayName = user.profile?.displayName || user.username
          const initials = displayName
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2)

          return (
            <button
              type="button"
              onClick={() => onViewUser?.(user)}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              {/* Avatar */}
              <div className="flex-shrink-0">
                {avatarUrl ? (
                  <img
                    src={avatarUrl}
                    alt={displayName}
                    className="h-10 w-10 rounded-full object-cover ring-2 ring-gray-200"
                  />
                ) : (
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center ring-2 ring-gray-200">
                    <span className="text-white text-sm font-semibold">{initials}</span>
                  </div>
                )}
              </div>
              {/* Username */}
              <div className="text-left">
                <div className="font-medium text-blue-600 hover:text-blue-800">
                  {user.username}
                </div>
                {user.profile?.displayName && user.profile.displayName !== user.username && (
                  <div className="text-xs text-gray-500">{user.profile.displayName}</div>
                )}
              </div>
            </button>
          )
        },
      },

      // Email column
      {
        accessorKey: 'email',
        header: 'Email',
        cell: ({ row }) => (
          <span className="text-sm text-gray-600">{row.original.email}</span>
        ),
      },

      // Status column
      {
        accessorKey: 'isActive',
        header: 'Status',
        cell: ({ row }) => (
          <button
            type="button"
            onClick={() => toggleUserActive(row.original.id, !row.original.isActive)}
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              row.original.isActive
                ? 'bg-green-100 text-green-800 hover:bg-green-200'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            {row.original.isActive ? 'Active' : 'Inactive'}
          </button>
        ),
      },

      // Verified column
      {
        accessorKey: 'isVerified',
        header: 'Verified',
        cell: ({ row }) => (
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium ${
              row.original.isVerified
                ? 'bg-blue-100 text-blue-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}
          >
            {row.original.isVerified ? 'Verified' : 'Unverified'}
          </span>
        ),
      },

      // Experience count column
      {
        accessorKey: 'experienceCount',
        header: 'Experiences',
        cell: ({ row }) => (
          <span className="text-sm text-gray-600">
            {row.original.experienceCount ?? 0}
          </span>
        ),
      },

      // Created at column
      {
        accessorKey: 'createdAt',
        header: 'Joined',
        cell: ({ row }) => (
          <span className="text-sm text-gray-600">
            {new Date(row.original.createdAt).toLocaleDateString()}
          </span>
        ),
      },

      // Actions column
      {
        id: 'actions',
        header: 'Actions',
        cell: ({ row }) => (
          <div className="flex gap-2">
            {onEditUser && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => onEditUser(row.original)}
              >
                Edit
              </Button>
            )}
            <Button
              size="sm"
              variant="destructive"
              onClick={() => {
                setUserToDelete(row.original)
                setDeleteConfirmOpen(true)
              }}
            >
              Delete
            </Button>
          </div>
        ),
        enableSorting: false,
      },
    ],
    [showBulkActions, onViewUser, onEditUser, toggleUserActive]
  )

  // Initialize table
  const table = useReactTable({
    data: users,
    columns,
    getCoreRowModel: getCoreRowModel(),
    state: {
      rowSelection,
    },
    onRowSelectionChange: setRowSelection,
    enableRowSelection: true,
    manualPagination: true,
    manualSorting: true,
    pageCount: totalPages,
  })

  // Get selected users
  const selectedUsers = useMemo(() => {
    return table.getSelectedRowModel().rows.map((row) => row.original)
  }, [table, rowSelection])

  // Handle bulk delete
  const handleBulkDelete = async () => {
    const userIds = selectedUsers.map((u) => u.id)
    await bulkDeleteUsers(userIds)
  }

  // Handle single delete
  const handleDelete = async () => {
    if (userToDelete) {
      await deleteUser(userToDelete.id)
    }
  }

  // Error state
  if (isError) {
    return (
      <div className="p-8 text-center">
        <div className="text-red-600 font-medium mb-2">Error loading users</div>
        <div className="text-sm text-gray-600">{error?.message}</div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header with search and filters */}
      {(showSearch || showFilters) && (
        <div className="flex gap-4 items-center flex-wrap">
          {/* Search bar */}
          {showSearch && (
            <div className="flex-1 min-w-[300px]">
              <Input
                type="search"
                placeholder="Search users by username or email..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full"
              />
            </div>
          )}

          {/* Filters */}
          {showFilters && (
            <>
              <select
                value={activeFilter === undefined ? 'all' : activeFilter ? 'active' : 'inactive'}
                onChange={(e) =>
                  setActiveFilter(
                    e.target.value === 'all'
                      ? undefined
                      : e.target.value === 'active'
                  )
                }
                className="px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>

              <select
                value={verifiedFilter === undefined ? 'all' : verifiedFilter ? 'verified' : 'unverified'}
                onChange={(e) =>
                  setVerifiedFilter(
                    e.target.value === 'all'
                      ? undefined
                      : e.target.value === 'verified'
                  )
                }
                className="px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Verification</option>
                <option value="verified">Verified</option>
                <option value="unverified">Unverified</option>
              </select>
            </>
          )}

          {/* Results count */}
          <div className="text-sm text-gray-600">
            {totalUsers} {totalUsers === 1 ? 'user' : 'users'}
          </div>
        </div>
      )}

      {/* Bulk actions */}
      {showBulkActions && selectedUsers.length > 0 && (
        <div className="flex items-center gap-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <span className="text-sm font-medium text-blue-900">
            {selectedUsers.length} user{selectedUsers.length === 1 ? '' : 's'} selected
          </span>
          <Button
            size="sm"
            variant="destructive"
            onClick={() => setBulkDeleteConfirmOpen(true)}
            disabled={isDeleting}
          >
            Delete Selected
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => setRowSelection({})}
          >
            Clear Selection
          </Button>
        </div>
      )}

      {/* Table */}
      <div className="border border-gray-200 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      key={header.id}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
                    >
                      {header.isPlaceholder
                        ? null
                        : flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {isLoading ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center">
                    <LoadingSpinner />
                    <div className="mt-2 text-sm text-gray-600">Loading users...</div>
                  </td>
                </tr>
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center">
                    <div className="text-gray-500 font-medium">No users found</div>
                    {search && (
                      <div className="mt-2 text-sm text-gray-400">
                        Try adjusting your search or filters
                      </div>
                    )}
                  </td>
                </tr>
              ) : (
                table.getRowModel().rows.map((row) => (
                  <tr
                    key={row.id}
                    className="hover:bg-gray-50 transition-colors"
                  >
                    {row.getVisibleCells().map((cell) => (
                      <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {!isLoading && totalPages > 1 && (
        <Pagination
          currentPage={page}
          totalPages={totalPages}
          pageSize={pageSize}
          totalItems={totalUsers}
          onPageChange={setPage}
          onPageSizeChange={setPageSize}
          onNextPage={nextPage}
          onPreviousPage={previousPage}
        />
      )}

      {/* Delete confirmation dialogs */}
      <ConfirmDialog
        open={deleteConfirmOpen}
        onClose={() => {
          setDeleteConfirmOpen(false)
          setUserToDelete(null)
        }}
        onConfirm={handleDelete}
        title="Delete User"
        description={`Are you sure you want to delete user "${userToDelete?.username}"? This action cannot be undone and will also delete all of their experiences.`}
        confirmText="Delete"
        cancelText="Cancel"
        variant="destructive"
      />

      <ConfirmDialog
        open={bulkDeleteConfirmOpen}
        onClose={() => setBulkDeleteConfirmOpen(false)}
        onConfirm={handleBulkDelete}
        title="Delete Multiple Users"
        description={`Are you sure you want to delete ${selectedUsers.length} user${
          selectedUsers.length === 1 ? '' : 's'
        }? This action cannot be undone and will also delete all of their experiences.`}
        confirmText={`Delete ${selectedUsers.length} User${selectedUsers.length === 1 ? '' : 's'}`}
        cancelText="Cancel"
        variant="destructive"
      />
    </div>
  )
}
