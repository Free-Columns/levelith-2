/**
 * UserForm Component
 *
 * @module admin/features/users/components/UserForm
 *
 * Reusable form for creating and editing users with:
 * - React Hook Form integration
 * - Zod schema validation
 * - Profile fields support
 * - Loading and error states
 * - Responsive layout
 */

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { createUserSchema, updateUserSchema, type CreateUserFormData, type UpdateUserFormData } from '../schemas/user.schema'
import type { User } from '../types/user.types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card } from '@/components/ui/card'

/**
 * Props for UserForm component
 */
export interface UserFormProps {
  /**
   * Mode: 'create' for new users, 'edit' for existing users
   */
  mode: 'create' | 'edit'

  /**
   * Existing user data (required for edit mode)
   */
  user?: User

  /**
   * Form submission handler
   */
  onSubmit: (data: CreateUserFormData | UpdateUserFormData) => Promise<void> | void

  /**
   * Cancel handler
   */
  onCancel: () => void

  /**
   * Whether form is currently submitting
   */
  isSubmitting?: boolean

  /**
   * Error message to display
   */
  error?: string | null
}

/**
 * UserForm Component
 *
 * Shared form for creating and editing users with full validation
 * and profile field support.
 *
 * @example
 * ```tsx
 * // Create mode
 * <UserForm
 *   mode="create"
 *   onSubmit={async (data) => {
 *     await createUser(data)
 *     navigate('/admin/users')
 *   }}
 *   onCancel={() => navigate('/admin/users')}
 * />
 *
 * // Edit mode
 * <UserForm
 *   mode="edit"
 *   user={existingUser}
 *   onSubmit={async (data) => {
 *     await updateUser(user.id, data)
 *     navigate('/admin/users')
 *   }}
 *   onCancel={() => navigate('/admin/users')}
 * />
 * ```
 */
