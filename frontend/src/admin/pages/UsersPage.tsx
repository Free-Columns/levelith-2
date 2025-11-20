/**
 * Users Management Page
 *
 * @module admin/pages/UsersPage
 *
 * Main page for managing users in the admin dashboard.
 * Displays the UsersTable component with full CRUD operations.
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UsersTable } from '../features/users'
import { Button } from '@/components/ui/button'
import type { User } from '../features/users/types/user.types'

/**
 * UsersPage Component
 *
 * Provides a complete user management interface with:
 * - User list table with pagination
 * - Search and filtering
 * - Create, edit, delete operations
 * - Navigation to user details
 *
 * @example
 * ```tsx
 * // In routing configuration
 * <Route path="/admin/users" element={<UsersPage />} />
 * ```
 */
export function UsersPage() {
  const navigate = useNavigate()
  const [showCreateModal, setShowCreateModal] = useState(false)

  /**
   * Navigate to user detail page
   */
  const handleViewUser = (user: User) => {
    navigate(`/admin/users/${user.id}`)
  }

  /**
   * Navigate to user edit page (or open edit modal)
   */
  const handleEditUser = (user: User) => {
    navigate(`/admin/users/${user.id}/edit`)
  }

  /**
   * Navigate to user creation page
   */
  const handleCreateUser = () => {
    navigate('/admin/users/new')
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="mt-2 text-sm text-gray-600">
            Manage user accounts, permissions, and profiles
          </p>
        </div>

        <Button
          onClick={handleCreateUser}
          size="lg"
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Create New User
        </Button>
      </div>

      {/* Users Table */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200">
        <UsersTable
          onViewUser={handleViewUser}
          onEditUser={handleEditUser}
          initialPageSize={50}
          showBulkActions={true}
          showSearch={true}
          showFilters={true}
        />
      </div>

      {/* Footer Info */}
      <div className="mt-6 text-sm text-gray-500 text-center">
        <p>
          Use the search bar to find users by username or email. Click on a username to view
          details.
        </p>
      </div>
    </div>
  )
}
