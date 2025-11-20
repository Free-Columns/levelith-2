/**
 * Users feature module
 *
 * @module admin/features/users
 *
 * Comprehensive user management module with:
 * - TypeScript types and schemas
 * - React Query hooks for data fetching
 * - React Query mutations for CRUD operations
 * - Composite useUsers hook
 * - UsersTable component with TanStack Table
 */

// Types
export * from './types/user.types'

// Schemas
export * from './schemas/user.schema'

// API methods
export * from './api/users.api'

// Query hooks
export * from './api/users.queries'

// Mutation hooks
export * from './api/users.mutations'

// Custom hooks
export * from './hooks'

// Components
export * from './components'
