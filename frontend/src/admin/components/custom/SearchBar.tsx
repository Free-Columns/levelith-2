/**
 * SearchBar Component
 *
 * @module admin/components/custom/SearchBar
 */

import { Search, X } from 'lucide-react'
import { useState } from 'react'
import { useDebounce } from '@/admin/hooks/useDebounce'
import { cn } from '@/lib/utils'

export interface SearchBarProps {
  /**
   * Search value
   */
  value?: string
  /**
   * Callback when search value changes (debounced)
   */
  onSearch: (value: string) => void
  /**
   * Placeholder text
   */
  placeholder?: string
  /**
   * Debounce delay in milliseconds
   */
  debounceDelay?: number
  /**
   * Additional CSS classes
   */
  className?: string
  /**
   * Disable the search bar
   */
  disabled?: boolean
}

/**
 * Search input with debouncing and clear button
 *
 * @example
 * ```tsx
 * <SearchBar
 *   placeholder="Search users..."
 *   onSearch={(value) => setSearchQuery(value)}
 *   debounceDelay={300}
 * />
 * ```
 */
export function SearchBar({
  value: controlledValue,
  onSearch,
  placeholder = 'Search...',
  debounceDelay = 500,
  className,
  disabled = false,
}: SearchBarProps) {
  const [internalValue, setInternalValue] = useState(controlledValue || '')
  const debouncedValue = useDebounce(internalValue, debounceDelay)

  // Call onSearch when debounced value changes
  React.useEffect(() => {
    onSearch(debouncedValue)
  }, [debouncedValue, onSearch])

  // Update internal value when controlled value changes
  React.useEffect(() => {
    if (controlledValue !== undefined) {
      setInternalValue(controlledValue)
    }
  }, [controlledValue])

  const handleClear = () => {
    setInternalValue('')
    onSearch('')
  }

  return (
    <div className={cn('relative flex items-center', className)}>
      <Search className="absolute left-3 h-4 w-4 text-muted-foreground" />
      <input
        type="text"
        value={internalValue}
        onChange={(e) => setInternalValue(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={cn(
          'flex h-10 w-full rounded-md border border-input bg-background px-10 py-2 text-sm',
          'ring-offset-background placeholder:text-muted-foreground',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50'
        )}
      />
      {internalValue && !disabled && (
        <button
          type="button"
          onClick={handleClear}
          className="absolute right-3 text-muted-foreground hover:text-foreground"
          aria-label="Clear search"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  )
}

// Fix React import
import * as React from 'react'
