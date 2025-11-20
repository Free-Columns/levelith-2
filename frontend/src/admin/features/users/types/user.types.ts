/**
 * User entity types for admin dashboard
 *
 * @module admin/features/users/types
 */

/**
 * Base user entity from backend
 */
export interface User {
  id: string
  username: string
  email: string
  isActive: boolean
  isVerified: boolean
  createdAt: string
  updatedAt: string
  lastLoginAt?: string
  profile?: UserProfile
  experienceCount?: number
}

/**
 * User profile information
 */
export interface UserProfile {
  firstName?: string
  lastName?: string
  displayName?: string
  bio?: string
  avatarUrl?: string
  location?: string
  websiteUrl?: string
  linkedinUrl?: string
  githubUrl?: string
}

/**
 * User creation payload
 */
export interface CreateUserPayload {
  username: string
  email: string
  password: string
  isActive?: boolean
  profile?: Partial<UserProfile>
}

/**
 * User update payload
 */
export interface UpdateUserPayload {
  username?: string
  email?: string
  password?: string
  isActive?: boolean
  isVerified?: boolean
  profile?: Partial<UserProfile>
}

/**
 * User filter options
 */
export interface UserFilterOptions {
  search?: string
  isActive?: boolean
  isVerified?: boolean
  dateRange?: {
    from?: string
    to?: string
  }
}

/**
 * User statistics
 */
export interface UserStats {
  totalUsers: number
  activeUsers: number
  inactiveUsers: number
  verifiedUsers: number
  recentSignups: number
}
