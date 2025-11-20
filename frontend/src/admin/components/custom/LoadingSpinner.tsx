/**
 * Loading Spinner Component
 *
 * @module admin/components/custom/LoadingSpinner
 */

import { cn } from '@/lib/utils'

export interface LoadingSpinnerProps {
  /**
   * Size variant
   */
  size?: 'sm' | 'md' | 'lg'
  /**
   * Additional CSS classes
   */
  className?: string
  /**
   * Label text (for accessibility)
   */
  label?: string
}

const sizeClasses = {
  sm: 'h-4 w-4 border-2',
  md: 'h-8 w-8 border-2',
  lg: 'h-12 w-12 border-3',
}

/**
 * Animated loading spinner
 *
 * @example
 * ```tsx
 * <LoadingSpinner size="md" label="Loading users..." />
 * ```
 */
export function LoadingSpinner({ size = 'md', className, label = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <div className={cn('flex items-center justify-center', className)} role="status" aria-label={label}>
      <div
        className={cn(
          'animate-spin rounded-full border-gray-200 border-t-primary',
          sizeClasses[size]
        )}
      />
      <span className="sr-only">{label}</span>
    </div>
  )
}

/**
 * Fullscreen loading overlay
 */
export function LoadingOverlay({ label = 'Loading...' }: { label?: string }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
      <div className="flex flex-col items-center gap-4">
        <LoadingSpinner size="lg" label={label} />
        <p className="text-sm text-muted-foreground">{label}</p>
      </div>
    </div>
  )
}

/**
 * Inline loading indicator
 */
export function LoadingInline({ label = 'Loading...' }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <LoadingSpinner size="sm" label={label} />
      <span>{label}</span>
    </div>
  )
}
