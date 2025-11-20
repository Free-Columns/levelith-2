/**
 * Zod validation schemas for NAICS entities
 *
 * @module admin/features/naics/schemas
 */

import { z } from 'zod'

/**
 * NAICS level enum
 */
export const naicsLevelEnum = z.enum(['2', '3', '4', '6'])

/**
 * Create NAICS schema
 */
export const createNAICSSchema = z.object({
  code: z
    .string()
    .regex(/^\d{2,6}$/, 'NAICS code must be 2, 3, 4, or 6 digits')
    .refine(
      (code) => [2, 3, 4, 6].includes(code.length),
      'NAICS code must be exactly 2, 3, 4, or 6 digits'
    ),
  title: z.string().min(1, 'Title is required').max(500),
  description: z.string().max(2000).optional(),
  level: z.number().refine((val) => [2, 3, 4, 6].includes(val), 'Level must be 2, 3, 4, or 6'),
  parentCode: z
    .string()
    .regex(/^\d{2,4}$/, 'Parent code must be 2, 3, or 4 digits')
    .optional(),
  tags: z.array(z.string()).default([]),
  customCategory: z.string().max(100).optional(),
  adminNotes: z.string().max(1000).optional(),
  isActive: z.boolean().default(true),
})

/**
 * Update NAICS schema (all fields optional except validation rules)
 */
export const updateNAICSSchema = z.object({
  title: z.string().min(1, 'Title is required').max(500).optional(),
  description: z.string().max(2000).optional(),
  tags: z.array(z.string()).optional(),
  customCategory: z.string().max(100).optional(),
  adminNotes: z.string().max(1000).optional(),
  isActive: z.boolean().optional(),
})

/**
 * NAICS filter schema
 */
export const naicsFilterSchema = z.object({
  search: z.string().optional(),
  level: z.number().refine((val) => [2, 3, 4, 6].includes(val)).optional(),
  customCategory: z.string().optional(),
  tags: z.array(z.string()).optional(),
  isActive: z.boolean().optional(),
  hasExperiences: z.boolean().optional(),
})

/**
 * Inferred types from schemas
 */
export type CreateNAICSFormData = z.infer<typeof createNAICSSchema>
export type UpdateNAICSFormData = z.infer<typeof updateNAICSSchema>
export type NAICSFilterFormData = z.infer<typeof naicsFilterSchema>
