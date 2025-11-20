/**
 * Pagination Component
 *
 * @module admin/components/custom/Pagination
 */

import * as React from 'react'
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react'
import { cn } from '@/lib/utils'
import { PAGINATION_CONFIG } from '@/admin/lib/constants'

export interface PaginationProps {
  /**
   * Current page (1-indexed)
   */
  currentPage: number
  /**
   * Total number of pages
   */
  totalPages: number
  /**
   * Callback when page changes
   */
  onPageChange: (page: number) => void
  /**
   * Items per page
   */
  pageSize?: number
  /**
   * Callback when page size changes
   */
  onPageSizeChange?: (pageSize: number) => void
  /**
   * Total number of items
   */
  totalItems?: number
  /**
   * Show page size selector
   */
  showPageSize?: boolean
  /**
   * Additional CSS classes
   */
  className?: string
}

/**
 * Pagination controls with page numbers and navigation
 *
 * @example
 * ```tsx
 * <Pagination
 *   currentPage={page}
 *   totalPages={Math.ceil(totalUsers / pageSize)}
 *   onPageChange={setPage}
 *   pageSize={pageSize}
 *   onPageSizeChange={setPageSize}
 *   totalItems={totalUsers}
 *   showPageSize
 * />
 * ```
 */
export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  pageSize = PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
  onPageSizeChange,
  totalItems,
  showPageSize = true,
  className,
}: PaginationProps) {
  const canPreviousPage = currentPage > 1
  const canNextPage = currentPage < totalPages

  // Generate page numbers to display
  const getPageNumbers = (): (number | 'ellipsis')[] => {
    const pages: (number | 'ellipsis')[] = []
    const maxVisible = 5

    if (totalPages <= maxVisible + 2) {
      // Show all pages if total is small
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      // Always show first page
      pages.push(1)

      if (currentPage > 3) {
        pages.push('ellipsis')
      }

      // Show pages around current page
      const startPage = Math.max(2, currentPage - 1)
      const endPage = Math.min(totalPages - 1, currentPage + 1)

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }

      if (currentPage < totalPages - 2) {
        pages.push('ellipsis')
      }

      // Always show last page
      pages.push(totalPages)
    }

    return pages
  }

  const pageNumbers = getPageNumbers()

  return (
    <div className={cn('flex items-center justify-between gap-4', className)}>
      {/* Left side: Info and page size */}
      <div className="flex items-center gap-4">
        {totalItems !== undefined && (
          <span className="text-sm text-muted-foreground">
            Showing {Math.min((currentPage - 1) * pageSize + 1, totalItems)} to{' '}
            {Math.min(currentPage * pageSize, totalItems)} of {totalItems} results
          </span>
        )}

        {showPageSize && onPageSizeChange && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Rows per page:</span>
            <select
              value={pageSize}
              onChange={(e) => onPageSizeChange(Number(e.target.value))}
              className="h-8 rounded-md border border-input bg-background px-2 text-sm"
            >
              {PAGINATION_CONFIG.PAGE_SIZE_OPTIONS.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Right side: Navigation */}
      <div className="flex items-center gap-1">
        {/* First page */}
        <PaginationButton
          onClick={() => onPageChange(1)}
          disabled={!canPreviousPage}
          aria-label="Go to first page"
        >
          <ChevronsLeft className="h-4 w-4" />
        </PaginationButton>

        {/* Previous page */}
        <PaginationButton
          onClick={() => onPageChange(currentPage - 1)}
          disabled={!canPreviousPage}
          aria-label="Go to previous page"
        >
          <ChevronLeft className="h-4 w-4" />
        </PaginationButton>

        {/* Page numbers */}
        {pageNumbers.map((page, index) => {
          if (page === 'ellipsis') {
            return (
              <span key={`ellipsis-${index}`} className="px-2 text-muted-foreground">
                ...
              </span>
            )
          }

          return (
            <PaginationButton
              key={page}
              onClick={() => onPageChange(page)}
              isActive={page === currentPage}
              aria-label={`Go to page ${page}`}
              aria-current={page === currentPage ? 'page' : undefined}
            >
              {page}
            </PaginationButton>
          )
        })}

        {/* Next page */}
        <PaginationButton
          onClick={() => onPageChange(currentPage + 1)}
          disabled={!canNextPage}
          aria-label="Go to next page"
        >
          <ChevronRight className="h-4 w-4" />
        </PaginationButton>

        {/* Last page */}
        <PaginationButton
          onClick={() => onPageChange(totalPages)}
          disabled={!canNextPage}
          aria-label="Go to last page"
        >
          <ChevronsRight className="h-4 w-4" />
        </PaginationButton>
      </div>
    </div>
  )
}

/**
 * Pagination button component
 */
interface PaginationButtonProps {
  onClick: () => void
  disabled?: boolean
  isActive?: boolean
  children: React.ReactNode
  'aria-label'?: string
  'aria-current'?: 'page' | undefined
}

function PaginationButton({
  onClick,
  disabled = false,
  isActive = false,
  children,
  ...props
}: PaginationButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'flex h-8 min-w-8 items-center justify-center rounded-md px-2 text-sm font-medium',
        'transition-colors',
        isActive
          ? 'bg-primary text-primary-foreground'
          : 'hover:bg-muted',
        disabled && 'cursor-not-allowed opacity-50'
      )}
      {...props}
    >
      {children}
    </button>
  )
}
