/**
 * Error Boundary Component
 *
 * @module admin/components/custom/ErrorBoundary
 */

import React, { Component, ErrorInfo, ReactNode } from 'react'

export interface ErrorBoundaryProps {
  /**
   * Child components to render
   */
  children: ReactNode
  /**
   * Custom fallback UI
   */
  fallback?: (error: Error, reset: () => void) => ReactNode
  /**
   * Callback when error is caught
   */
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

export interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

/**
 * Error boundary to catch and display React errors
 *
 * @example
 * ```tsx
 * <ErrorBoundary>
 *   <MyComponent />
 * </ErrorBoundary>
 * ```
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
    }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('Error caught by ErrorBoundary:', error, errorInfo)
    this.props.onError?.(error, errorInfo)
  }

  resetError = (): void => {
    this.setState({
      hasError: false,
      error: null,
    })
  }

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.resetError)
      }

      return <DefaultErrorFallback error={this.state.error} reset={this.resetError} />
    }

    return this.props.children
  }
}

/**
 * Default error fallback UI
 */
function DefaultErrorFallback({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center gap-4 p-8">
      <div className="rounded-lg border border-destructive bg-destructive/10 p-6 max-w-2xl">
        <h2 className="text-2xl font-bold text-destructive mb-2">Something went wrong</h2>
        <p className="text-sm text-muted-foreground mb-4">
          An error occurred while rendering this component.
        </p>

        {/* Error details (development only) */}
        {import.meta.env.DEV && (
          <details className="mb-4">
            <summary className="cursor-pointer text-sm font-medium">Error details</summary>
            <pre className="mt-2 overflow-auto rounded bg-muted p-4 text-xs">
              {error.message}
              {'\n\n'}
              {error.stack}
            </pre>
          </details>
        )}

        <button
          onClick={reset}
          className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          Try again
        </button>
      </div>
    </div>
  )
}

/**
 * Hook-based error boundary for functional components
 * Note: This is a simplified version. For full hook support, use react-error-boundary library
 */
export function useErrorBoundary() {
  const [error, setError] = React.useState<Error | null>(null)

  React.useEffect(() => {
    if (error) {
      throw error
    }
  }, [error])

  const resetError = React.useCallback(() => {
    setError(null)
  }, [])

  return {
    error,
    setError,
    resetError,
  }
}
