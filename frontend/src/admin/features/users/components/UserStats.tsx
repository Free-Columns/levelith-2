/**
 * UserStats Widget Component
 *
 * @module admin/features/users/components/UserStats
 *
 * Dashboard widget displaying user statistics with:
 * - Total users count
 * - Active/inactive users
 * - Verified users count
 * - Recent signups (last 30 days)
 * - Loading and error states
 * - Responsive grid layout
 */

import { useUserStats } from '../api/users.queries'
import { Card } from '@/components/ui/card'
import { LoadingSpinner } from '@/admin/components/custom/LoadingSpinner'

/**
 * Props for UserStats component
 */
export interface UserStatsProps {
  /**
   * Optional CSS class name
   */
  className?: string

  /**
   * Whether to show grid layout (default: true)
   */
  showGrid?: boolean
}

/**
 * UserStats Component
 *
 * Dashboard widget that fetches and displays user statistics
 * from the backend API using React Query.
 *
 * @example
 * ```tsx
 * // In Dashboard page
 * import { UserStats } from '../features/users/components'
 *
 * function Dashboard() {
 *   return (
 *     <div className="space-y-6">
 *       <UserStats />
 *       {/* Other dashboard components *\/}
 *     </div>
 *   )
 * }
 * ```
 */
export function UserStats({ className = '', showGrid = true }: UserStatsProps) {
  // Fetch user statistics using React Query
  const { data: stats, isLoading, isError, error } = useUserStats()

  // Loading state
  if (isLoading) {
    return (
      <div className={`p-8 ${className}`}>
        <div className="flex flex-col items-center justify-center">
          <LoadingSpinner />
          <div className="mt-4 text-sm text-gray-600">Loading user statistics...</div>
        </div>
      </div>
    )
  }

  // Error state
  if (isError) {
    return (
      <div className={`p-8 ${className}`}>
        <div className="flex flex-col items-center justify-center">
          <svg className="h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div className="mt-4 text-sm text-red-600">
            {error?.message || 'Failed to load user statistics'}
          </div>
        </div>
      </div>
    )
  }

  // No data state
  if (!stats) {
    return (
      <div className={`p-8 ${className}`}>
        <div className="text-center text-sm text-gray-600">No statistics available</div>
      </div>
    )
  }

  // Stat card data
  const statCards = [
    {
      label: 'Total Users',
      value: stats.totalUsers,
      color: 'blue',
      icon: (
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ),
    },
    {
      label: 'Active Users',
      value: stats.activeUsers,
      color: 'green',
      icon: (
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      subtitle: `${stats.inactiveUsers} inactive`,
    },
    {
      label: 'Verified Users',
      value: stats.verifiedUsers,
      color: 'purple',
      icon: (
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
      ),
    },
    {
      label: 'Recent Signups',
      value: stats.recentSignups,
      color: 'orange',
      icon: (
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
        </svg>
      ),
      subtitle: 'Last 30 days',
    },
  ]

  // Color variants
  const colorVariants = {
    blue: {
      bg: 'bg-blue-50',
      text: 'text-blue-600',
      icon: 'text-blue-500',
    },
    green: {
      bg: 'bg-green-50',
      text: 'text-green-600',
      icon: 'text-green-500',
    },
    purple: {
      bg: 'bg-purple-50',
      text: 'text-purple-600',
      icon: 'text-purple-500',
    },
    orange: {
      bg: 'bg-orange-50',
      text: 'text-orange-600',
      icon: 'text-orange-500',
    },
  }

  return (
    <div className={className}>
      {/* Grid Layout */}
      {showGrid ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {statCards.map((stat, index) => {
            const colors = colorVariants[stat.color as keyof typeof colorVariants]
            return (
              <Card key={index} className="overflow-hidden">
                <div className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-600 mb-1">
                        {stat.label}
                      </p>
                      <div className="flex items-baseline">
                        <p className={`text-3xl font-bold ${colors.text}`}>
                          {stat.value.toLocaleString()}
                        </p>
                      </div>
                      {stat.subtitle && (
                        <p className="text-xs text-gray-500 mt-1">{stat.subtitle}</p>
                      )}
                    </div>
                    <div className={`p-3 rounded-full ${colors.bg}`}>
                      <div className={colors.icon}>{stat.icon}</div>
                    </div>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      ) : (
        /* List Layout */
        <div className="space-y-4">
          {statCards.map((stat, index) => {
            const colors = colorVariants[stat.color as keyof typeof colorVariants]
            return (
              <div key={index} className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200">
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-full ${colors.bg}`}>
                    <div className={colors.icon}>{stat.icon}</div>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    {stat.subtitle && (
                      <p className="text-xs text-gray-500">{stat.subtitle}</p>
                    )}
                  </div>
                </div>
                <p className={`text-2xl font-bold ${colors.text}`}>
                  {stat.value.toLocaleString()}
                </p>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
