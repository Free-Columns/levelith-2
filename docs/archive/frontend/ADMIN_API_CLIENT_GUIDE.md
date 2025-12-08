# Admin Dashboard - API Client Methods Guide

---
title: "Admin Dashboard API Client Methods Guide"
description: "Comprehensive guide to type-safe API client methods for the admin dashboard, covering Users, Experiences, and NAICS endpoints with usage examples and best practices."
category: "frontend"
tags: ["admin", "api", "client", "typescript", "rest", "axios"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 25
relatedPages:
  - "/docs/development/frontend/ADMIN_COMPONENTS_GUIDE.md"
  - "/docs/development/frontend/ADMIN_HOOKS_GUIDE.md"
  - "/docs/api/API_DOCUMENTATION.md"
  - "/docs/development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md"
searchKeywords:
  - "api client"
  - "rest api"
  - "axios"
  - "typescript"
  - "crud operations"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Admin Dashboard - API Client Methods Guide

> **TL;DR:** Type-safe API client methods for all admin dashboard operations. Covers Users, Experiences (polymorphic), and NAICS endpoints with full TypeScript support, pagination, filtering, and error handling.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Overview](#overview)
- [API Client Architecture](#api-client-architecture)
- [Users API](#users-api)
- [Experiences API](#experiences-api)
- [NAICS API](#naics-api)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)

---

## Overview

The admin dashboard uses a centralized, type-safe API client built on Axios. All API methods are organized by feature and provide full TypeScript support.

### Key Features

- ✅ **Type Safety** - Full TypeScript generics for request/response
- ✅ **Centralized** - Single axios instance with interceptors
- ✅ **Consistent** - Uniform error handling and response format
- ✅ **Pagination** - Built-in pagination support
- ✅ **Filtering** - Type-safe filter parameters
- ✅ **Authentication** - Automatic JWT token handling
- ✅ **Logging** - Request/response logging in development

### Location

```
frontend/src/
├── lib/
│   ├── api.ts          # Base axios client
│   └── queryClient.ts  # React Query config
└── admin/features/
    ├── users/api/users.api.ts
    ├── experiences/api/experiences.api.ts
    └── naics/api/naics.api.ts
```

### Import Pattern

```typescript
// Import specific API modules
import * as UsersAPI from '@/admin/features/users/api/users.api'
import * as ExperiencesAPI from '@/admin/features/experiences/api/experiences.api'
import * as NAICSAPI from '@/admin/features/naics/api/naics.api'

// Or import individual methods
import { getUsers, createUser } from '@/admin/features/users/api/users.api'
```

---

## API Client Architecture

### Base Client Configuration

**File:** `frontend/src/lib/api.ts`

The base client provides:
- Request/response interceptors
- Authentication token injection
- Error handling
- Development logging

```typescript
import { api } from '@/lib/api'

// All methods return typed responses
const users = await api.get<User[]>('/users')
const user = await api.post<User>('/users', data)
```

### Request Interceptors

Automatically adds:
- `Authorization: Bearer <token>` header
- Request logging (development only)

### Response Interceptors

Handles:
- 401 Unauthorized → Redirect to login
- 403 Forbidden → Show error message
- 404 Not Found → Log error
- 500 Server Error → Show error toast

---

## Users API

**File:** `frontend/src/admin/features/users/api/users.api.ts`

### Methods Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `getUsers` | `GET /users` | Fetch paginated user list |
| `getUserById` | `GET /users/:id` | Fetch single user |
| `createUser` | `POST /users` | Create new user |
| `updateUser` | `PATCH /users/:id` | Update existing user |
| `deleteUser` | `DELETE /users/:id` | Delete user |
| `getUserStats` | `GET /users/stats` | Fetch user statistics |
| `bulkDeleteUsers` | `POST /users/bulk-delete` | Delete multiple users |

### Get Users (Paginated)

```typescript
import { getUsers } from '@/admin/features/users/api/users.api'

// Basic usage
const response = await getUsers()
// Returns: PaginatedResponse<User>

// With pagination
const response = await getUsers({
  page: 1,
  pageSize: 20,
})

// With search
const response = await getUsers({
  search: 'john',
  page: 1,
  pageSize: 20,
})

// With filters
const response = await getUsers({
  search: 'admin',
  isActive: true,
  isVerified: true,
  page: 1,
  pageSize: 50,
})

// Response structure
interface PaginatedResponse<User> {
  data: User[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}
```

### Get User By ID

```typescript
import { getUserById } from '@/admin/features/users/api/users.api'

const user = await getUserById('user-uuid-123')

// Returns: User
interface User {
  id: string
  username: string
  email: string
  isActive: boolean
  isVerified: boolean
  createdAt: string
  updatedAt: string
  profile?: UserProfile
}
```

### Create User

```typescript
import { createUser } from '@/admin/features/users/api/users.api'

const newUser = await createUser({
  username: 'johndoe',
  email: 'john@example.com',
  password: 'SecurePass123!',
  isActive: true,
  profile: {
    firstName: 'John',
    lastName: 'Doe',
  },
})

// Returns: User (created user with ID)
```

### Update User

```typescript
import { updateUser } from '@/admin/features/users/api/users.api'

const updatedUser = await updateUser('user-id', {
  username: 'johndoe_updated',
  isActive: false,
})

// Returns: User (updated user)
```

### Delete User

```typescript
import { deleteUser } from '@/admin/features/users/api/users.api'

const result = await deleteUser('user-id')

// Returns: { success: boolean; message: string }
```

### Get User Statistics

```typescript
import { getUserStats } from '@/admin/features/users/api/users.api'

const stats = await getUserStats()

// Returns: UserStats
interface UserStats {
  totalUsers: number
  activeUsers: number
  inactiveUsers: number
  verifiedUsers: number
  recentSignups: number
}
```

### Bulk Delete Users

```typescript
import { bulkDeleteUsers } from '@/admin/features/users/api/users.api'

const result = await bulkDeleteUsers(['id1', 'id2', 'id3'])

// Returns: { success: boolean; deleted: number; failed: number }
```

### With React Query

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import * as UsersAPI from '@/admin/features/users/api/users.api'

// Query
function useUsers(params) {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => UsersAPI.getUsers(params),
  })
}

// Mutation
function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: UsersAPI.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

// Usage
const { data, isLoading } = useUsers({ page: 1, pageSize: 20 })
const createUser = useCreateUser()

await createUser.mutateAsync(userData)
```

---

## Experiences API

**File:** `frontend/src/admin/features/experiences/api/experiences.api.ts`

### Methods Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `getExperiences` | `GET /experiences` | Fetch paginated experience list |
| `getExperienceById` | `GET /experiences/:id` | Fetch single experience |
| `getExperiencesByUser` | `GET /users/:userId/experiences` | Fetch user's experiences |
| `createExperience` | `POST /experiences` | Create new experience (polymorphic) |
| `updateExperience` | `PATCH /experiences/:id` | Update experience (polymorphic) |
| `deleteExperience` | `DELETE /experiences/:id` | Delete experience |
| `getExperienceStats` | `GET /experiences/stats` | Fetch experience statistics |
| `bulkDeleteExperiences` | `POST /experiences/bulk-delete` | Delete multiple experiences |

### Polymorphic Experience Types

Experiences come in 9 variants across 3 categories:

**Education:** Certificate, Degree, Course
**Workplace:** Gig, Part-Time, Full-Time
**Skills:** Soft Skills, Hard Skills, Native Skills

### Get Experiences (Paginated)

```typescript
import { getExperiences } from '@/admin/features/experiences/api/experiences.api'

// All experiences
const response = await getExperiences()

// Filter by category
const response = await getExperiences({
  category: 'Education',
  page: 1,
  pageSize: 20,
})

// Filter by type
const response = await getExperiences({
  category: 'Workplace',
  type: 'Full-Time',
})

// Filter by NAICS code
const response = await getExperiences({
  naicsCode: '541511', // Software development
})

// Filter by user
const response = await getExperiences({
  userId: 'user-id',
})

// Complex filters
const response = await getExperiences({
  search: 'software',
  category: 'Workplace',
  isCurrent: true,
  dateRange: {
    from: '2023-01-01T00:00:00Z',
    to: '2024-01-01T00:00:00Z',
  },
  page: 1,
  pageSize: 50,
})
```

### Create Experience (Polymorphic)

```typescript
import { createExperience } from '@/admin/features/experiences/api/experiences.api'

// Education - Certificate
const cert = await createExperience({
  userId: 'user-id',
  category: 'Education',
  type: 'Certificate',
  title: 'AWS Certified Developer',
  institution: 'Amazon Web Services',
  naicsCode: '541511',
  startDate: '2024-01-01T00:00:00Z',
  endDate: '2024-03-01T00:00:00Z',
  isCurrent: false,
  credentialId: 'AWS-CERT-12345',
  credentialUrl: 'https://aws.amazon.com/verify',
})

// Workplace - Full-Time
const job = await createExperience({
  userId: 'user-id',
  category: 'Workplace',
  type: 'Full-Time',
  title: 'Senior Software Engineer',
  company: 'Tech Corp',
  position: 'Senior Software Engineer',
  naicsCode: '541511',
  startDate: '2020-01-01T00:00:00Z',
  isCurrent: true,
  responsibilities: [
    'Lead development team',
    'Architecture design',
    'Code review',
  ],
  achievements: [
    'Reduced deployment time by 50%',
    'Implemented CI/CD pipeline',
  ],
})

// Skills - Hard Skills
const skill = await createExperience({
  userId: 'user-id',
  category: 'Skills',
  type: 'Hard Skills',
  title: 'Python Programming',
  naicsCode: '541511',
  proficiencyLevel: 'Expert',
  yearsOfExperience: 8,
})
```

### Get Experiences By User

```typescript
import { getExperiencesByUser } from '@/admin/features/experiences/api/experiences.api'

const response = await getExperiencesByUser('user-id', {
  page: 1,
  pageSize: 20,
})

// Returns all experiences for specific user
```

### Get Experience Statistics

```typescript
import { getExperienceStats } from '@/admin/features/experiences/api/experiences.api'

const stats = await getExperienceStats()

// Returns: ExperienceStats
interface ExperienceStats {
  totalExperiences: number
  byCategory: {
    Education: number
    Workplace: number
    Skills: number
  }
  byType: {
    Certificate: number
    Degree: number
    Course: number
    Gig: number
    'Part-Time': number
    'Full-Time': number
    'Soft Skills': number
    'Hard Skills': number
    'Native Skills': number
  }
  recentlyAdded: number
}
```

---

## NAICS API

**File:** `frontend/src/admin/features/naics/api/naics.api.ts`

### Methods Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `getNAICSCodes` | `GET /naics` | Fetch paginated NAICS list |
| `getNAICSById` | `GET /naics/:id` | Fetch single NAICS by ID |
| `getNAICSByCode` | `GET /naics/code/:code` | Fetch single NAICS by code |
| `searchNAICS` | `GET /naics/search` | Search NAICS by title/description |
| `getNAICSHierarchy` | `GET /naics/hierarchy` | Fetch NAICS tree structure |
| `createNAICS` | `POST /naics` | Create new NAICS code (admin) |
| `updateNAICS` | `PATCH /naics/:id` | Update NAICS (tags/notes only) |
| `deleteNAICS` | `DELETE /naics/:id` | Delete NAICS (soft delete) |
| `getNAICSStats` | `GET /naics/stats` | Fetch NAICS statistics |

### Get NAICS Codes (Paginated)

```typescript
import { getNAICSCodes } from '@/admin/features/naics/api/naics.api'

// All codes
const response = await getNAICSCodes()

// Filter by level
const response = await getNAICSCodes({
  level: 6, // 2, 3, 4, or 6 digit codes
  page: 1,
  pageSize: 50,
})

// Filter by custom category
const response = await getNAICSCodes({
  customCategory: 'Technology',
})

// Filter by activity status
const response = await getNAICSCodes({
  isActive: true,
})

// Search with filters
const response = await getNAICSCodes({
  search: 'software',
  level: 6,
  isActive: true,
  page: 1,
  pageSize: 50,
})
```

### Get NAICS By Code

```typescript
import { getNAICSByCode } from '@/admin/features/naics/api/naics.api'

const naics = await getNAICSByCode('541511')

// Returns: NAICS
interface NAICS {
  id: string
  code: string
  title: string
  description?: string
  level: 2 | 3 | 4 | 6
  parentCode?: string
  tags: string[]
  customCategory?: string
  adminNotes?: string
  isActive: boolean
  experienceCount?: number
  createdAt: string
  updatedAt: string
}
```

### Search NAICS

```typescript
import { searchNAICS } from '@/admin/features/naics/api/naics.api'

const results = await searchNAICS('software development', {
  pageSize: 20,
})

// Returns: PaginatedResponse<NAICS>
// Searches in title and description fields
```

### Get NAICS Hierarchy

```typescript
import { getNAICSHierarchy } from '@/admin/features/naics/api/naics.api'

// Get full hierarchy
const tree = await getNAICSHierarchy()

// Get hierarchy from specific root
const tree = await getNAICSHierarchy('54') // Professional Services

// Returns: NAICSNode[]
interface NAICSNode {
  code: string
  title: string
  level: 2 | 3 | 4 | 6
  children?: NAICSNode[]
  experienceCount: number
}
```

### Update NAICS (Admin)

```typescript
import { updateNAICS } from '@/admin/features/naics/api/naics.api'

// Update tags and custom category
const updated = await updateNAICS('naics-id', {
  tags: ['technology', 'software', 'it'],
  customCategory: 'Information Technology',
  adminNotes: 'Updated classification for 2025',
})

// Note: Cannot update code, title, or description (read-only from NAICS database)
```

### Get NAICS Statistics

```typescript
import { getNAICSStats } from '@/admin/features/naics/api/naics.api'

const stats = await getNAICSStats()

// Returns: NAICSStats
interface NAICSStats {
  totalCodes: number
  byLevel: {
    2: number
    3: number
    4: number
    6: number
  }
  topCategories: Array<{
    category: string
    count: number
  }>
  mostUsed: Array<{
    code: string
    title: string
    count: number
  }>
}
```

---

## Error Handling

### API Error Types

```typescript
interface ApiError {
  message: string
  code?: string
  details?: Record<string, any>
}
```

### Try-Catch Pattern

```typescript
import { toast } from 'sonner'

try {
  const user = await createUser(userData)
  toast.success('User created successfully')
} catch (error) {
  if (error.response?.status === 400) {
    toast.error('Invalid user data')
  } else if (error.response?.status === 409) {
    toast.error('User already exists')
  } else {
    toast.error('Failed to create user')
  }
}
```

### With React Query

```typescript
const createUser = useMutation({
  mutationFn: UsersAPI.createUser,
  onSuccess: () => {
    toast.success('User created')
  },
  onError: (error) => {
    toast.error(error.message || 'Failed to create user')
  },
})
```

---

## Best Practices

### Use React Query

```tsx
// ✅ GOOD - React Query handles caching, loading, errors
import { useQuery } from '@tanstack/react-query'

function UsersList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users', { page: 1 }],
    queryFn: () => getUsers({ page: 1 }),
  })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error} />

  return <UserTable users={data.data} />
}

