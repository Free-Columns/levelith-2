import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

/**
 * API client configuration for admin dashboard
 *
 * Features:
 * - Centralized axios instance
 * - Request/response interceptors
 * - Error handling
 * - Type-safe API methods
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

/**
 * Create axios instance with default configuration
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor
 * Add authentication tokens, logging, etc.
 */
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('adminToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`)
    }

    return config
  },
  (error) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

/**
 * Response interceptor
 * Handle errors, transform responses, etc.
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status)
    }

    return response
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const status = error.response.status
      const message = error.response.data?.message || error.message

      switch (status) {
        case 401:
          console.error('[API] Unauthorized - redirecting to login')
          // Could trigger logout or redirect here
          break
        case 403:
          console.error('[API] Forbidden')
          break
        case 404:
          console.error('[API] Not found')
          break
        case 500:
          console.error('[API] Server error')
          break
        default:
          console.error(`[API] Error ${status}: ${message}`)
      }
    } else if (error.request) {
      // Request made but no response
      console.error('[API] No response from server')
    } else {
      // Error in request setup
      console.error('[API] Request error:', error.message)
    }

    return Promise.reject(error)
  }
)

/**
 * Type-safe API request wrapper
 */
export const api = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> =>
    apiClient.get<T>(url, config).then((res) => res.data),

  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> =>
    apiClient.post<T>(url, data, config).then((res) => res.data),

  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> =>
    apiClient.put<T>(url, data, config).then((res) => res.data),

  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> =>
    apiClient.patch<T>(url, data, config).then((res) => res.data),

  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> =>
    apiClient.delete<T>(url, config).then((res) => res.data),
}

export default apiClient
