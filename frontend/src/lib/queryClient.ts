import { QueryClient } from '@tanstack/react-query'

/**
 * React Query client configuration for admin dashboard
 *
 * Configuration:
 * - Default stale time: 5 minutes (data considered fresh for 5 minutes)
 * - Default cache time: 10 minutes (unused data garbage collected after 10 minutes)
 * - Retry: 1 time on failure (prevents excessive retries)
 * - refetchOnWindowFocus: false (prevents unnecessary refetches)
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
      refetchOnMount: true,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 0, // Don't retry mutations by default
    },
  },
})
