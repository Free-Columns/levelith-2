# Admin Dashboard - Custom Hooks Guide

---
title: "Admin Dashboard Custom Hooks Guide"
description: "Comprehensive guide to custom React hooks for the admin dashboard, including state management, optimization, and utility hooks with usage examples."
category: "frontend"
tags: ["admin", "hooks", "react", "typescript", "state-management", "utilities"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 20
relatedPages:
  - "/docs/development/frontend/ADMIN_COMPONENTS_GUIDE.md"
  - "/docs/development/frontend/ADMIN_API_CLIENT_GUIDE.md"
  - "/docs/development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md"
searchKeywords:
  - "react hooks"
  - "custom hooks"
  - "useDebounce"
  - "usePagination"
  - "localStorage"
  - "state management"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Admin Dashboard - Custom Hooks Guide

> **TL;DR:** Custom React hooks for common patterns in the admin dashboard. Includes debouncing, pagination, localStorage, and disclosure state management. All hooks are fully typed, tested, and production-ready.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 20 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Overview](#overview)
- [Hooks](#hooks)
  - [useDebounce](#usedebounce)
  - [usePagination](#usepagination)
  - [useLocalStorage](#uselocalstorage)
  - [useDisclosure](#usedisclosure)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Overview

Custom hooks encapsulate reusable stateful logic for the admin dashboard. They follow React hooks conventions and provide type-safe APIs.

### Location

All custom hooks are located in:
```
frontend/src/admin/hooks/
├── useDebounce.ts       # Debounce values
├── usePagination.ts     # Pagination state
├── useLocalStorage.ts   # LocalStorage with sync
├── useDisclosure.ts     # Open/close state
└── index.ts             # Barrel export
```

### Import Pattern

```typescript
// Import individual hooks
import { useDebounce, usePagination } from '@/admin/hooks'

// Or import all
import * as Hooks from '@/admin/hooks'
```

---

## Hooks

## useDebounce

**Purpose:** Delay updating a value until after a specified time has passed.

**File:** `frontend/src/admin/hooks/useDebounce.ts`

### Problem It Solves

When implementing search functionality, you don't want to fire API requests on every keystroke. Debouncing delays the update until the user stops typing.

### Usage

```typescript
import { useDebounce } from '@/admin/hooks'

function SearchUsers() {
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 500)

  // This effect only runs 500ms after user stops typing
  useEffect(() => {
    fetchUsers(debouncedSearch)
  }, [debouncedSearch])

  return (
    <input
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      placeholder="Search users..."
    />
  )
}
```

### With API Calls

```typescript
function SearchableList() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 300)

  const { data, isLoading } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => searchAPI(debouncedQuery),
    enabled: debouncedQuery.length > 2,
  })

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {isLoading && <LoadingSpinner />}
      {data && <ResultsList results={data} />}
    </div>
  )
}
```

### Customizable Delay

```typescript
// Fast debounce for UI responsiveness
const fastDebounce = useDebounce(value, 150)

// Standard debounce for search
const searchDebounce = useDebounce(query, 500)

// Slow debounce for expensive operations
const slowDebounce = useDebounce(largeData, 1000)
```

### API Reference

```typescript
function useDebounce<T>(
  value: T,
  delay?: number // Default: 500ms
): T
```

**Parameters:**
- `value` - The value to debounce
- `delay` - Delay in milliseconds (default: 500)

**Returns:** Debounced value that updates after delay

**Benefits:**
- ✅ Reduces API calls
- ✅ Improves performance
- ✅ Better UX (no lag while typing)
- ✅ Configurable delay

---

## usePagination

**Purpose:** Manage pagination state with navigation controls.

**File:** `frontend/src/admin/hooks/usePagination.ts`

### Features

- ✅ Page number tracking
- ✅ Page size management
- ✅ Navigation methods (next, previous, first, last)
- ✅ Page number generation for UI
- ✅ Boundary checks
- ✅ Auto-adjust on data change

### Basic Usage

```typescript
import { usePagination } from '@/admin/hooks'

function UsersList() {
  const totalUsers = 100
  const pagination = usePagination(totalUsers, 20)

  return (
    <div>
      <UserTable
        users={users}
        page={pagination.page}
        pageSize={pagination.pageSize}
      />

      <div>
        <button
          onClick={pagination.firstPage}
          disabled={!pagination.canPreviousPage}
        >
          First
        </button>
        <button
          onClick={pagination.previousPage}
          disabled={!pagination.canPreviousPage}
        >
          Previous
        </button>
        <span>
          Page {pagination.page} of {pagination.totalPages}
        </span>
        <button
          onClick={pagination.nextPage}
          disabled={!pagination.canNextPage}
        >
          Next
        </button>
        <button
          onClick={pagination.lastPage}
          disabled={!pagination.canNextPage}
        >
          Last
        </button>
      </div>
    </div>
  )
}
```

### With Page Size Selector

```typescript
const pagination = usePagination(totalItems, 20)

<select
  value={pagination.pageSize}
  onChange={(e) => pagination.setPageSize(Number(e.target.value))}
>
  <option value={10}>10 per page</option>
  <option value={20}>20 per page</option>
  <option value={50}>50 per page</option>
  <option value={100}>100 per page</option>
</select>
```

### With Page Number Buttons

```typescript
const pagination = usePagination(totalItems, 20)

{pagination.getPageNumbers().map((pageNum) => (
  <button
    key={pageNum}
    onClick={() => pagination.setPage(pageNum)}
    className={pageNum === pagination.page ? 'active' : ''}
  >
    {pageNum}
  </button>
))}
```

### With Pagination Component

```typescript
import { Pagination } from '@/admin/components/custom'

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
interface UsePaginationReturn {
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

function usePagination(
  totalItems: number,
  initialPageSize?: number // Default: 20
): UsePaginationReturn
```

**Benefits:**
- ✅ Complete pagination logic
- ✅ Type-safe API
- ✅ Boundary checks
- ✅ Auto-reset on page size change
- ✅ Smart page number generation

---

## useLocalStorage

**Purpose:** Store and sync state with localStorage.

**File:** `frontend/src/admin/hooks/useLocalStorage.ts`

### Features

- ✅ Type-safe localStorage
- ✅ Cross-tab synchronization
- ✅ SSR-safe (checks for window)
- ✅ JSON serialization
- ✅ Error handling
- ✅ Remove functionality

### Basic Usage

```typescript
import { useLocalStorage } from '@/admin/hooks'

function ThemeToggle() {
  const [theme, setTheme, removeTheme] = useLocalStorage<'light' | 'dark'>(
    'theme',
    'light'
  )

  return (
    <div>
      <p>Current theme: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
      <button onClick={removeTheme}>
        Reset to Default
      </button>
    </div>
  )
}
```

### With Complex Objects

```typescript
interface UserPreferences {
  language: string
  notifications: boolean
  pageSize: number
}

function UserSettings() {
  const [preferences, setPreferences] = useLocalStorage<UserPreferences>(
    'userPreferences',
    {
      language: 'en',
      notifications: true,
      pageSize: 20,
    }
  )

  const updateLanguage = (language: string) => {
    setPreferences({
      ...preferences,
      language,
    })
  }

  return <SettingsForm preferences={preferences} onUpdate={setPreferences} />
}
```

### With Function Updates

```typescript
const [count, setCount] = useLocalStorage('count', 0)

// Functional update (like useState)
<button onClick={() => setCount((prev) => prev + 1)}>
  Increment
</button>
```

### Cross-Tab Sync

```typescript
// Tab 1
const [data, setData] = useLocalStorage('sharedData', { value: 0 })

// Tab 2 (automatically updates when Tab 1 changes)
const [data, setData] = useLocalStorage('sharedData', { value: 0 })
```

### API Reference

```typescript
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [
  T,                                    // Current value
  (value: T | ((prev: T) => T)) => void, // Setter (like useState)
  () => void                            // Remove value
]
```

**Parameters:**
- `key` - localStorage key name
- `initialValue` - Default value if key doesn't exist

**Returns:** Tuple of `[value, setValue, removeValue]`

**Benefits:**
- ✅ Persistent state across sessions
- ✅ Type safety with generics
- ✅ Cross-tab synchronization
- ✅ SSR-safe
- ✅ Error handling

---

## useDisclosure

**Purpose:** Manage open/close state for UI elements.

**File:** `frontend/src/admin/hooks/useDisclosure.ts`

### Problem It Solves

Managing boolean state for modals, dropdowns, sidebars, etc. requires repetitive open/close/toggle logic. This hook provides a clean API.

### Basic Usage

```typescript
import { useDisclosure } from '@/admin/hooks'

function UserDialog() {
  const dialog = useDisclosure()

  return (
    <div>
      <button onClick={dialog.open}>Open Dialog</button>

      {dialog.isOpen && (
        <Dialog onClose={dialog.close}>
          <DialogContent>Hello!</DialogContent>
        </Dialog>
      )}
    </div>
  )
}
```

### With Modal

```typescript
function EditUserModal({ user }: { user: User }) {
  const modal = useDisclosure()

  return (
    <>
      <button onClick={modal.open}>Edit User</button>

      <Modal isOpen={modal.isOpen} onClose={modal.close}>
        <form onSubmit={handleSubmit}>
          <input defaultValue={user.name} />
          <button type="submit">Save</button>
          <button type="button" onClick={modal.close}>
            Cancel
          </button>
        </form>
      </Modal>
    </>
  )
}
```

### With Dropdown

```typescript
function UserMenu() {
  const dropdown = useDisclosure()

  return (
    <div>
      <button onClick={dropdown.toggle}>
        Menu
      </button>

      {dropdown.isOpen && (
        <div className="dropdown">
          <button onClick={() => { handleAction(); dropdown.close() }}>
            Action 1
          </button>
          <button onClick={() => { handleAction(); dropdown.close() }}>
            Action 2
          </button>
        </div>
      )}
    </div>
  )
}
```

### With Filter Panel

```typescript
import { FilterPanel } from '@/admin/components/custom'

function Filters() {
  const panel = useDisclosure()

  return (
    <FilterPanel
      isOpen={panel.isOpen}
      onToggle={panel.toggle}
      onClear={() => {
        resetFilters()
        panel.close()
      }}
    >
      {/* Filter controls */}
    </FilterPanel>
  )
}
```

### Initial State

```typescript
// Start opened
const panel = useDisclosure(true)

// Start closed (default)
const modal = useDisclosure()
```

### API Reference

```typescript
interface UseDisclosureReturn {
  isOpen: boolean
  open: () => void
  close: () => void
  toggle: () => void
}

function useDisclosure(
  initialState?: boolean // Default: false
): UseDisclosureReturn
```

**Returns:**
- `isOpen` - Current state
- `open` - Set to true
- `close` - Set to false
- `toggle` - Toggle state

**Benefits:**
- ✅ Clean API
- ✅ Memoized functions
- ✅ Consistent naming
- ✅ Reusable pattern

---

## Best Practices

### Debouncing Search

```tsx
// ✅ GOOD - Debounce search input
const [search, setSearch] = useState('')
const debouncedSearch = useDebounce(search, 500)

useEffect(() => {
  if (debouncedSearch) {
    fetchResults(debouncedSearch)
  }
}, [debouncedSearch])

// ❌ BAD - No debouncing (fires on every keystroke)
const [search, setSearch] = useState('')

useEffect(() => {
  fetchResults(search)
}, [search])
```

### Pagination State

```tsx
// ✅ GOOD - Use pagination hook
const pagination = usePagination(totalItems, 20)

// ❌ BAD - Manual pagination logic
const [page, setPage] = useState(1)
const [pageSize, setPageSize] = useState(20)
const totalPages = Math.ceil(totalItems / pageSize)
const canNext = page < totalPages
// ... more logic
```

### LocalStorage Persistence

```tsx
// ✅ GOOD - Persist user preferences
const [settings, setSettings] = useLocalStorage('userSettings', defaults)

// ❌ BAD - Lost on refresh
const [settings, setSettings] = useState(defaults)
```

### Modal State

```tsx
// ✅ GOOD - Clean modal state
const modal = useDisclosure()

<button onClick={modal.open}>Open</button>
<Modal isOpen={modal.isOpen} onClose={modal.close} />

// ❌ BAD - Verbose manual state
const [isOpen, setIsOpen] = useState(false)

<button onClick={() => setIsOpen(true)}>Open</button>
<Modal isOpen={isOpen} onClose={() => setIsOpen(false)} />
```

---

## Common Patterns

### Debounced Search with Pagination

```typescript
function SearchableTable() {
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 500)
  const pagination = usePagination(totalItems, 20)

  const { data, isLoading } = useQuery({
    queryKey: ['items', debouncedSearch, pagination.page, pagination.pageSize],
    queryFn: () => fetchItems({
      search: debouncedSearch,
      page: pagination.page,
      pageSize: pagination.pageSize,
    }),
  })

  return (
    <div>
      <SearchBar value={search} onSearch={setSearch} />
      <DataTable data={data.items} columns={columns} isLoading={isLoading} />
      <Pagination {...pagination} totalItems={data.total} />
    </div>
  )
}
```

### Persisted Filter State

```typescript
function FilteredList() {
  const [filters, setFilters] = useLocalStorage('listFilters', {
    status: '',
    category: '',
  })
  const panel = useDisclosure()

  return (
    <div>
      <FilterPanel
        isOpen={panel.isOpen}
        onToggle={panel.toggle}
        onClear={() => setFilters({ status: '', category: '' })}
      >
        <FilterSelect
          value={filters.status}
          onChange={(status) => setFilters({ ...filters, status })}
        />
        <FilterSelect
          value={filters.category}
          onChange={(category) => setFilters({ ...filters, category })}
        />
      </FilterPanel>
      <DataTable data={filteredData} columns={columns} />
    </div>
  )
}
```

### Multi-Step Form with Persistence

```typescript
interface FormData {
  step1: { name: string }
  step2: { email: string }
  step3: { preferences: any }
}

function MultiStepForm() {
  const [formData, setFormData] = useLocalStorage<FormData>('formDraft', {
    step1: { name: '' },
    step2: { email: '' },
    step3: { preferences: {} },
  })
  const [currentStep, setCurrentStep] = useState(1)

  const updateStep = (step: keyof FormData, data: any) => {
    setFormData({
      ...formData,
      [step]: data,
    })
  }

  return (
    <div>
      {currentStep === 1 && <Step1 data={formData.step1} onNext={updateStep} />}
      {currentStep === 2 && <Step2 data={formData.step2} onNext={updateStep} />}
      {currentStep === 3 && <Step3 data={formData.step3} onSubmit={handleSubmit} />}
    </div>
  )
}
```

---

## Troubleshooting

### useDebounce Not Working

**Issue:** Value updates immediately instead of debouncing

**Solution:** Check that you're using the debounced value, not the original

```tsx
// ❌ WRONG - Using original value
const debounced = useDebounce(search, 500)
fetchResults(search) // Should use 'debounced' instead

// ✅ CORRECT
const debounced = useDebounce(search, 500)
fetchResults(debounced)
```

### usePagination Out of Bounds

**Issue:** Page number exceeds total pages

**Solution:** Hook auto-adjusts, but ensure totalItems is correct

```tsx
const pagination = usePagination(data?.total ?? 0, 20)
// Will auto-reset to last valid page if totalItems changes
```

### useLocalStorage Not Syncing

**Issue:** Changes in one tab don't reflect in another

**Solution:** Ensure both tabs use the same key

```tsx
// Tab 1
const [data, setData] = useLocalStorage('myKey', {})

// Tab 2 - Must use SAME key
const [data, setData] = useLocalStorage('myKey', {})
```

### useDisclosure State Not Resetting

**Issue:** Modal stays open after navigation

**Solution:** Reset state in useEffect cleanup

```tsx
const modal = useDisclosure()

useEffect(() => {
  return () => modal.close() // Cleanup on unmount
}, [])
```

---

## Related Documentation

- **[Admin Components Guide](ADMIN_COMPONENTS_GUIDE.md)** - Custom UI components
- **[Admin API Client Guide](ADMIN_API_CLIENT_GUIDE.md)** - API client methods
- **[Admin Dashboard Refactor V2](../admin/ADMIN_DASHBOARD_REFACTOR_V2.md)** - Implementation plan

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Maintained By:** Semour Media Group
