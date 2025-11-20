/**
 * DataTable Component - TanStack Table Wrapper
 *
 * @module admin/components/custom/DataTable
 */

import * as React from 'react'
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  type ColumnDef,
  type SortingState,
  type RowSelectionState,
  useReactTable,
} from '@tanstack/react-table'
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { TableSkeleton } from './LoadingSkeleton'

export interface DataTableProps<TData, TValue> {
  /**
   * Table columns definition
   */
  columns: ColumnDef<TData, TValue>[]
  /**
   * Table data
   */
  data: TData[]
  /**
   * Loading state
   */
  isLoading?: boolean
  /**
   * Error message
   */
  error?: string | null
  /**
   * Empty state message
   */
  emptyMessage?: string
  /**
   * Enable row selection
   */
  enableRowSelection?: boolean
  /**
   * Callback when row selection changes
   */
  onRowSelectionChange?: (selectedRows: TData[]) => void
  /**
   * Enable sorting
   */
  enableSorting?: boolean
  /**
   * Additional CSS classes
   */
  className?: string
  /**
   * Custom row className function
   */
  rowClassName?: (row: TData) => string
}

/**
 * Reusable data table component with sorting and selection
 *
 * @example
 * ```tsx
 * const columns: ColumnDef<User>[] = [
 *   {
 *     accessorKey: 'username',
 *     header: 'Username',
 *   },
 *   {
 *     accessorKey: 'email',
 *     header: 'Email',
 *   },
 * ]
 *
 * <DataTable
 *   columns={columns}
 *   data={users}
 *   isLoading={isLoading}
 *   emptyMessage="No users found"
 *   enableRowSelection
 *   onRowSelectionChange={(rows) => setSelectedUsers(rows)}
 * />
 * ```
 */
export function DataTable<TData, TValue>({
  columns,
  data,
  isLoading = false,
  error = null,
  emptyMessage = 'No results found',
  enableRowSelection = false,
  onRowSelectionChange,
  enableSorting = true,
  className,
  rowClassName,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [rowSelection, setRowSelection] = React.useState<RowSelectionState>({})

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      rowSelection,
    },
    onSortingChange: setSorting,
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: enableSorting ? getSortedRowModel() : undefined,
    enableRowSelection,
    enableSorting,
  })

  // Notify parent of selection changes
  React.useEffect(() => {
    if (onRowSelectionChange) {
      const selectedRows = table.getSelectedRowModel().rows.map((row) => row.original)
      onRowSelectionChange(selectedRows)
    }
  }, [rowSelection, onRowSelectionChange, table])

  // Loading state
  if (isLoading) {
    return <TableSkeleton rows={5} columns={columns.length} />
  }

  // Error state
  if (error) {
    return (
      <div className="flex min-h-[400px] items-center justify-center rounded-lg border border-destructive bg-destructive/10 p-8">
        <div className="text-center">
          <p className="text-destructive font-medium mb-2">Error loading data</p>
          <p className="text-sm text-muted-foreground">{error}</p>
        </div>
      </div>
    )
  }

  // Empty state
  if (data.length === 0) {
    return (
      <div className="flex min-h-[400px] items-center justify-center rounded-lg border p-8">
        <div className="text-center text-muted-foreground">
          <p>{emptyMessage}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={cn('rounded-md border', className)}>
      <div className="overflow-x-auto">
        <table className="w-full caption-bottom text-sm">
          <thead className="border-b bg-muted/50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="h-12 px-4 text-left align-middle font-medium text-muted-foreground"
                  >
                    {header.isPlaceholder ? null : (
                      <div
                        className={cn(
                          'flex items-center gap-2',
                          header.column.getCanSort() && 'cursor-pointer select-none'
                        )}
                        onClick={header.column.getToggleSortingHandler()}
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {header.column.getCanSort() && (
                          <SortIcon sorted={header.column.getIsSorted()} />
                        )}
                      </div>
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="[&_tr:last-child]:border-0">
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className={cn(
                  'border-b transition-colors hover:bg-muted/50',
                  row.getIsSelected() && 'bg-muted',
                  rowClassName?.(row.original)
                )}
              >
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="p-4 align-middle">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Selection info */}
      {enableRowSelection && table.getSelectedRowModel().rows.length > 0 && (
        <div className="flex items-center justify-between border-t p-4 bg-muted/30">
          <div className="text-sm text-muted-foreground">
            {table.getSelectedRowModel().rows.length} of {table.getRowModel().rows.length} row(s)
            selected
          </div>
          <button
            onClick={() => table.resetRowSelection()}
            className="text-sm text-primary hover:underline"
          >
            Clear selection
          </button>
        </div>
      )}
    </div>
  )
}

/**
 * Sort icon component
 */
function SortIcon({ sorted }: { sorted: false | 'asc' | 'desc' }) {
  if (sorted === 'asc') {
    return <ArrowUp className="h-4 w-4" />
  }
  if (sorted === 'desc') {
    return <ArrowDown className="h-4 w-4" />
  }
  return <ArrowUpDown className="h-4 w-4 opacity-50" />
}

/**
 * Helper to create a checkbox column for row selection
 */
export function createCheckboxColumn<TData>(): ColumnDef<TData> {
  return {
    id: 'select',
    header: ({ table }) => (
      <input
        type="checkbox"
        checked={table.getIsAllPageRowsSelected()}
        onChange={table.getToggleAllPageRowsSelectedHandler()}
        aria-label="Select all rows"
        className="h-4 w-4 rounded border-input"
      />
    ),
    cell: ({ row }) => (
      <input
        type="checkbox"
        checked={row.getIsSelected()}
        onChange={row.getToggleSelectedHandler()}
        aria-label="Select row"
        className="h-4 w-4 rounded border-input"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  }
}
