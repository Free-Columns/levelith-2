/**
 * Constants and configuration values for admin dashboard
 *
 * @module admin/lib/constants
 */

/**
 * API configuration
 */
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
} as const

/**
 * Pagination configuration
 */
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100,
} as const

/**
 * Table configuration
 */
export const TABLE_CONFIG = {
  DEFAULT_SORT_ORDER: 'asc' as const,
  EMPTY_MESSAGE: 'No data available',
  LOADING_MESSAGE: 'Loading...',
} as const

/**
 * Experience categories
 */
export const EXPERIENCE_CATEGORIES = {
  EDUCATION: 'Education',
  WORKPLACE: 'Workplace',
  SKILLS: 'Skills',
} as const

/**
 * Education experience types
 */
export const EDUCATION_TYPES = {
  CERTIFICATE: 'Certificate',
  DEGREE: 'Degree',
  COURSE: 'Course',
} as const

/**
 * Workplace experience types
 */
export const WORKPLACE_TYPES = {
  GIG: 'Gig',
  PART_TIME: 'Part-Time',
  FULL_TIME: 'Full-Time',
} as const

/**
 * Skills experience types
 */
export const SKILLS_TYPES = {
  SOFT_SKILLS: 'Soft Skills',
  HARD_SKILLS: 'Hard Skills',
  NATIVE_SKILLS: 'Native Skills',
} as const

/**
 * All experience types combined
 */
export const ALL_EXPERIENCE_TYPES = {
  ...EDUCATION_TYPES,
  ...WORKPLACE_TYPES,
  ...SKILLS_TYPES,
} as const

/**
 * Proficiency levels for skills
 */
export const PROFICIENCY_LEVELS = {
  BEGINNER: 'Beginner',
  INTERMEDIATE: 'Intermediate',
  ADVANCED: 'Advanced',
  EXPERT: 'Expert',
} as const

/**
 * NAICS code levels
 */
export const NAICS_LEVELS = {
  TWO_DIGIT: 2,
  THREE_DIGIT: 3,
  FOUR_DIGIT: 4,
  SIX_DIGIT: 6,
} as const

/**
 * NAICS fallback code for "GENERAL" category
 */
export const NAICS_GENERAL_CODE = '123456' as const

/**
 * Entity status values
 */
export const ENTITY_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  DELETED: 'deleted',
} as const

/**
 * Date format strings
 */
export const DATE_FORMATS = {
  SHORT: 'MMM dd, yyyy',
  LONG: 'MMMM dd, yyyy',
  WITH_TIME: 'MMM dd, yyyy HH:mm',
  FULL: 'EEEE, MMMM dd, yyyy HH:mm:ss',
  ISO: "yyyy-MM-dd'T'HH:mm:ss",
} as const

/**
 * Validation constraints
 */
export const VALIDATION = {
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 50,
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_MAX_LENGTH: 128,
  EMAIL_MAX_LENGTH: 255,
  TITLE_MAX_LENGTH: 255,
  DESCRIPTION_MAX_LENGTH: 2000,
  BIO_MAX_LENGTH: 500,
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
} as const

/**
 * Toast notification configuration
 */
export const TOAST_CONFIG = {
  DURATION: 5000, // 5 seconds
  POSITION: 'bottom-right' as const,
} as const

/**
 * Query configuration for React Query
 */
export const QUERY_CONFIG = {
  STALE_TIME: 5 * 60 * 1000, // 5 minutes
  CACHE_TIME: 10 * 60 * 1000, // 10 minutes
  RETRY_ATTEMPTS: 1,
} as const

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'adminToken',
  USER_PREFERENCES: 'adminUserPreferences',
  TABLE_SETTINGS: 'adminTableSettings',
  THEME: 'adminTheme',
} as const

/**
 * Route paths
 */
export const ROUTES = {
  DASHBOARD: '/admin',
  USERS: '/admin/users',
  EXPERIENCES: '/admin/experiences',
  NAICS: '/admin/naics',
  SETTINGS: '/admin/settings',
  LOGIN: '/admin/login',
} as const

/**
 * HTTP status codes
 */
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
} as const

/**
 * Error messages
 */
export const ERROR_MESSAGES = {
  GENERIC: 'An error occurred. Please try again.',
  NETWORK: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION: 'Please check your input and try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
} as const
