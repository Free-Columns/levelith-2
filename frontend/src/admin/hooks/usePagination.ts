/**
 * Hook for managing pagination state
 *
 * @module admin/hooks/usePagination
 */

import { useState, useMemo } from 'react'
import { PAGINATION_CONFIG } from '@/admin/lib/constants'

/**
 * Pagination state and controls
 */
export interface UsePaginationReturn {
  page: number
  pageSize: number
  totalPages: number
  canPreviousPage: boolean
  canNextPage: boolean
  setPage: (page: number) => void
  setPageSize: (pageSize: number) => void
  nextPage: () => void
  previousPage: () => void
  firstPage: () => void
  lastPage: () => void
  getPageNumbers: () => number[]
}

/**
 * Manage pagination state and provide navigation controls
 *
 * @param totalItems - Total number of items
 * @param initialPageSize - Initial page size (default: 20)
 * @returns Pagination state and controls
 *
 * @example
 * ```tsx
 * const pagination = usePagination(totalUsers, 20)
 *
 * return (
 *   <>
 *     <Table data={users} />
 *     <div>
 *       <button onClick={pagination.previousPage} disabled={!pagination.canPreviousPage}>
 *         Previous
 *       </button>
 *       <span>Page {pagination.page} of {pagination.totalPages}</span>
 *       <button onClick={pagination.nextPage} disabled={!pagination.canNextPage}>
 *         Next
 *       </button>
 *     </div>
 *   </>
 * )
 * ```
 */
export function usePagination(
  totalItems: number,
  initialPageSize = PAGINATION_CONFIG.DEFAULT_PAGE_SIZE
): UsePaginationReturn {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(initialPageSize)

  // Calculate total pages
  const totalPages = useMemo(() => {
    return Math.ceil(totalItems / pageSize) || 1
  }, [totalItems, pageSize])

  // Navigation flags
  const canPreviousPage = page > 1
  const canNextPage = page < totalPages

  // Navigation functions
  const nextPage = () => {
    if (canNextPage) {
      setPage((prev) => prev + 1)
    }
  }

  const previousPage = () => {
    if (canPreviousPage) {
      setPage((prev) => prev - 1)
    }
  }

  const firstPage = () => {
    setPage(1)
  }

  const lastPage = () => {
    setPage(totalPages)
  }

  // Update page size and reset to first page
  const handleSetPageSize = (newPageSize: number) => {
    setPageSize(newPageSize)
    setPage(1)
  }

  // Ensure current page doesn't exceed total pages
  useMemo(() => {
    if (page > totalPages && totalPages > 0) {
      setPage(totalPages)
    }
  }, [page, totalPages])

  // Generate array of page numbers for pagination UI
  const getPageNumbers = (): number[] => {
    const pages: number[] = []
    const maxVisible = 5
    const halfVisible = Math.floor(maxVisible / 2)

    let startPage = Math.max(1, page - halfVisible)
    let endPage = Math.min(totalPages, page + halfVisible)

    // Adjust if near start
    if (page <= halfVisible) {
      endPage = Math.min(maxVisible, totalPages)
    }

    // Adjust if near end
    if (page > totalPages - halfVisible) {
      startPage = Math.max(1, totalPages - maxVisible + 1)
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }

    return pages
  }

  return {
    page,
    pageSize,
    totalPages,
    canPreviousPage,
    canNextPage,
    setPage,
    setPageSize: handleSetPageSize,
    nextPage,
    previousPage,
    firstPage,
    lastPage,
    getPageNumbers,
  }
}