// ❌ BAD - Manual state management
function UsersList() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    getUsers()
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [])

  // ... rest
}
```

### Type Safety

```tsx
// ✅ GOOD - Full type safety
import type { User } from '@/admin/features/users/types/user.types'

const user: User = await getUserById('id')

// ❌ BAD - No type safety
const user: any = await getUserById('id')
```

### Error Boundaries

```tsx
// ✅ GOOD - Wrap in error boundary
<ErrorBoundary>
  <UsersList />
</ErrorBoundary>

// ❌ BAD - No error handling
<UsersList />
```

---

## Common Patterns

### CRUD Operations

```typescript
// List with pagination
const { data } = useQuery({
  queryKey: ['users', { page }],
  queryFn: () => getUsers({ page }),
})

// Create
const create = useMutation({
  mutationFn: createUser,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})

// Update
const update = useMutation({
  mutationFn: ({ id, data }) => updateUser(id, data),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})

// Delete
const remove = useMutation({
  mutationFn: deleteUser,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})
```

### Search with Debounce

```typescript
import { useDebounce } from '@/admin/hooks'

const [search, setSearch] = useState('')
const debouncedSearch = useDebounce(search, 500)

const { data } = useQuery({
  queryKey: ['users', { search: debouncedSearch }],
  queryFn: () => getUsers({ search: debouncedSearch }),
  enabled: debouncedSearch.length > 0,
})
```

---

## Related Documentation

- **[Admin Components Guide](ADMIN_COMPONENTS_GUIDE.md)** - Custom UI components
- **[Admin Hooks Guide](ADMIN_HOOKS_GUIDE.md)** - Custom React hooks
- **[API Documentation](../../api/API_DOCUMENTATION.md)** - Backend API reference
- **[Admin Dashboard Refactor V2](../admin/ADMIN_DASHBOARD_REFACTOR_V2.md)** - Implementation plan

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Maintained By:** Semour Media Group
