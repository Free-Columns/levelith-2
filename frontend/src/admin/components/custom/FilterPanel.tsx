/**
 * FilterPanel Component
 *
 * @module admin/components/custom/FilterPanel
 */

import * as React from 'react'
import { Filter, X } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface FilterOption {
  label: string
  value: string
}

export interface FilterPanelProps {
  /**
   * Panel title
   */
  title?: string
  /**
   * Show/hide panel
   */
  isOpen: boolean
  /**
   * Callback to toggle panel
   */
  onToggle: () => void
  /**
   * Filter content (render prop)
   */
  children: React.ReactNode
  /**
   * Callback to clear all filters
   */
  onClear?: () => void
  /**
   * Number of active filters (for badge)
   */
  activeFilters?: number
  /**
   * Additional CSS classes
   */
  className?: string
}

/**
 * Collapsible filter panel with clear button
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false)
 *
 * <FilterPanel
 *   title="Filters"
 *   isOpen={isOpen}
 *   onToggle={() => setIsOpen(!isOpen)}
 *   onClear={() => resetFilters()}
 *   activeFilters={2}
 * >
 *   <FilterSelect label="Status" options={statusOptions} />
 *   <FilterSelect label="Role" options={roleOptions} />
 * </FilterPanel>
 * ```
 */
export function FilterPanel({
  title = 'Filters',
  isOpen,
  onToggle,
  children,
  onClear,
  activeFilters = 0,
  className,
}: FilterPanelProps) {
  return (
    <div className={cn('border rounded-lg', className)}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <button
          onClick={onToggle}
          className="flex items-center gap-2 text-sm font-medium hover:text-primary"
        >
          <Filter className="h-4 w-4" />
          <span>{title}</span>
          {activeFilters > 0 && (
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
              {activeFilters}
            </span>
          )}
        </button>

        {activeFilters > 0 && onClear && (
          <button
            onClick={onClear}
            className="text-xs text-muted-foreground hover:text-foreground"
          >
            Clear all
          </button>
        )}
      </div>

      {/* Content */}
      {isOpen && (
        <div className="p-4 space-y-4">
          {children}
        </div>
      )}
    </div>
  )
}

/**
 * Individual filter item
 */
export interface FilterItemProps {
  label: string
  children: React.ReactNode
  className?: string
}

export function FilterItem({ label, children, className }: FilterItemProps) {
  return (
    <div className={cn('space-y-2', className)}>
      <label className="text-sm font-medium">{label}</label>
      {children}
    </div>
  )
}

/**
 * Quick filter chips/tags
 */
export interface QuickFiltersProps {
  filters: Array<{ key: string; label: string; value: string }>
  onRemove: (key: string) => void
  onClearAll: () => void
  className?: string
}

export function QuickFilters({ filters, onRemove, onClearAll, className }: QuickFiltersProps) {
  if (filters.length === 0) return null

  return (
    <div className={cn('flex flex-wrap items-center gap-2', className)}>
      <span className="text-sm text-muted-foreground">Active filters:</span>
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onRemove(filter.key)}
          className={cn(
            'inline-flex items-center gap-1 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium',
            'hover:bg-primary/20 transition-colors'
          )}
        >
          <span>{filter.label}: {filter.value}</span>
          <X className="h-3 w-3" />
        </button>
      ))}
      {filters.length > 1 && (
        <button
          onClick={onClearAll}
          className="text-xs text-muted-foreground hover:text-foreground underline"
        >
          Clear all
        </button>
      )}
    </div>
  )
}
