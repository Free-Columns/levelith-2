/**
 * Tests for API transformation utilities
 *
 * @module lib/__tests__/transformers.test
 */

import { describe, it, expect } from 'vitest'
import {
  snakeToCamel,
  camelToSnake,
  keysToCamel,
  keysToSnake,
  transformPaginatedResponse,
} from '../transformers'

describe('snakeToCamel', () => {
  it('converts snake_case to camelCase', () => {
    expect(snakeToCamel('user_name')).toBe('userName')
    expect(snakeToCamel('is_active')).toBe('isActive')
    expect(snakeToCamel('created_at')).toBe('createdAt')
    expect(snakeToCamel('last_login_at')).toBe('lastLoginAt')
  })

  it('handles strings without underscores', () => {
    expect(snakeToCamel('username')).toBe('username')
    expect(snakeToCamel('email')).toBe('email')
  })

  it('handles empty strings', () => {
    expect(snakeToCamel('')).toBe('')
  })
})

describe('camelToSnake', () => {
  it('converts camelCase to snake_case', () => {
    expect(camelToSnake('userName')).toBe('user_name')
    expect(camelToSnake('isActive')).toBe('is_active')
    expect(camelToSnake('createdAt')).toBe('created_at')
    expect(camelToSnake('lastLoginAt')).toBe('last_login_at')
  })

  it('handles strings without uppercase letters', () => {
    expect(camelToSnake('username')).toBe('username')
    expect(camelToSnake('email')).toBe('email')
  })

  it('handles empty strings', () => {
    expect(camelToSnake('')).toBe('')
  })
})

describe('keysToCamel', () => {
  it('transforms object keys from snake_case to camelCase', () => {
    const input = {
      user_name: 'john',
      is_active: true,
      created_at: '2025-01-01',
    }

    const expected = {
      userName: 'john',
      isActive: true,
      createdAt: '2025-01-01',
    }

    expect(keysToCamel(input)).toEqual(expected)
  })

  it('transforms nested objects', () => {
    const input = {
      user_name: 'john',
      profile_data: {
        first_name: 'John',
        last_name: 'Doe',
        contact_info: {
          phone_number: '123-456-7890',
        },
      },
    }

    const expected = {
      userName: 'john',
      profileData: {
        firstName: 'John',
        lastName: 'Doe',
        contactInfo: {
          phoneNumber: '123-456-7890',
        },
      },
    }

    expect(keysToCamel(input)).toEqual(expected)
  })

  it('transforms arrays of objects', () => {
    const input = [
      { user_name: 'john', is_active: true },
      { user_name: 'jane', is_active: false },
    ]

    const expected = [
      { userName: 'john', isActive: true },
      { userName: 'jane', isActive: false },
    ]

    expect(keysToCamel(input)).toEqual(expected)
  })

  it('handles null and undefined values', () => {
    expect(keysToCamel(null)).toBe(null)
    expect(keysToCamel(undefined)).toBe(undefined)
  })

  it('handles primitive values', () => {
    expect(keysToCamel('string')).toBe('string')
    expect(keysToCamel(123)).toBe(123)
    expect(keysToCamel(true)).toBe(true)
  })

  it('handles Date objects', () => {
    const date = new Date('2025-01-01')
    expect(keysToCamel(date)).toBe(date)
  })

  it('handles arrays of primitives', () => {
    const input = [1, 2, 3, 'test']
    expect(keysToCamel(input)).toEqual(input)
  })
})

describe('keysToSnake', () => {
  it('transforms object keys from camelCase to snake_case', () => {
    const input = {
      userName: 'john',
      isActive: true,
      createdAt: '2025-01-01',
    }

    const expected = {
      user_name: 'john',
      is_active: true,
      created_at: '2025-01-01',
    }

    expect(keysToSnake(input)).toEqual(expected)
  })

  it('transforms nested objects', () => {
    const input = {
      userName: 'john',
      profileData: {
        firstName: 'John',
        lastName: 'Doe',
        contactInfo: {
          phoneNumber: '123-456-7890',
        },
      },
    }

    const expected = {
      user_name: 'john',
      profile_data: {
        first_name: 'John',
        last_name: 'Doe',
        contact_info: {
          phone_number: '123-456-7890',
        },
      },
    }

    expect(keysToSnake(input)).toEqual(expected)
  })

  it('transforms arrays of objects', () => {
    const input = [
      { userName: 'john', isActive: true },
      { userName: 'jane', isActive: false },
    ]

    const expected = [
      { user_name: 'john', is_active: true },
      { user_name: 'jane', is_active: false },
    ]

    expect(keysToSnake(input)).toEqual(expected)
  })

  it('handles null and undefined values', () => {
    expect(keysToSnake(null)).toBe(null)
    expect(keysToSnake(undefined)).toBe(undefined)
  })

  it('handles primitive values', () => {
    expect(keysToSnake('string')).toBe('string')
    expect(keysToSnake(123)).toBe(123)
    expect(keysToSnake(true)).toBe(true)
  })
})

describe('transformPaginatedResponse', () => {
  it('transforms backend paginated response with items array', () => {
    const backendResponse = {
      items: [
        { user_name: 'john', is_active: true },
        { user_name: 'jane', is_active: false },
      ],
      total: 100,
      page: 1,
      page_size: 50,
      total_pages: 2,
    }

    const result = transformPaginatedResponse(backendResponse)

    expect(result).toEqual({
      data: [
        { userName: 'john', isActive: true },
        { userName: 'jane', isActive: false },
      ],
      total: 100,
      page: 1,
      pageSize: 50,
      totalPages: 2,
    })
  })

  it('transforms backend paginated response with data array', () => {
    const backendResponse = {
      data: [
        { user_name: 'john', is_active: true },
      ],
      total: 1,
      page: 1,
      page_size: 50,
      total_pages: 1,
    }

    const result = transformPaginatedResponse(backendResponse)

    expect(result.data[0]).toEqual({ userName: 'john', isActive: true })
    expect(result.total).toBe(1)
  })

  it('handles direct array response', () => {
    const backendResponse = [
      { user_name: 'john', is_active: true },
      { user_name: 'jane', is_active: false },
    ]

    const result = transformPaginatedResponse(backendResponse)

    expect(result.data).toEqual([
      { userName: 'john', isActive: true },
      { userName: 'jane', isActive: false },
    ])
    expect(result.total).toBe(0)
    expect(result.page).toBe(1)
  })

  it('handles empty array', () => {
    const backendResponse = {
      items: [],
      total: 0,
      page: 1,
      page_size: 50,
      total_pages: 0,
    }

    const result = transformPaginatedResponse(backendResponse)

    expect(result.data).toEqual([])
    expect(result.total).toBe(0)
  })

  it('handles response with nested objects', () => {
    const backendResponse = {
      items: [
        {
          user_name: 'john',
          profile_data: {
            first_name: 'John',
            last_name: 'Doe',
          },
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
      total_pages: 1,
    }

    const result = transformPaginatedResponse(backendResponse)

    expect(result.data[0]).toEqual({
      userName: 'john',
      profileData: {
        firstName: 'John',
        lastName: 'Doe',
      },
    })
  })

  it('provides default values for missing pagination metadata', () => {
    const backendResponse = {
      items: [{ user_name: 'john' }],
    }

    const result = transformPaginatedResponse(backendResponse)

    expect(result.total).toBe(0)
    expect(result.page).toBe(1)
    expect(result.pageSize).toBe(50)
    expect(result.totalPages).toBe(1)
  })
})