export function UserForm({
  mode,
  user,
  onSubmit,
  onCancel,
  isSubmitting = false,
  error = null,
}: UserFormProps) {
  // Select appropriate schema based on mode
  const schema = mode === 'create' ? createUserSchema : updateUserSchema

  // Initialize form with React Hook Form and Zod validation
  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<CreateUserFormData | UpdateUserFormData>({
    resolver: zodResolver(schema),
    defaultValues: mode === 'edit' && user
      ? {
          username: user.username,
          email: user.email,
          isActive: user.isActive,
          profile: {
            firstName: user.profile?.firstName || '',
            lastName: user.profile?.lastName || '',
            displayName: user.profile?.displayName || '',
            bio: user.profile?.bio || '',
            location: user.profile?.location || '',
            websiteUrl: user.profile?.websiteUrl || '',
            linkedinUrl: user.profile?.linkedinUrl || '',
            githubUrl: user.profile?.githubUrl || '',
          },
        }
      : {
          username: '',
          email: '',
          password: '',
          isActive: true,
          profile: {
            firstName: '',
            lastName: '',
            displayName: '',
            bio: '',
            location: '',
            websiteUrl: '',
            linkedinUrl: '',
            githubUrl: '',
          },
        },
  })

  /**
   * Handle form submission
   */
  const handleFormSubmit = async (data: CreateUserFormData | UpdateUserFormData) => {
    try {
      await onSubmit(data)
    } catch (err) {
      // Error is handled by parent component
      console.error('Form submission error:', err)
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-8">
      {/* Error Alert */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      )}

      {/* Account Information Card */}
      <Card className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Username */}
          <div className="space-y-2">
            <Label htmlFor="username">
              Username <span className="text-red-500">*</span>
            </Label>
            <Input
              id="username"
              {...register('username')}
              disabled={mode === 'edit'} // Username cannot be changed
              className={errors.username ? 'border-red-500' : ''}
              placeholder="Enter username"
            />
            {errors.username && (
              <p className="text-sm text-red-600">{errors.username.message}</p>
            )}
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email">
              Email <span className="text-red-500">*</span>
            </Label>
            <Input
              id="email"
              type="email"
              {...register('email')}
              className={errors.email ? 'border-red-500' : ''}
              placeholder="user@example.com"
            />
            {errors.email && (
              <p className="text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>

          {/* Password (create mode only) */}
          {mode === 'create' && (
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="password">
                Password <span className="text-red-500">*</span>
              </Label>
              <Input
                id="password"
                type="password"
                {...register('password')}
                className={errors.password ? 'border-red-500' : ''}
                placeholder="Enter password (min 8 characters)"
              />
              {errors.password && (
                <p className="text-sm text-red-600">{errors.password.message}</p>
              )}
              <p className="text-xs text-gray-500">
                Password must be at least 8 characters and contain uppercase, lowercase, number, and special character.
              </p>
            </div>
          )}

          {/* Active Status */}
          <div className="flex items-center space-x-2">
            <input
              id="isActive"
              type="checkbox"
              {...register('isActive')}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <Label htmlFor="isActive" className="font-normal">
              Active Account
            </Label>
          </div>
        </div>
      </Card>

      {/* Profile Information Card */}
      <Card className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* First Name */}
          <div className="space-y-2">
            <Label htmlFor="firstName">First Name</Label>
            <Input
              id="firstName"
              {...register('profile.firstName')}
              className={errors.profile?.firstName ? 'border-red-500' : ''}
              placeholder="Enter first name"
            />
            {errors.profile?.firstName && (
              <p className="text-sm text-red-600">{errors.profile.firstName.message}</p>
            )}
          </div>

          {/* Last Name */}
          <div className="space-y-2">
            <Label htmlFor="lastName">Last Name</Label>
            <Input
              id="lastName"
              {...register('profile.lastName')}
              className={errors.profile?.lastName ? 'border-red-500' : ''}
              placeholder="Enter last name"
            />
            {errors.profile?.lastName && (
              <p className="text-sm text-red-600">{errors.profile.lastName.message}</p>
            )}
          </div>

          {/* Display Name */}
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="displayName">Display Name</Label>
            <Input
              id="displayName"
              {...register('profile.displayName')}
              className={errors.profile?.displayName ? 'border-red-500' : ''}
              placeholder="How should we display your name?"
            />
            {errors.profile?.displayName && (
              <p className="text-sm text-red-600">{errors.profile.displayName.message}</p>
            )}
          </div>

          {/* Bio */}
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="bio">Bio</Label>
            <textarea
              id="bio"
              {...register('profile.bio')}
              rows={3}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.profile?.bio ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Tell us about yourself (max 500 characters)"
              maxLength={500}
            />
            {errors.profile?.bio && (
              <p className="text-sm text-red-600">{errors.profile.bio.message}</p>
            )}
          </div>

          {/* Location */}
          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              {...register('profile.location')}
              className={errors.profile?.location ? 'border-red-500' : ''}
              placeholder="City, State/Country"
            />
            {errors.profile?.location && (
              <p className="text-sm text-red-600">{errors.profile.location.message}</p>
            )}
          </div>

          {/* Website URL */}
          <div className="space-y-2">
            <Label htmlFor="websiteUrl">Website</Label>
            <Input
              id="websiteUrl"
              type="url"
              {...register('profile.websiteUrl')}
              className={errors.profile?.websiteUrl ? 'border-red-500' : ''}
              placeholder="https://example.com"
            />
            {errors.profile?.websiteUrl && (
              <p className="text-sm text-red-600">{errors.profile.websiteUrl.message}</p>
            )}
          </div>

          {/* LinkedIn URL */}
          <div className="space-y-2">
            <Label htmlFor="linkedinUrl">LinkedIn Profile</Label>
            <Input
              id="linkedinUrl"
              type="url"
              {...register('profile.linkedinUrl')}
              className={errors.profile?.linkedinUrl ? 'border-red-500' : ''}
              placeholder="https://linkedin.com/in/username"
            />
            {errors.profile?.linkedinUrl && (
              <p className="text-sm text-red-600">{errors.profile.linkedinUrl.message}</p>
            )}
          </div>

          {/* GitHub URL */}
          <div className="space-y-2">
            <Label htmlFor="githubUrl">GitHub Profile</Label>
            <Input
              id="githubUrl"
              type="url"
              {...register('profile.githubUrl')}
              className={errors.profile?.githubUrl ? 'border-red-500' : ''}
              placeholder="https://github.com/username"
            />
            {errors.profile?.githubUrl && (
              <p className="text-sm text-red-600">{errors.profile.githubUrl.message}</p>
            )}
          </div>
        </div>
      </Card>

      {/* Form Actions */}
      <div className="flex items-center justify-end gap-4 pt-6 border-t border-gray-200">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isSubmitting || (mode === 'edit' && !isDirty)}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          {isSubmitting ? (
            <>
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {mode === 'create' ? 'Creating...' : 'Saving...'}
            </>
          ) : (
            mode === 'create' ? 'Create User' : 'Save Changes'
          )}
        </Button>
      </div>
    </form>
  )
}
