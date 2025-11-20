/**
 * Validation utility functions for admin dashboard
 *
 * @module admin/lib/validators
 */

/**
 * Validate email format
 *
 * @param email - Email address to validate
 * @returns True if valid email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate URL format
 *
 * @param url - URL to validate
 * @returns True if valid URL format
 */
export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Validate UUID format
 *
 * @param uuid - UUID string to validate
 * @returns True if valid UUID format
 */
export function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
  return uuidRegex.test(uuid)
}

/**
 * Validate NAICS code format (6 digits)
 *
 * @param code - NAICS code to validate
 * @returns True if valid NAICS code
 */
export function isValidNAICSCode(code: string): boolean {
  return /^\d{6}$/.test(code)
}

/**
 * Validate phone number format (US)
 *
 * @param phone - Phone number to validate
 * @returns True if valid US phone number
 */
export function isValidPhoneNumber(phone: string): boolean {
  const cleaned = phone.replace(/\D/g, '')
  return cleaned.length === 10 || cleaned.length === 11
}

/**
 * Validate password strength
 *
 * @param password - Password to validate
 * @returns Object with validation results
 */
export function validatePasswordStrength(password: string): {
  isValid: boolean
  errors: string[]
  strength: 'weak' | 'medium' | 'strong'
} {
  const errors: string[] = []

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters')
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number')
  }

  if (!/[^A-Za-z0-9]/.test(password)) {
    errors.push('Password must contain at least one special character')
  }

  const isValid = errors.length === 0

  let strength: 'weak' | 'medium' | 'strong' = 'weak'
  if (isValid) {
    if (password.length >= 12 && /[^A-Za-z0-9]/.test(password)) {
      strength = 'strong'
    } else {
      strength = 'medium'
    }
  }

  return { isValid, errors, strength }
}

/**
 * Validate date range
 *
 * @param startDate - Start date
 * @param endDate - End date
 * @returns True if valid date range (end after start)
 */
export function isValidDateRange(startDate: string | Date, endDate: string | Date): boolean {
  try {
    const start = new Date(startDate)
    const end = new Date(endDate)
    return end >= start
  } catch {
    return false
  }
}

/**
 * Validate file size
 *
 * @param fileSize - File size in bytes
 * @param maxSize - Maximum allowed size in bytes
 * @returns True if file size is within limit
 */
export function isValidFileSize(fileSize: number, maxSize: number): boolean {
  return fileSize <= maxSize
}

/**
 * Validate file type
 *
 * @param fileName - File name
 * @param allowedExtensions - Array of allowed extensions (e.g., ['.jpg', '.png'])
 * @returns True if file type is allowed
 */
export function isValidFileType(fileName: string, allowedExtensions: string[]): boolean {
  const extension = fileName.toLowerCase().substring(fileName.lastIndexOf('.'))
  return allowedExtensions.includes(extension)
}

/**
 * Sanitize input (remove potentially dangerous characters)
 *
 * @param input - Input string to sanitize
 * @returns Sanitized string
 */
export function sanitizeInput(input: string): string {
  return input
    .replace(/[<>]/g, '') // Remove HTML tags
    .replace(/['"]/g, '') // Remove quotes
    .trim()
}

/**
 * Validate username format
 *
 * @param username - Username to validate
 * @returns True if valid username format
 */
export function isValidUsername(username: string): boolean {
  // 3-50 characters, alphanumeric, underscores, and hyphens only
  return /^[a-zA-Z0-9_-]{3,50}$/.test(username)
}
