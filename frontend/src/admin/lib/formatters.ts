/**
 * Formatting utility functions for admin dashboard
 *
 * @module admin/lib/formatters
 */

import { format, formatDistance, formatRelative, parseISO } from 'date-fns'

/**
 * Format date to human-readable string
 *
 * @param date - Date string or Date object
 * @param formatString - Format pattern (default: 'MMM dd, yyyy')
 * @returns Formatted date string
 */
export function formatDate(date: string | Date | undefined, formatString = 'MMM dd, yyyy'): string {
  if (!date) return 'N/A'
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return format(dateObj, formatString)
  } catch {
    return 'Invalid date'
  }
}

/**
 * Format date with time
 *
 * @param date - Date string or Date object
 * @returns Formatted date and time string
 */
export function formatDateTime(date: string | Date | undefined): string {
  return formatDate(date, 'MMM dd, yyyy HH:mm')
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 *
 * @param date - Date string or Date object
 * @returns Relative time string
 */
export function formatRelativeDate(date: string | Date | undefined): string {
  if (!date) return 'N/A'
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return formatDistance(dateObj, new Date(), { addSuffix: true })
  } catch {
    return 'Invalid date'
  }
}

/**
 * Format date to relative with context (e.g., "yesterday at 3:54 PM")
 *
 * @param date - Date string or Date object
 * @returns Relative date string with context
 */
export function formatRelativeWithContext(date: string | Date | undefined): string {
  if (!date) return 'N/A'
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return formatRelative(dateObj, new Date())
  } catch {
    return 'Invalid date'
  }
}

/**
 * Format currency amount
 *
 * @param amount - Numeric amount
 * @param currency - Currency code (default: 'USD')
 * @returns Formatted currency string
 */
export function formatCurrency(amount: number | undefined, currency = 'USD'): string {
  if (amount === undefined || amount === null) return 'N/A'
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
    }).format(amount)
  } catch {
    return `${currency} ${amount}`
  }
}

/**
 * Format number with thousand separators
 *
 * @param num - Number to format
 * @returns Formatted number string
 */
export function formatNumber(num: number | undefined): string {
  if (num === undefined || num === null) return 'N/A'
  return new Intl.NumberFormat('en-US').format(num)
}

/**
 * Format percentage
 *
 * @param value - Decimal value (0.85 = 85%)
 * @param decimals - Number of decimal places (default: 0)
 * @returns Formatted percentage string
 */
export function formatPercentage(value: number | undefined, decimals = 0): string {
  if (value === undefined || value === null) return 'N/A'
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * Truncate text with ellipsis
 *
 * @param text - Text to truncate
 * @param maxLength - Maximum length before truncation
 * @returns Truncated text
 */
export function truncateText(text: string | undefined, maxLength = 50): string {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return `${text.substring(0, maxLength)}...`
}

/**
 * Format file size to human-readable format
 *
 * @param bytes - Size in bytes
 * @returns Formatted size string (e.g., "1.5 MB")
 */
export function formatFileSize(bytes: number | undefined): string {
  if (bytes === undefined || bytes === null) return 'N/A'
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

/**
 * Format phone number to US format
 *
 * @param phone - Phone number string
 * @returns Formatted phone number
 */
export function formatPhoneNumber(phone: string | undefined): string {
  if (!phone) return 'N/A'
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length === 10) {
    return `(${cleaned.substring(0, 3)}) ${cleaned.substring(3, 6)}-${cleaned.substring(6)}`
  }
  return phone
}

/**
 * Format boolean as Yes/No
 *
 * @param value - Boolean value
 * @returns "Yes" or "No"
 */
export function formatBoolean(value: boolean | undefined): string {
  if (value === undefined || value === null) return 'N/A'
  return value ? 'Yes' : 'No'
}

/**
 * Format array as comma-separated list
 *
 * @param items - Array of strings
 * @param maxItems - Maximum items before "and X more"
 * @returns Formatted list string
 */
export function formatList(items: string[] | undefined, maxItems = 3): string {
  if (!items || items.length === 0) return 'None'
  if (items.length <= maxItems) return items.join(', ')
  const visible = items.slice(0, maxItems).join(', ')
  const remaining = items.length - maxItems
  return `${visible}, and ${remaining} more`
}
