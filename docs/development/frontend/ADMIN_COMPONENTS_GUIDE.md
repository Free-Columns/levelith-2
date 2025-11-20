# Admin Dashboard - Custom Components Guide

---
title: "Admin Dashboard Custom Components Guide"
description: "Comprehensive guide to reusable UI components for the admin dashboard, including usage examples, API reference, and best practices."
category: "frontend"
tags: ["admin", "components", "react", "typescript", "ui", "reusable"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 30
relatedPages:
  - "/docs/development/frontend/ADMIN_HOOKS_GUIDE.md"
  - "/docs/development/frontend/ADMIN_API_CLIENT_GUIDE.md"
  - "/docs/development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md"
searchKeywords:
  - "admin components"
  - "react components"
  - "data table"
  - "loading states"
  - "error handling"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Admin Dashboard - Custom Components Guide

> **TL;DR:** Reusable UI components for the admin dashboard built with React, TypeScript, and Tailwind CSS. Includes DataTable, SearchBar, FilterPanel, Pagination, loading states, error boundaries, and confirmation dialogs. All components are fully typed, accessible, and production-ready.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 30 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Overview](#overview)
- [Component Architecture](#component-architecture)
- [Components](#components)
  - [DataTable](#datatable)
  - [SearchBar](#searchbar)
  - [FilterPanel](#filterpanel)
  - [Pagination](#pagination)
  - [LoadingSpinner](#loadingspinner)
  - [LoadingSkeleton](#loadingskeleton)
  - [ErrorBoundary](#errorboundary)
  - [ConfirmDialog](#confirmdialog)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Overview

The admin dashboard uses a set of reusable, production-ready UI components built with modern React patterns. All components are:

- ✅ **Fully Typed** - Complete TypeScript support with generics
- ✅ **Accessible** - ARIA labels, keyboard navigation, screen reader friendly
- ✅ **Responsive** - Mobile-first design with Tailwind CSS
- ✅ **Documented** - JSDoc comments with usage examples
- ✅ **Consistent** - Follow shadcn/ui design patterns
- ✅ **Composable** - Easy to combine and extend

### Location

All custom components are located in:
```
frontend/src/admin/components/custom/
├── DataTable.tsx         # TanStack Table wrapper
├── SearchBar.tsx         # Debounced search input
├── FilterPanel.tsx       # Collapsible filter panel
├── Pagination.tsx        # Full pagination controls
├── LoadingSpinner.tsx    # Loading indicators
├── LoadingSkeleton.tsx   # Skeleton loaders
├── ErrorBoundary.tsx     # React error boundary
├── ConfirmDialog.tsx     # Confirmation dialogs
└── index.ts              # Barrel export
```

### Import Pattern

```typescript
// Import individual components
import { DataTable, SearchBar, Pagination } from '@/admin/components/custom'

// Or import all
import * as CustomComponents from '@/admin/components/custom'
```

---

## Component Architecture

### Design Principles

1. **Composition over Configuration** - Components are composable building blocks
2. **Type Safety** - Leverage TypeScript generics for flexibility
3. **Controlled Components** - Parent manages state, component handles UI
4. **Accessibility First** - ARIA labels, keyboard navigation, semantic HTML
5. **Performance** - Memoization, lazy loading, optimized re-renders

### Dependencies

- **React 18+** - Hooks, concurrent features
- **TypeScript 5+** - Type safety and developer experience
- **TanStack Table 8+** - Headless table library (DataTable only)
- **Lucide React** - Icon library
- **Tailwind CSS 3+** - Utility-first styling
- **clsx + tailwind-merge** - Class name utilities

---

## Components

## Form Components

### FormButton

**Purpose:** Reusable button component with variant styles for forms and modals.

**File:** `frontend/src/admin/components/forms/FormButton.jsx`

#### Features

- ✅ Three variants: `primary`, `secondary`, `danger`
- ✅ ONETRUTH theme integration
- ✅ Disabled state handling
- ✅ Custom styling support
- ✅ Full prop spreading

#### Basic Usage

```jsx
import FormButton from '../components/forms/FormButton'

function MyForm() {
  return (
    <div>
      <FormButton variant="primary" onClick={handleSave}>
        Save Changes
      </FormButton>

      <FormButton variant="secondary" onClick={handleCancel}>
        Cancel
      </FormButton>

      <FormButton variant="danger" onClick={handleDelete}>
        Delete Permanently
      </FormButton>
    </div>
  )
}
```

#### Variants

```jsx
// Primary (default) - Blue background
<FormButton variant="primary" onClick={handleAction}>
  Primary Action
</FormButton>

// Secondary - Gray background with border
<FormButton variant="secondary" onClick={handleAction}>
  Secondary Action
</FormButton>

// Danger - Red background for destructive actions
<FormButton variant="danger" onClick={handleDelete}>
  Delete
</FormButton>
```

#### With Custom Styles

```jsx
<FormButton
  variant="primary"
  onClick={handleSave}
  style={{ backgroundColor: ONETRUTH.colors.success }}
>
  Custom Styled Button
</FormButton>
```

#### Disabled State

```jsx
<FormButton
  variant="primary"
  onClick={handleSave}
  disabled={isLoading}
>
  {isLoading ? 'Saving...' : 'Save'}
</FormButton>
```

#### API Reference

```typescript
interface FormButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  className?: string
  style?: React.CSSProperties
}
```

---

### FormInput

**Purpose:** Reusable input field with label, validation, and error display.

**File:** `frontend/src/admin/components/forms/FormInput.jsx`

#### Features

- ✅ Label with required indicator
- ✅ Error state styling
- ✅ Help text support
- ✅ Disabled state
- ✅ ONETRUTH theme integration
- ✅ All standard input types

#### Basic Usage

```jsx
import FormInput from '../components/forms/FormInput'

function UserForm() {
  const [username, setUsername] = useState('')
  const [error, setError] = useState('')

  return (
    <FormInput
      label="Username"
      name="username"
      value={username}
      onChange={(e) => setUsername(e.target.value)}
      placeholder="Enter username"
      required
      error={error}
      helpText="Username must be unique"
    />
  )
}
```

#### With Validation

```jsx
<FormInput
  label="Email"
  name="email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={emailError}
  required
/>
```

#### API Reference

```typescript
interface FormInputProps {
  label?: string
  name: string
  type?: string
  value: string
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
  placeholder?: string
  required?: boolean
  error?: string
  disabled?: boolean
  helpText?: string
}
```

---

### FormTextarea

**Purpose:** Reusable textarea field with label and validation.

**File:** `frontend/src/admin/components/forms/FormTextarea.jsx`

#### Features

- ✅ Label with required indicator
- ✅ Error state styling
- ✅ Help text support
- ✅ Disabled state
- ✅ Configurable rows
- ✅ ONETRUTH theme integration

#### Basic Usage

```jsx
import FormTextarea from '../components/forms/FormTextarea'

function NoteForm() {
  const [notes, setNotes] = useState('')

  return (
    <FormTextarea
      label="Admin Notes"
      name="adminNotes"
      value={notes}
      onChange={(e) => setNotes(e.target.value)}
      placeholder="Enter notes..."
      rows={4}
      helpText="Internal notes visible only to admins"
    />
  )
}
```

#### With Validation

```jsx
<FormTextarea
  label="Description"
  name="description"
  value={description}
  onChange={(e) => setDescription(e.target.value)}
  error={descriptionError}
  required
  rows={6}
/>
```

#### API Reference

```typescript
interface FormTextareaProps {
  label?: string
  name: string
  value: string
  onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void
  placeholder?: string
  required?: boolean
  error?: string
  disabled?: boolean
  helpText?: string
  rows?: number
}
```

---

## DataTable

**Purpose:** Reusable data table with sorting, selection, and empty states.

**File:** `frontend/src/admin/components/custom/DataTable.tsx`

### Features

- ✅ Generic TypeScript support
- ✅ Sortable columns with visual indicators
- ✅ Row selection with checkboxes
- ✅ Loading skeletons
- ✅ Error states
- ✅ Empty states
- ✅ Custom row styling

### Basic Usage

```tsx
import { DataTable } from '@/admin/components/custom'
import type { ColumnDef } from '@tanstack/react-table'

interface User {
  id: string
  username: string
  email: string
}

const columns: ColumnDef<User>[] = [
  {
    accessorKey: 'username',
    header: 'Username',
  },
  {
    accessorKey: 'email',
    header: 'Email',
  },
]

function UsersTable() {
  return (
    <DataTable
      columns={columns}
      data={users}
      isLoading={isLoading}
      error={error}
      emptyMessage="No users found"
    />
  )
}
```

### With Row Selection

```tsx
const [selectedUsers, setSelectedUsers] = useState<User[]>([])

<DataTable
  columns={columns}
  data={users}
  enableRowSelection
  onRowSelectionChange={setSelectedUsers}
/>

// Access selected rows
console.log(selectedUsers) // Array of selected User objects
```

### With Checkbox Column

```tsx
import { createCheckboxColumn } from '@/admin/components/custom'

const columns: ColumnDef<User>[] = [
  createCheckboxColumn<User>(), // Add checkbox column
  {
    accessorKey: 'username',
    header: 'Username',
  },
  // ... other columns
]
```

### Custom Row Styling

```tsx
<DataTable
  columns={columns}
  data={users}
  rowClassName={(user) =>
    user.isActive ? '' : 'opacity-50 bg-red-50'
  }
/>
```

### API Reference

```typescript
interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  isLoading?: boolean
  error?: string | null
  emptyMessage?: string
  enableRowSelection?: boolean
  onRowSelectionChange?: (selectedRows: TData[]) => void
  enableSorting?: boolean
  className?: string
  rowClassName?: (row: TData) => string
}
```

---

## SearchBar

**Purpose:** Debounced search input with clear button.

**File:** `frontend/src/admin/components/custom/SearchBar.tsx`

### Features

- ✅ Automatic debouncing
- ✅ Clear button
- ✅ Configurable delay
- ✅ Controlled or uncontrolled
- ✅ Loading states

### Basic Usage

```tsx
import { SearchBar } from '@/admin/components/custom'

function UsersList() {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <SearchBar
      placeholder="Search users..."
      onSearch={setSearchQuery}
      debounceDelay={500}
    />
  )
}
```

### Controlled Component

```tsx
const [search, setSearch] = useState('')

<SearchBar
  value={search}
  onSearch={setSearch}
  placeholder="Search..."
/>
```

### Custom Debounce Delay

```tsx
<SearchBar
  placeholder="Search (fast)..."
  onSearch={handleSearch}
  debounceDelay={200} // Fire after 200ms
/>
```

### API Reference

```typescript
interface SearchBarProps {
  value?: string
  onSearch: (value: string) => void
  placeholder?: string
  debounceDelay?: number
  className?: string
  disabled?: boolean
}
```

---

## FilterPanel

**Purpose:** Collapsible filter panel with active filter badges.

**File:** `frontend/src/admin/components/custom/FilterPanel.tsx`

### Features

- ✅ Collapsible panel
- ✅ Active filter count badge
- ✅ Quick filter chips
- ✅ Clear all functionality
- ✅ Flexible content

### Basic Usage

```tsx
import { FilterPanel, FilterItem } from '@/admin/components/custom'
import { useDisclosure } from '@/admin/hooks'

function UsersFilters() {
  const panel = useDisclosure()
  const [status, setStatus] = useState('')
  const [role, setRole] = useState('')

  const activeFilters = [status, role].filter(Boolean).length

  return (
    <FilterPanel
      title="Filters"
      isOpen={panel.isOpen}
      onToggle={panel.toggle}
      onClear={() => {
        setStatus('')
        setRole('')
      }}
      activeFilters={activeFilters}
    >
      <FilterItem label="Status">
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </FilterItem>

      <FilterItem label="Role">
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="">All</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
      </FilterItem>
    </FilterPanel>
  )
}
```

### With Quick Filter Chips

```tsx
import { QuickFilters } from '@/admin/components/custom'

const activeFilters = [
  { key: 'status', label: 'Status', value: 'Active' },
  { key: 'role', label: 'Role', value: 'Admin' },
]

<QuickFilters
  filters={activeFilters}
  onRemove={(key) => handleRemoveFilter(key)}
  onClearAll={handleClearAll}
/>
```

### API Reference

```typescript
interface FilterPanelProps {
  title?: string
  isOpen: boolean
  onToggle: () => void
  children: React.ReactNode
  onClear?: () => void
  activeFilters?: number
  className?: string
}

interface FilterItemProps {
  label: string
  children: React.ReactNode
  className?: string
}

interface QuickFiltersProps {
  filters: Array<{ key: string; label: string; value: string }>
  onRemove: (key: string) => void
  onClearAll: () => void
  className?: string
}
```

---

## Pagination

**Purpose:** Full pagination controls with page size selector.

**File:** `frontend/src/admin/components/custom/Pagination.tsx`

### Features

- ✅ First/Previous/Next/Last navigation
- ✅ Page number buttons with ellipsis
- ✅ Page size selector
- ✅ Item count display
- ✅ Keyboard accessible

### Basic Usage

```tsx
import { Pagination } from '@/admin/components/custom'

function UsersList() {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const totalPages = Math.ceil(totalUsers / pageSize)

  return (
    <Pagination
      currentPage={page}
      totalPages={totalPages}
      onPageChange={setPage}
      pageSize={pageSize}
      onPageSizeChange={setPageSize}
      totalItems={totalUsers}
      showPageSize
    />
  )
}
```

### With usePagination Hook

```tsx
import { usePagination } from '@/admin/hooks'

const pagination = usePagination(totalUsers, 20)

<Pagination
  currentPage={pagination.page}
  totalPages={pagination.totalPages}
  onPageChange={pagination.setPage}
  pageSize={pagination.pageSize}
  onPageSizeChange={pagination.setPageSize}
  totalItems={totalUsers}
  showPageSize
/>
```

### API Reference

```typescript
interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
  pageSize?: number
  onPageSizeChange?: (pageSize: number) => void
  totalItems?: number
  showPageSize?: boolean
  className?: string
}
```

---

## LoadingSpinner

**Purpose:** Animated loading indicators for various contexts.

**File:** `frontend/src/admin/components/custom/LoadingSpinner.tsx`

### Variants

1. **LoadingSpinner** - Default spinner (3 sizes)
2. **LoadingOverlay** - Fullscreen overlay with spinner
3. **LoadingInline** - Inline spinner with text

### Basic Usage

```tsx
import { LoadingSpinner, LoadingOverlay, LoadingInline } from '@/admin/components/custom'

// Default spinner
<LoadingSpinner size="md" label="Loading users..." />

// Fullscreen overlay
{isLoading && <LoadingOverlay label="Loading..." />}

// Inline indicator
<LoadingInline label="Saving..." />
```

### Sizes

```tsx
<LoadingSpinner size="sm" />  // Small (16px)
<LoadingSpinner size="md" />  // Medium (32px) - default
<LoadingSpinner size="lg" />  // Large (48px)
```

### API Reference

```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
  label?: string
}
```

---

## LoadingSkeleton

**Purpose:** Skeleton loaders for different content types.

**File:** `frontend/src/admin/components/custom/LoadingSkeleton.tsx`

### Variants

1. **Skeleton** - Base skeleton block
2. **TableSkeleton** - Table structure
3. **CardSkeleton** - Card structure
4. **FormSkeleton** - Form fields
5. **StatsCardSkeleton** - Stats card

### Usage Examples

```tsx
import { TableSkeleton, CardSkeleton, FormSkeleton } from '@/admin/components/custom'

// Table skeleton
{isLoading && <TableSkeleton rows={5} columns={4} />}

// Card skeleton
{isLoading && (
  <div className="grid grid-cols-3 gap-4">
    <CardSkeleton />
    <CardSkeleton />
    <CardSkeleton />
  </div>
)}

// Form skeleton
{isLoading && <FormSkeleton fields={3} />}

// Custom skeleton
import { Skeleton } from '@/admin/components/custom'

<Skeleton className="h-10 w-[250px]" />
```

### API Reference

```typescript
interface SkeletonProps {
  className?: string
}

function TableSkeleton({ rows?: number; columns?: number }): JSX.Element
function CardSkeleton(): JSX.Element
function FormSkeleton({ fields?: number }): JSX.Element
function StatsCardSkeleton(): JSX.Element
```

---

## ErrorBoundary

**Purpose:** Catch and display React errors gracefully.

**File:** `frontend/src/admin/components/custom/ErrorBoundary.tsx`

### Features

- ✅ Catch rendering errors
- ✅ Custom fallback UI
- ✅ Error details in development
- ✅ Reset functionality
- ✅ Error callback hook

### Basic Usage

```tsx
import { ErrorBoundary } from '@/admin/components/custom'

function App() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  )
}
```

### Custom Fallback

```tsx
<ErrorBoundary
  fallback={(error, reset) => (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )}
  onError={(error, errorInfo) => {
    console.error('Error caught:', error, errorInfo)
    // Send to error tracking service
  }}
>
  <MyComponent />
</ErrorBoundary>
```

### With Hook

```tsx
import { useErrorBoundary } from '@/admin/components/custom'

function MyComponent() {
  const { setError } = useErrorBoundary()

  const handleAction = async () => {
    try {
      await riskyOperation()
    } catch (err) {
      setError(err) // Trigger error boundary
    }
  }

  return <button onClick={handleAction}>Do something risky</button>
}
```

### API Reference

```typescript
interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: (error: Error, reset: () => void) => ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}
```

---

## ConfirmDialog

**Purpose:** Confirmation dialogs with promise-based API.

**File:** `frontend/src/admin/components/custom/ConfirmDialog.tsx`

### Features

- ✅ 3 variants (default, destructive, warning)
- ✅ Promise-based API with hook
- ✅ Loading states
- ✅ Customizable text
- ✅ Accessible modals

### Variants

1. **default** - Blue info icon, primary button
2. **destructive** - Red warning icon, destructive button
3. **warning** - Yellow alert icon, yellow button

### Basic Usage

```tsx
import { ConfirmDialog } from '@/admin/components/custom'

function UserActions() {
  const [showConfirm, setShowConfirm] = useState(false)

  const handleDelete = async () => {
    await deleteUser()
    setShowConfirm(false)
  }

  return (
    <>
      <button onClick={() => setShowConfirm(true)}>Delete</button>

      <ConfirmDialog
        isOpen={showConfirm}
        title="Delete User"
        description="Are you sure you want to delete this user? This action cannot be undone."
        variant="destructive"
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleDelete}
        onCancel={() => setShowConfirm(false)}
      />
    </>
  )
}
```

### With Hook (Recommended)

```tsx
import { useConfirmDialog } from '@/admin/components/custom'

function UserActions() {
  const confirm = useConfirmDialog()

  const handleDelete = async () => {
    const confirmed = await confirm.show({
      title: 'Delete User',
      description: 'Are you sure? This cannot be undone.',
      variant: 'destructive',
      confirmText: 'Delete',
    })

    if (confirmed) {
      await deleteUser()
      toast.success('User deleted')
    }
  }

  return (
    <>
      <button onClick={handleDelete}>Delete</button>
      <confirm.ConfirmDialog />
    </>
  )
}
```

### With Loading State

```tsx
const handleDelete = async () => {
  const confirmed = await confirm.show({
    title: 'Delete User',
    description: 'This will permanently delete the user.',
    variant: 'destructive',
  })

  if (confirmed) {
    setIsLoading(true)
    await deleteUser()
    setIsLoading(false)
  }
}

<ConfirmDialog
  isOpen={showConfirm}
  title="Delete User"
  description="..."
  onConfirm={handleDelete}
  onCancel={() => setShowConfirm(false)}
  isLoading={isLoading}
/>
```

### API Reference

```typescript
interface ConfirmDialogProps {
  isOpen: boolean
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  variant?: 'default' | 'destructive' | 'warning'
  onConfirm: () => void | Promise<void>
  onCancel: () => void
  isLoading?: boolean
}

function useConfirmDialog(): {
  show: (config: Omit<ConfirmDialogProps, 'isOpen' | 'onConfirm' | 'onCancel'>) => Promise<boolean>
  ConfirmDialog: React.ComponentType
}
```

---

## Best Practices

### Component Composition

```tsx
// ✅ GOOD - Compose components
function UsersPage() {
  return (
    <ErrorBoundary>
      <SearchBar onSearch={setSearch} />
      <FilterPanel {...filterProps}>
        {/* Filter controls */}
      </FilterPanel>
      <DataTable {...tableProps} />
      <Pagination {...paginationProps} />
    </ErrorBoundary>
  )
}

// ❌ BAD - Single monolithic component
function UsersPage() {
  return <GiantUserTableComponent />
}
```

### Loading States

```tsx
// ✅ GOOD - Proper loading states
{isLoading ? (
  <TableSkeleton rows={5} columns={4} />
) : (
  <DataTable data={users} columns={columns} />
)}

// ❌ BAD - Generic loading
{isLoading && <div>Loading...</div>}
```

### Error Handling

```tsx
// ✅ GOOD - Wrap in error boundary
<ErrorBoundary>
  <DataTable data={users} columns={columns} />
</ErrorBoundary>

// ❌ BAD - No error handling
<DataTable data={users} columns={columns} />
```

### Accessibility

```tsx
// ✅ GOOD - Proper labels
<SearchBar
  placeholder="Search users"
  onSearch={setSearch}
  aria-label="Search users by name or email"
/>

// ❌ BAD - No accessibility
<input onChange={e => setSearch(e.target.value)} />
```

---

## Common Patterns

### CRUD Table

```tsx
function UsersTable() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const confirm = useConfirmDialog()

  const { data, isLoading } = useUsers({ page, search })

  const handleDelete = async (id: string) => {
    const confirmed = await confirm.show({
      title: 'Delete User',
      description: 'Are you sure?',
      variant: 'destructive',
    })

    if (confirmed) {
      await deleteUser(id)
    }
  }

  return (
    <div>
      <SearchBar onSearch={setSearch} />
      <DataTable
        data={data.users}
        columns={getColumns(handleDelete)}
        isLoading={isLoading}
      />
      <Pagination
        currentPage={page}
        totalPages={data.totalPages}
        onPageChange={setPage}
      />
      <confirm.ConfirmDialog />
    </div>
  )
}
```

### Filtered List

```tsx
function FilteredUsersList() {
  const panel = useDisclosure()
  const [filters, setFilters] = useState({})
  const [search, setSearch] = useState('')

  const activeFilters = Object.values(filters).filter(Boolean).length

  return (
    <div>
      <SearchBar onSearch={setSearch} />
      <FilterPanel
        isOpen={panel.isOpen}
        onToggle={panel.toggle}
        activeFilters={activeFilters}
        onClear={() => setFilters({})}
      >
        {/* Filter controls */}
      </FilterPanel>
      <DataTable data={filteredUsers} columns={columns} />
    </div>
  )
}
```

---

## Troubleshooting

### DataTable Not Sorting

**Issue:** Columns aren't sortable

**Solution:** Ensure `enableSorting` is enabled and columns have `accessorKey`

```tsx
<DataTable
  columns={columns}
  data={data}
  enableSorting={true} // Enable sorting
/>
```

### SearchBar Not Debouncing

**Issue:** Search fires on every keystroke

**Solution:** Check `debounceDelay` prop and ensure `onSearch` callback is memoized

```tsx
const handleSearch = useCallback((value: string) => {
  setSearch(value)
}, [])

<SearchBar onSearch={handleSearch} debounceDelay={500} />
```

### ConfirmDialog Not Showing

**Issue:** Dialog doesn't appear

**Solution:** Ensure you render the dialog component

```tsx
const confirm = useConfirmDialog()

return (
  <>
    <button onClick={handleAction}>Action</button>
    <confirm.ConfirmDialog /> {/* Don't forget this! */}
  </>
)
```

### Skeleton Flashing

**Issue:** Skeleton briefly appears then data loads

**Solution:** Add minimum loading time or use proper suspense

```tsx
const [minLoadingTime, setMinLoadingTime] = useState(true)

useEffect(() => {
  setTimeout(() => setMinLoadingTime(false), 300)
}, [])

{(isLoading || minLoadingTime) && <TableSkeleton />}
```

---

## Related Documentation

- **[Admin Hooks Guide](ADMIN_HOOKS_GUIDE.md)** - Custom React hooks
- **[Admin API Client Guide](ADMIN_API_CLIENT_GUIDE.md)** - API client methods
- **[Admin Dashboard Refactor V2](../admin/ADMIN_DASHBOARD_REFACTOR_V2.md)** - Implementation plan

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Maintained By:** Semour Media Group
