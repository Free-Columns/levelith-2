/**
 * User Detail Page
 *
 * @module admin/pages/UserDetailPage
 *
 * Displays detailed information about a single user including:
 * - Profile information
 * - Account status
 * - Associated experiences
 * - Activity history
 */

import { useParams, useNavigate, Link } from 'react-router-dom'
import { useUser } from '../features/users'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '../components/custom/LoadingSpinner'
import { Card, CardHeader, CardContent } from '@/components/ui/card'

/**
 * UserDetailPage Component
 *
 * Shows comprehensive details for a single user with options to
 * edit or delete the user account.
 *
 * @example
 * ```tsx
 * // In routing configuration
 * <Route path="/admin/users/:id" element={<UserDetailPage />} />
 * ```
 */
export function UserDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: user, isLoading, isError, error } = useUser(id!, { enabled: !!id })

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <LoadingSpinner />
          <p className="mt-4 text-gray-600">Loading user details...</p>
        </div>
      </div>
    )
  }

  // Error state
  if (isError || !user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h2 className="text-xl font-semibold text-red-900 mb-2">Error Loading User</h2>
          <p className="text-red-700">{error?.message || 'User not found'}</p>
          <Button onClick={() => navigate('/admin/users')} className="mt-4">
            Back to Users
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="mb-6 text-sm text-gray-600">
        <Link to="/admin" className="hover:text-blue-600">
          Admin
        </Link>
        {' / '}
        <Link to="/admin/users" className="hover:text-blue-600">
          Users
        </Link>
        {' / '}
        <span className="text-gray-900 font-medium">{user.username}</span>
      </nav>

      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{user.username}</h1>
          <p className="mt-1 text-sm text-gray-600">{user.email}</p>
        </div>

        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={() => navigate(`/admin/users/${user.id}/edit`)}
          >
            Edit User
          </Button>
          <Button variant="outline" onClick={() => navigate('/admin/users')}>
            Back to List
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Account Information */}
          <Card>
            <CardHeader>
              <h2 className="text-xl font-semibold">Account Information</h2>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Username</label>
                    <p className="mt-1 text-gray-900">{user.username}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Email</label>
                    <p className="mt-1 text-gray-900">{user.email}</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Status</label>
                    <p className="mt-1">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          user.isActive
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {user.isActive ? 'Active' : 'Inactive'}
                      </span>
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Verification</label>
                    <p className="mt-1">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          user.isVerified
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {user.isVerified ? 'Verified' : 'Unverified'}
                      </span>
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Member Since</label>
                    <p className="mt-1 text-gray-900">
                      {new Date(user.createdAt).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">Last Updated</label>
                    <p className="mt-1 text-gray-900">
                      {new Date(user.updatedAt).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                </div>

                {user.lastLoginAt && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">Last Login</label>
                    <p className="mt-1 text-gray-900">
                      {new Date(user.lastLoginAt).toLocaleString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Profile Information */}
          {user.profile && (
            <Card>
              <CardHeader>
                <h2 className="text-xl font-semibold">Profile Information</h2>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {user.profile.displayName && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Display Name</label>
                      <p className="mt-1 text-gray-900">{user.profile.displayName}</p>
                    </div>
                  )}

                  {user.profile.bio && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Bio</label>
                      <p className="mt-1 text-gray-900">{user.profile.bio}</p>
                    </div>
                  )}

                  {user.profile.location && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Location</label>
                      <p className="mt-1 text-gray-900">{user.profile.location}</p>
                    </div>
                  )}

                  {(user.profile.websiteUrl || user.profile.linkedinUrl || user.profile.githubUrl) && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Links</label>
                      <div className="mt-1 space-y-1">
                        {user.profile.websiteUrl && (
                          <p>
                            <a
                              href={user.profile.websiteUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline"
                            >
                              Website
                            </a>
                          </p>
                        )}
                        {user.profile.linkedinUrl && (
                          <p>
                            <a
                              href={user.profile.linkedinUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline"
                            >
                              LinkedIn
                            </a>
                          </p>
                        )}
                        {user.profile.githubUrl && (
                          <p>
                            <a
                              href={user.profile.githubUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline"
                            >
                              GitHub
                            </a>
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold">Quick Stats</h2>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Experiences</span>
                  <span className="text-lg font-semibold text-gray-900">
                    {user.experienceCount ?? 0}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Account Age</span>
                  <span className="text-lg font-semibold text-gray-900">
                    {Math.floor(
                      (Date.now() - new Date(user.createdAt).getTime()) / (1000 * 60 * 60 * 24)
                    )}{' '}
                    days
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold">Actions</h2>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => navigate(`/admin/users/${user.id}/edit`)}
              >
                Edit User
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => navigate(`/admin/experiences?userId=${user.id}`)}
              >
                View Experiences
              </Button>
              <Button variant="outline" className="w-full justify-start text-red-600 hover:text-red-700">
                Delete User
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
