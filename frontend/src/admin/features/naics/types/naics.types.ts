/**
 * NAICS entity types for admin dashboard
 *
 * @module admin/features/naics/types
 */

/**
 * NAICS code level (2, 3, 4, or 6 digit)
 */
export type NAICSLevel = 2 | 3 | 4 | 6

/**
 * NAICS entity from backend
 */
export interface NAICS {
  id: string
  code: string
  title: string
  description?: string
  level: NAICSLevel
  parentCode?: string
  tags: string[]
  customCategory?: string
  adminNotes?: string
  isActive: boolean
  experienceCount?: number
  createdAt: string
  updatedAt: string
}

/**
 * NAICS creation payload
 */
export interface CreateNAICSPayload {
  code: string
  title: string
  description?: string
  level: NAICSLevel
  parentCode?: string
  tags?: string[]
  customCategory?: string
  adminNotes?: string
  isActive?: boolean
}

/**
 * NAICS update payload
 */
export interface UpdateNAICSPayload {
  title?: string
  description?: string
  tags?: string[]
  customCategory?: string
  adminNotes?: string
  isActive?: boolean
}

/**
 * NAICS filter options
 */
export interface NAICSFilterOptions {
  search?: string
  level?: NAICSLevel
  customCategory?: string
  tags?: string[]
  isActive?: boolean
  hasExperiences?: boolean
}

/**
 * NAICS statistics
 */
export interface NAICSStats {
  totalCodes: number
  byLevel: Record<NAICSLevel, number>
  topCategories: Array<{
    category: string
    count: number
  }>
  mostUsed: Array<{
    code: string
    title: string
    count: number
  }>
}

/**
 * NAICS hierarchy node (for tree view)
 */
export interface NAICSNode {
  code: string
  title: string
  level: NAICSLevel
  children?: NAICSNode[]
  experienceCount: number
}
