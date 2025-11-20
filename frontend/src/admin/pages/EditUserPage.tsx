/**
 * Edit User Page
 *
 * @module admin/pages/EditUserPage
 *
 * Page for editing existing users with full form validation and error handling.
 */

import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { UserForm } from '../features/users/components'
import { useUser } from '../features/users/api/users.queries'
import { useUpdateUser } from '../features/users/api/users.mutations'
import type { UpdateUserPayload } from '../features/users/types/user.types'
import type { UpdateUserFormData } from '../features/users/schemas/user.schema'
import { LoadingSpinner } from '../components/custom/LoadingSpinner'

/**
 * EditUserPage Component
 *
 * Provides a complete interface for editing existing users with:
 * - User data fetching with loading state
 * - Full validation with Zod schemas
 * - Profile information fields
 * - Error handling with toast notifications
 * - Navigation on success
 *
 * @example
 * ```tsx
 * // In routing configuration
 * <Route path="/admin/users/:userId/edit" element={<EditUserPage />} />
 * ```
 */
export function EditUserPage() {
  const navigate = useNavigate()
  const { userId } = useParams<{ userId: string }>()
  const [error, setError] = useState<string | null>(null)

  // Fetch user data
  const {
    data: user,
    isLoading: isLoadingUser,
    isError: isUserError,
    error: userError
  } = useUser(userId!, {
    enabled: !!userId
  })

  // Use the update mutation hook
  const updateUserMutation = useUpdateUser({
    onSuccess: (updatedUser) => {
      // Navigate to user detail page on success
      navigate(`/admin/users/${updatedUser.id}`, {
        state: { message: `User "${updatedUser.username}" updated successfully!` }
      })
    },
    onError: (err) => {
      // Display error message
      setError(err.message || 'Failed to update user. Please try again.')
    }
  })

  /**
   * Handle form submission
   */
  const handleSubmit = async (formData: UpdateUserFormData) => {
    if (!userId) return

    setError(null)

    // Transform form data to API payload format
    const payload: UpdateUserPayload = {
      email: formData.email,
      isActive: formData.isActive,
      isVerified: formData.isVerified,
      profile: formData.profile,
    }

    // Trigger mutation
    await updateUserMutation.mutateAsync({
      id: userId,
      data: payload
    })
  }

  /**
   * Handle cancel action
   */
  const handleCancel = () => {
    navigate(`/admin/users/${userId}`)
  }

  // Loading state
  if (isLoadingUser) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <LoadingSpinner />
          <div className="mt-4 text-sm text-gray-600">Loading user data...</div>
        </div>
      </div>
    )
  }

  // Error state
  if (isUserError || !user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <div className="text-center">
            <svg className="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h2 className="mt-4 text-lg font-medium text-gray-900">User Not Found</h2>
            <p className="mt-2 text-sm text-gray-600">
              {userError?.message || 'The requested user could not be found.'}
            </p>
            <button
              onClick={() => navigate('/admin/users')}
              className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Back to Users
            </button>
          </div>
        </div>
      </div>
    )
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
          <button
            onClick={() => navigate(`/admin/users/${userId}`)}
            className="hover:text-blue-600 transition-colors"
          >
            {user.username}
          </button>
          <span>/</span>
          <span className="text-gray-900">Edit</span>
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Edit User</h1>
        <p className="mt-2 text-sm text-gray-600">
          Update account and profile information for <strong>{user.username}</strong>
        </p>
      </div>

      {/* User Form */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-6">
          <UserForm
            mode="edit"
            user={user}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={updateUserMutation.isPending}
            error={error}
          />
        </div>
      </div>

      {/* Help Text */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Tips for Editing Users</h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>Username cannot be changed once created for data integrity</li>
          <li>Email can be updated but must remain unique in the system</li>
          <li>Deactivating a user will prevent them from logging in</li>
          <li>Profile changes are reflected immediately in the user's public profile</li>
          <li>Password cannot be changed from this form - use the password reset feature</li>
        </ul>
      </div>
    </div>
  )
}
