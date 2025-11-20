/**
 * Zod validation schemas for experience entities
 *
 * @module admin/features/experiences/schemas
 */

import { z } from 'zod'

/**
 * Experience category enum
 */
export const experienceCategoryEnum = z.enum(['Education', 'Workplace', 'Skills'])

/**
 * Experience type enums
 */
export const educationTypeEnum = z.enum(['Certificate', 'Degree', 'Course'])
export const workplaceTypeEnum = z.enum(['Gig', 'Part-Time', 'Full-Time'])
export const skillsTypeEnum = z.enum(['Soft Skills', 'Hard Skills', 'Native Skills'])

/**
 * Proficiency level enum
 */
export const proficiencyLevelEnum = z.enum(['Beginner', 'Intermediate', 'Advanced', 'Expert'])

/**
 * Base experience schema (common fields)
 */
export const baseExperienceSchema = z.object({
  userId: z.string().uuid().optional(),
  category: experienceCategoryEnum,
  type: z.string(),
  title: z.string().min(1, 'Title is required').max(255),
  description: z.string().max(2000).optional(),
  startDate: z.string().datetime().optional(),
  endDate: z.string().datetime().optional(),
  isCurrent: z.boolean().default(false),
  naicsCode: z.string().regex(/^\d{6}$/, 'NAICS code must be 6 digits'),
  skillsGained: z.array(z.string()).default([]),
  metadata: z.record(z.any()).default({}),
})

/**
 * Education experience schema
 */
export const educationExperienceSchema = baseExperienceSchema.extend({
  category: z.literal('Education'),
  type: educationTypeEnum,
  institution: z.string().min(1, 'Institution is required').max(255),
  fieldOfStudy: z.string().max(255).optional(),
  degreeLevel: z.string().optional(),
  grade: z.string().optional(),
  credentialId: z.string().optional(),
  credentialUrl: z.string().url().optional(),
})

/**
 * Workplace experience schema
 */
export const workplaceExperienceSchema = baseExperienceSchema.extend({
  category: z.literal('Workplace'),
  type: workplaceTypeEnum,
  company: z.string().min(1, 'Company is required').max(255),
  position: z.string().min(1, 'Position is required').max(255),
  location: z.string().max(255).optional(),
  employmentType: z.string().optional(),
  responsibilities: z.array(z.string()).default([]),
  achievements: z.array(z.string()).default([]),
})

/**
 * Skills experience schema
 */
export const skillsExperienceSchema = baseExperienceSchema.extend({
  category: z.literal('Skills'),
  type: skillsTypeEnum,
  proficiencyLevel: proficiencyLevelEnum.optional(),
  yearsOfExperience: z.number().min(0).optional(),
  endorsements: z.number().min(0).default(0),
})

/**
 * Discriminated union for creating experiences
 */
export const createExperienceSchema = z.discriminatedUnion('category', [
  educationExperienceSchema,
  workplaceExperienceSchema,
  skillsExperienceSchema,
])

/**
 * Update experience schema (partial with category discrimination)
 */
export const updateExperienceSchema = z.discriminatedUnion('category', [
  educationExperienceSchema.partial(),
  workplaceExperienceSchema.partial(),
  skillsExperienceSchema.partial(),
])

/**
 * Experience filter schema
 */
export const experienceFilterSchema = z.object({
  search: z.string().optional(),
  userId: z.string().uuid().optional(),
  category: experienceCategoryEnum.optional(),
  type: z.string().optional(),
  naicsCode: z.string().optional(),
  isCurrent: z.boolean().optional(),
  dateRange: z
    .object({
      from: z.string().datetime().optional(),
      to: z.string().datetime().optional(),
    })
    .optional(),
})

/**
 * Inferred types from schemas
 */
export type CreateExperienceFormData = z.infer<typeof createExperienceSchema>
export type UpdateExperienceFormData = z.infer<typeof updateExperienceSchema>
export type ExperienceFilterFormData = z.infer<typeof experienceFilterSchema>
