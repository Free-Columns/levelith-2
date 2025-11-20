/**
 * Create User Page
 *
 * @module admin/pages/CreateUserPage
 *
 * Page for creating new users with full form validation and error handling.
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UserForm } from '../features/users/components'
import { useCreateUser } from '../features/users/api/users.mutations'
import type { CreateUserPayload } from '../features/users/types/user.types'
import type { CreateUserFormData } from '../features/users/schemas/user.schema'

/**
 * CreateUserPage Component
 *
 * Provides a complete interface for creating new users with:
 * - Full validation with Zod schemas
 * - Profile information fields
 * - Error handling with toast notifications
 * - Navigation on success
 *
 * @example
 * ```tsx
 * // In routing configuration
 * <Route path="/admin/users/new" element={<CreateUserPage />} />
 * ```
 */
export function CreateUserPage() {
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)

  // Use the create mutation hook
  const createUserMutation = useCreateUser({
    onSuccess: (user) => {
      // Navigate to user detail page on success
      navigate(`/admin/users/${user.id}`, {
        state: { message: `User "${user.username}" created successfully!` }
      })
    },
    onError: (err) => {
      // Display error message
      setError(err.message || 'Failed to create user. Please try again.')
    }
  })

  /**
   * Handle form submission
   */
  const handleSubmit = async (formData: CreateUserFormData) => {
    setError(null)

    // Transform form data to API payload format
    const payload: CreateUserPayload = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      isActive: formData.isActive,
      profile: formData.profile,
    }

    // Trigger mutation
    await createUserMutation.mutateAsync(payload)
  }

  /**
   * Handle cancel action
   */
  const handleCancel = () => {
    navigate('/admin/users')
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
          <button
            onClick={() => navigate('/admin/users')}
            className="hover:text-blue-600 transition-colors"
          >
            Users
          </button>
          <span>/</span>
          <span className="text-gray-900">Create New User</span>
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Create New User</h1>
        <p className="mt-2 text-sm text-gray-600">
          Add a new user to the system with account and profile information.
        </p>
      </div>

      {/* User Form */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-6">
          <UserForm
            mode="create"
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={createUserMutation.isPending}
            error={error}
          />
        </div>
      </div>

      {/* Help Text */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Tips for Creating Users</h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>Username must be unique and contain only letters, numbers, underscores, and hyphens</li>
          <li>Password must be at least 8 characters with uppercase, lowercase, number, and special character</li>
          <li>Email must be unique in the system</li>
          <li>Profile information is optional but recommended for better user experience</li>
          <li>Users are set to active by default but can be deactivated later</li>
        </ul>
      </div>
    </div>
  )
}
