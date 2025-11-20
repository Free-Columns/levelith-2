/**
 * Experience entity types for admin dashboard
 *
 * @module admin/features/experiences/types
 */

/**
 * Experience categories (main types)
 */
export type ExperienceCategory = 'Education' | 'Workplace' | 'Skills'

/**
 * Education experience types
 */
export type EducationType = 'Certificate' | 'Degree' | 'Course'

/**
 * Workplace experience types
 */
export type WorkplaceType = 'Gig' | 'Part-Time' | 'Full-Time'

/**
 * Skills experience types
 */
export type SkillsType = 'Soft Skills' | 'Hard Skills' | 'Native Skills'

/**
 * All experience types combined
 */
export type ExperienceType = EducationType | WorkplaceType | SkillsType

/**
 * Base experience entity (common fields)
 */
export interface BaseExperience {
  id: string
  userId: string
  category: ExperienceCategory
  type: ExperienceType
  title: string
  description?: string
  startDate?: string
  endDate?: string
  isCurrent: boolean
  naicsCode: string
  naicsDescription?: string
  skillsGained: string[]
  metadata: Record<string, any>
  createdAt: string
  updatedAt: string
}

/**
 * Education-specific fields
 */
export interface EducationFields {
  institution: string
  fieldOfStudy?: string
  degreeLevel?: string
  grade?: string
  credentialId?: string
  credentialUrl?: string
}

/**
 * Workplace-specific fields
 */
export interface WorkplaceFields {
  company: string
  position: string
  location?: string
  employmentType?: string
  responsibilities?: string[]
  achievements?: string[]
}

/**
 * Skills-specific fields
 */
export interface SkillsFields {
  proficiencyLevel?: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'
  yearsOfExperience?: number
  endorsements?: number
}

/**
 * Education experience
 */
export interface EducationExperience extends BaseExperience, EducationFields {
  category: 'Education'
  type: EducationType
}

/**
 * Workplace experience
 */
export interface WorkplaceExperience extends BaseExperience, WorkplaceFields {
  category: 'Workplace'
  type: WorkplaceType
}

/**
 * Skills experience
 */
export interface SkillsExperience extends BaseExperience, SkillsFields {
  category: 'Skills'
  type: SkillsType
}

/**
 * Union type for all experience variants
 */
export type Experience = EducationExperience | WorkplaceExperience | SkillsExperience

/**
 * Experience creation payload (polymorphic)
 */
export type CreateExperiencePayload =
  | (Partial<BaseExperience> & Partial<EducationFields>)
  | (Partial<BaseExperience> & Partial<WorkplaceFields>)
  | (Partial<BaseExperience> & Partial<SkillsFields>)

/**
 * Experience update payload (polymorphic)
 */
export type UpdateExperiencePayload = Partial<CreateExperiencePayload>

/**
 * Experience filter options
 */
export interface ExperienceFilterOptions {
  search?: string
  userId?: string
  category?: ExperienceCategory
  type?: ExperienceType
  naicsCode?: string
  isCurrent?: boolean
  dateRange?: {
    from?: string
    to?: string
  }
}

/**
 * Experience statistics
 */
export interface ExperienceStats {
  totalExperiences: number
  byCategory: Record<ExperienceCategory, number>
  byType: Record<ExperienceType, number>
  recentlyAdded: number
}
