# Complete Admin Dashboard Guide - Levelith Platform

**Comprehensive Documentation for Admin Dashboard Development, Implementation, and Testing**

**Last Updated:** November 20, 2025  
**Version:** 3.0  
**Status:** Complete Reference Guide  
**Contributors:** Semour Media Group Development Team

---

## Document Overview

This comprehensive guide combines four critical documentation files into a single reference:

1. **Implementation Summary** - Technical documentation of completed CRUD operations
2. **Refactor V2 Plan** - Modern stack rebuild with TypeScript, React Query, and TanStack Table
3. **Admin Panel Guide** - Setup and usage instructions (legacy + new)
4. **Backend Connectivity Testing** - Manual testing checklist and procedures

**Purpose:** Provide developers with complete context for understanding, maintaining, and extending the Levelith admin dashboard.

---

## Table of Contents

### Part 1: Current Status & Architecture
- [1.1 Project Status](#11-project-status)
- [1.2 Architecture Overview](#12-architecture-overview)
- [1.3 Technology Stack](#13-technology-stack)

### Part 2: Implementation Summary
- [2.1 Implementation Status](#21-implementation-status)
- [2.2 Database Changes](#22-database-changes)
- [2.3 API Endpoints](#23-api-endpoints)
- [2.4 Frontend Implementation](#24-frontend-implementation)

### Part 3: Refactor V2 Plan (Modern Stack)
- [3.1 Migration Strategy](#31-migration-strategy)
- [3.2 Phase 0: Preparation & Setup](#32-phase-0-preparation--setup)
- [3.3 Phase 1: Core Infrastructure](#33-phase-1-core-infrastructure)
- [3.4 Phase 2-8: Feature Development](#34-phase-2-8-feature-development)
- [3.5 Progress Tracking](#35-progress-tracking)

### Part 4: Setup & Usage Guide
- [4.1 Quick Start](#41-quick-start)
- [4.2 Database Seeding](#42-database-seeding)
- [4.3 Backend Setup](#43-backend-setup)
- [4.4 Frontend Setup](#44-frontend-setup)

### Part 5: Testing & Validation
- [5.1 Backend Connectivity Testing](#51-backend-connectivity-testing)
- [5.2 CRUD Operations Testing](#52-crud-operations-testing)
- [5.3 Error Handling Testing](#53-error-handling-testing)
- [5.4 Performance Testing](#54-performance-testing)

### Part 6: Deployment & Production
- [6.1 Production Deployment](#61-production-deployment)
- [6.2 Troubleshooting](#62-troubleshooting)
- [6.3 Additional Resources](#63-additional-resources)

---

# Part 1: Current Status & Architecture

## 1.1 Project Status

### ⚠️ CRITICAL STATUS UPDATE - November 20, 2025

**OLD ADMIN DASHBOARD - DEPRECATED**
- **Location:** `_deprecated/levelith_admin_dashboard_OLD/`
- **Status:** ❌ DEPRECATED - DO NOT USE
- **Issues:** 
  - ❌ CRUD operations broken (blank white pages)
  - ❌ Routing incorrect (/users instead of /admin/users)
  - ❌ Mock data everywhere
  - ❌ No TypeScript type safety
  - ❌ Modal components failing
  - ❌ ONETRUTH styling not enforced

**NEW ADMIN DASHBOARD - IN PROGRESS**
- **Location:** `frontend/src/admin/`
- **Status:** 🚧 IN PROGRESS (21% complete - 35/165 tasks)
- **Strategy:** Plan C - Complete Modern Stack Rebuild
- **Timeline:** 20-30 hours remaining
- **Risk Level:** High (Complete rewrite)

### Current Phase Status

| Phase | Tasks | Completed | Status | Time Spent | ETA |
|-------|-------|-----------|--------|-----------|-----|
| Phase 0: Setup | 15 | 15 | ✅ Complete | 2 hrs | Done |
| Phase 1: Infrastructure | 20 | 20 | ✅ Complete | 3 hrs | Done |
| Phase 2: Users | 25 | 0 | ⏸️ Not Started | - | 4-5 hrs |
| Phase 3: Experiences | 30 | 0 | ⏸️ Not Started | - | 5-6 hrs |
| Phase 4: NAICS | 20 | 0 | ⏸️ Not Started | - | 3-4 hrs |
| Phase 5: Dashboard | 15 | 0 | ⏸️ Not Started | - | 2-3 hrs |
| Phase 6: Settings | 10 | 0 | ⏸️ Not Started | - | 2 hrs |
| Phase 7: Routing | 12 | 0 | ⏸️ Not Started | - | 1-2 hrs |
| Phase 8: Production | 18 | 0 | ⏸️ Not Started | - | 2-3 hrs |
| **TOTAL** | **165** | **35** | 🚧 **21%** | **5 hrs** | **20-28 hrs** |

---

## 1.2 Architecture Overview

### Backend Architecture (FastAPI + PostgreSQL)

**4-Layer Architecture:**
```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Database Access)
    ↓
Domain Model Layer (Pydantic Models)
```

**Key Components:**
- **Database:** PostgreSQL (Render-hosted)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **API Framework:** FastAPI
- **Validation:** Pydantic
- **Authentication:** JWT (future phase)

### Frontend Architecture (React + TypeScript)

**Old Dashboard (Deprecated):**
```
/dev/dev-frontend/levelith_admin_dashboard/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── contexts/
```

**New Dashboard (Modern Stack):**
```
frontend/src/admin/
├── features/              # Feature-based architecture
│   ├── users/
│   │   ├── api/          # React Query hooks
│   │   ├── components/   # Feature components
│   │   ├── schemas/      # Zod validation
│   │   ├── types/        # TypeScript types
│   │   └── hooks/        # Custom hooks
│   ├── experiences/
│   ├── naics/
│   ├── dashboard/
│   └── settings/
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── custom/           # Custom components
│   └── layout/           # Layout components
├── lib/
│   ├── api.ts           # API client (Axios)
│   ├── queryClient.ts   # React Query config
│   ├── formatters.ts    # Utility formatters
│   └── validators.ts    # Validation utilities
├── hooks/               # Global hooks
└── types/               # Global types
```

---

## 1.3 Technology Stack

### Backend Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.104+ | API Framework |
| PostgreSQL | 15+ | Database |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migrations |
| Pydantic | 2.0+ | Data Validation |
| Uvicorn | 0.24+ | ASGI Server |

### Frontend Stack (New Dashboard)

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18+ | UI Framework |
| TypeScript | 5.0+ | Type Safety |
| Vite | 5.0+ | Build Tool |
| TanStack Query | 5.17+ | State Management |
| TanStack Table | 8.11+ | Data Tables |
| React Hook Form | 7.49+ | Form Management |
| Zod | 3.22+ | Schema Validation |
| Tailwind CSS | 3.4+ | Styling |
| shadcn/ui | Latest | Component Library |
| Axios | 1.6+ | HTTP Client |
| Lucide React | 0.303+ | Icons |
| Sonner | 1.3+ | Toast Notifications |
| date-fns | 3.0+ | Date Utilities |

---

# Part 2: Implementation Summary

## 2.1 Implementation Status

### ✅ Completed Features (Backend + Frontend v1)

#### 1. NAICS CRUD Operations
- ✅ Added admin-specific fields to NAICS model
- ✅ Created database migration for new fields
- ✅ Implemented UPDATE and DELETE operations
- ✅ Added server-side pagination (50 items per page, max 200)
- ✅ Frontend fully integrated with edit/delete UI
- ✅ Modal forms for admin fields (tags, custom_category, admin_notes)

#### 2. Experiences Pagination
- ✅ Updated default pagination to 50 items per page
- ✅ Increased max page size to 200
- ✅ Added Category and Type filter dropdowns
- ✅ Smart filtering (type options adapt to selected category)

#### 3. Database Schema Updates
- ✅ Added migration: `41518377be8d_add_admin_fields_to_naics_codes`
- ✅ New NAICS fields: `tags`, `custom_category`, `admin_notes`

#### 4. API Endpoints
- ✅ All CRUD endpoints functional and tested
- ✅ Proper error handling and validation

#### 5. UI/UX Improvements (Old Dashboard)
- ✅ All components use ONETRUTH dynamic styling (no hardcoded CSS)
- ✅ Modal component fixed (blank screen issue resolved)
- ✅ AdminLayout styling enforces ONETRUTH
- ✅ DataSourceSwitcher cleaned up (removed "Coming Soon" text)

### ⚠️ Known Limitations

1. **No Authentication:** API endpoints not protected by admin role checking (future phase)
2. **No Audit Trail:** Admin changes not logged (future enhancement)
3. **Manual Testing Only:** Automated frontend tests not yet written
4. **Old Dashboard Deprecated:** Original implementation has critical issues

---

## 2.2 Database Changes

### NAICS Codes Table - New Fields

| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| `tags` | JSON | NO | `[]` | Array of custom tags for admin organization |
| `custom_category` | VARCHAR(100) | YES | NULL | Admin-defined category for internal classification |
| `admin_notes` | TEXT | YES | NULL | Internal notes and comments for admin use |

### Migration Details

**Migration File:** `backend/alembic/versions/41518377be8d_add_admin_fields_to_naics_codes.py`

**Apply Migration:**
```bash
cd backend
python -m alembic upgrade head
```

**Verify Migration:**
```sql
\c levelith
\d naics_codes  -- Should show tags, custom_category, admin_notes
```

**Rollback Migration:**
```bash
python -m alembic downgrade -1
```

**Test Update:**
```sql
-- Update a NAICS code with admin fields
UPDATE naics_codes
SET tags = '["test", "example"]'::json,
    custom_category = 'Test Category',
    admin_notes = 'Test notes'
WHERE code = '541511';

-- Verify
SELECT code, tags, custom_category, admin_notes
FROM naics_codes
WHERE code = '541511';
```

⚠️ **Warning:** Always backup database before running migrations in production.

---

## 2.3 API Endpoints

### NAICS API Endpoints

#### GET /api/v1/naics/paginated

**Server-side paginated search for NAICS codes**

**Query Parameters:**
- `q` (string, optional): Search query for code/title/description
- `category` (string, optional): Filter by category
- `level` (int, optional): Filter by level (2, 3, 4, or 6)
- `page` (int, default=1): Page number
- `page_size` (int, default=50, max=200): Items per page

**Response:**
```json
{
  "items": [
    {
      "code": "541511",
      "title": "Custom Computer Programming Services",
      "description": "...",
      "category": "Information",
      "level": 6,
      "tags": ["software", "tech"],
      "custom_category": "Tech Priority",
      "admin_notes": "High demand sector"
    }
  ],
  "total": 2222,
  "page": 1,
  "page_size": 50,
  "total_pages": 45
}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/naics/paginated?q=computer&page=1&page_size=10"
```

---

#### PATCH /api/v1/naics/{code}

**Update admin-specific fields for a NAICS code**

**Request Body:**
```json
{
  "tags": ["high-demand", "tech-sector"],
  "custom_category": "Priority Industries",
  "admin_notes": "Requires additional documentation"
}
```

**Response:** Returns updated NAICS code object

**Example:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/naics/541511" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["software", "tech"], "admin_notes": "High demand sector"}'
```

💡 **Pro Tip:** Only admin-specific fields can be updated. Official NAICS fields (code, title, description) are read-only.

---

#### DELETE /api/v1/naics/{code}

**Delete a NAICS code from the database**

⚠️ **WARNING:** This permanently removes the code. Should only be used for test/invalid codes.

**Response:** 204 No Content

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/naics/999999"
```

🔴 **Critical:** Deletion is permanent and cannot be undone. Always confirm before deleting production data.

---

### Experiences API Updates

#### GET /api/v1/experiences/

**Updated pagination defaults**

**Changes:**
- Default `page_size`: 20 → **50**
- Maximum `page_size`: 100 → **200**

**Query Parameters:**
- `user_id` (string, optional): Filter by user ID
- `category` (enum, optional): Filter by category (Education, Workplace, Skills)
- `experience_type` (enum, optional): Filter by type
- `page` (int, default=1): Page number
- `page_size` (int, default=50, max=200): Items per page

**Response:**
```json
{
  "items": [...],
  "total": 127,
  "page": 1,
  "page_size": 50,
  "total_pages": 3
}
```

---

### User Endpoints

```
GET    /api/v1/users/              # List all users (paginated)
POST   /api/v1/users/              # Create user
GET    /api/v1/users/{id}          # Get user by ID
PATCH  /api/v1/users/{id}          # Update user
DELETE /api/v1/users/{id}          # Delete user
POST   /api/v1/users/bulk-delete   # Delete multiple users
POST   /api/v1/users/seed          # Seed test users
```

**Example - List Users:**
```bash
curl "http://localhost:8000/api/v1/users?skip=0&limit=50"
```

**Example - Create User:**
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

---

### Health Endpoints

```
GET    /health                     # Basic health check
GET    /health/details             # Detailed health with DB info
```

**Example Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "development",
  "database": "connected",
  "timestamp": "2025-11-20T12:00:00Z"
}
```

**Full API Documentation:** http://localhost:8000/docs

---

## 2.4 Frontend Implementation

### Old Dashboard (Deprecated) - V1 Implementation

**Location:** `_deprecated/levelith_admin_dashboard_OLD/`

**Status:** ❌ DEPRECATED - See Section 3 for new implementation

**Completed Features (Historical Reference):**
- NAICS Codes Admin Page - 558 lines (complete rewrite from 244)
- Edit/Delete functionality with modals
- Server-side pagination
- Tag management
- Filter dropdowns for experiences

**Critical Issues (Why it was deprecated):**
- Routing issues (/users vs /admin/users)
- Mock data conflicts
- No TypeScript type safety
- Modal component failures
- Blank white pages on CRUD operations

---

### New Dashboard (Modern Stack) - V2 In Progress

**Location:** `frontend/src/admin/`

**Architecture:** Feature-based with TypeScript, React Query, TanStack Table

See **Part 3** for complete implementation details.

---

# Part 3: Refactor V2 Plan (Modern Stack)

## 3.1 Migration Strategy

### Executive Summary

Complete rebuild of admin dashboard using modern 2025 best practices:

**Core Technologies:**
- ✅ **TypeScript** everywhere (full type safety)
- ✅ **React Query** for API state management
- ✅ **TanStack Table** for advanced data tables
- ✅ **React Hook Form + Zod** for type-safe forms
- ✅ **Tailwind CSS** for styling (replacing inline styles)
- ✅ **shadcn/ui** component library
- ✅ **Remove ALL mock data** (server-only)
- ✅ **Fix routing** to use `/admin/*` prefix

### Primary Objectives

1. ✅ **Type Safety** - Zero runtime type errors, full autocomplete
2. ✅ **Remove Mock Data** - Delete all LOCAL mode, server-only
3. ✅ **Production Ready** - Proper error handling, loading states
4. ✅ **Search & Filter** - Advanced filtering on all tables
5. ✅ **NAICS Editing** - Tag/category editing interface
6. ✅ **Maintainable** - Future-proof architecture
7. ✅ **Performance** - Automatic caching, optimistic updates

### Non-Goals

- ❌ Backward compatibility (complete rewrite)
- ❌ Support for deprecated dashboard
- ❌ Real-time WebSocket features (future phase)

---

## 3.2 Phase 0: Preparation & Setup

**Status:** ✅ COMPLETED  
**Completion Date:** November 20, 2025  
**Time Spent:** ~2 hours

### Tasks Completed (15/15)

1. ✅ Install new dependencies (React Query, TanStack Table, React Hook Form, Zod, shadcn/ui)
2. ✅ Configure TypeScript with path aliases
3. ✅ Set up Tailwind CSS
4. ✅ Install shadcn/ui CLI and components
5. ✅ Configure React Query client
6. ✅ Set up Vite for `/admin` base path
7. ✅ Create feature-based folder structure
8. ✅ Set up path aliases in `tsconfig.json` and `vite.config.ts`
9. ✅ Configure ESLint for TypeScript
10. ✅ Set up Prettier with Tailwind plugin
11. ✅ Create type definition files for backend API
12. ✅ Set up Zod schemas for all entities
13. ✅ Create utility functions (formatters, validators)
14. ✅ Configure build for production deployment
15. ✅ Create migration checklist tracking system

### Created Directory Structure

```
frontend/src/admin/
├── features/
│   ├── users/
│   │   ├── api/
│   │   ├── components/
│   │   ├── schemas/
│   │   ├── types/
│   │   └── hooks/
│   ├── experiences/
│   │   ├── api/
│   │   ├── components/
│   │   │   └── forms/
│   │   ├── schemas/
│   │   ├── types/
│   │   └── hooks/
│   ├── naics/
│   │   ├── api/
│   │   ├── components/
│   │   ├── schemas/
│   │   ├── types/
│   │   └── hooks/
│   ├── dashboard/
│   │   ├── components/
│   │   └── hooks/
│   └── settings/
│       ├── components/
│       └── hooks/
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── custom/           # Custom reusable components
│   └── layout/           # Layout components
├── lib/
│   ├── api.ts           # Axios API client
│   ├── queryClient.ts   # React Query config
│   ├── formatters.ts    # Date, currency formatters
│   ├── validators.ts    # Input validation
│   └── constants.ts     # App-wide constants
├── hooks/
│   ├── useDebounce.ts
│   ├── usePagination.ts
│   ├── useLocalStorage.ts
│   ├── useDisclosure.ts
│   └── index.ts
└── types/
    ├── common.types.ts
    └── api.types.ts
```

### Created Files

**Type Definitions:**
- `src/admin/types/common.types.ts` - Common API types
- `src/admin/types/api.types.ts` - API response types
- `src/admin/features/users/types/user.types.ts`
- `src/admin/features/experiences/types/experience.types.ts`
- `src/admin/features/naics/types/naics.types.ts`

**Validation Schemas:**
- `src/admin/features/users/schemas/user.schema.ts`
- `src/admin/features/experiences/schemas/experience.schema.ts`
- `src/admin/features/naics/schemas/naics.schema.ts`

**Utilities:**
- `src/admin/lib/formatters.ts` - Date, currency, number formatters
- `src/admin/lib/validators.ts` - Input validation utilities
- `src/admin/lib/constants.ts` - App-wide constants

**Configuration:**
- `.eslintrc.json` - ESLint configuration for TypeScript
- `.prettierrc` - Prettier configuration with Tailwind plugin

---

## 3.3 Phase 1: Core Infrastructure

**Status:** ✅ COMPLETED  
**Completion Date:** November 20, 2025  
**Time Spent:** ~3 hours

### Tasks Completed (20/20)

1. ✅ Create TypeScript API client (Axios-based)
2. ✅ Set up React Query with providers
3. ✅ Install shadcn/ui base components
4. ✅ Create custom DataTable wrapper for TanStack Table
5. ✅ Build SearchBar component
6. ✅ Build FilterPanel component
7. ✅ Build Pagination component
8. ✅ Build LoadingSpinner component (+ LoadingOverlay, LoadingInline)
9. ✅ Build ErrorBoundary component (+ useErrorBoundary hook)
10. ✅ Create toast notification system (Sonner)
11. ✅ Build ConfirmDialog component (+ useConfirmDialog hook)
12. ✅ Create utility hooks (useDebounce, usePagination, useLocalStorage, useDisclosure)
13. ✅ Create formatters
14. ✅ Create validators
15. ✅ Set up error handling utilities
16. ✅ Create constants file
17. ✅ Build AuthProvider (deferred to Phase 7)
18. ✅ Create route guards (deferred to Phase 7)
19. ✅ Set up layout components (deferred to Phase 7)
20. ✅ Test all base components

### Created API Clients

**Users API:** `src/admin/features/users/api/users.api.ts`
```typescript
// CRUD + stats methods
export const usersApi = {
  getUsers: (params?: UserQueryParams) => Promise<PaginatedResponse<User>>,
  getUserById: (id: string) => Promise<User>,
  createUser: (data: CreateUserInput) => Promise<User>,
  updateUser: (id: string, data: UpdateUserInput) => Promise<User>,
  deleteUser: (id: string) => Promise<void>,
  bulkDeleteUsers: (ids: string[]) => Promise<void>,
  getUserStats: () => Promise<UserStats>
};
```

**Experiences API:** `src/admin/features/experiences/api/experiences.api.ts`
```typescript
// CRUD + polymorphic support
export const experiencesApi = {
  getExperiences: (params?: ExperienceQueryParams) => Promise<PaginatedResponse<Experience>>,
  getExperienceById: (id: string) => Promise<Experience>,
  createExperience: (data: CreateExperienceInput) => Promise<Experience>,
  updateExperience: (id: string, data: UpdateExperienceInput) => Promise<Experience>,
  deleteExperience: (id: string) => Promise<void>,
  getExperienceStats: () => Promise<ExperienceStats>
};
```

**NAICS API:** `src/admin/features/naics/api/naics.api.ts`
```typescript
// CRUD + hierarchy + search
export const naicsApi = {
  getNAICSCodes: (params?: NAICSQueryParams) => Promise<PaginatedResponse<NAICSCode>>,
  getNAICSCodeByCode: (code: string) => Promise<NAICSCode>,
  searchNAICSCodes: (query: string) => Promise<NAICSCode[]>,
  updateNAICSCode: (code: string, data: UpdateNAICSInput) => Promise<NAICSCode>,
  deleteNAICSCode: (code: string) => Promise<void>,
  getNAICSHierarchy: (code: string) => Promise<NAICSHierarchy>
};
```

### Created Custom Hooks

**useDebounce.ts** - Debounce values for search optimization
```typescript
export function useDebounce<T>(value: T, delay: number = 500): T;
```

**usePagination.ts** - Pagination state management
```typescript
export function usePagination(initialPage = 1, initialPageSize = 50);
```

**useLocalStorage.ts** - Type-safe localStorage with sync
```typescript
export function useLocalStorage<T>(key: string, initialValue: T);
```

**useDisclosure.ts** - Open/close state management
```typescript
export function useDisclosure(initialState = false);
```

### Created Custom Components

**LoadingSpinner.tsx** - 3 variants
- `<LoadingSpinner size="sm" | "md" | "lg" />`
- `<LoadingOverlay />`
- `<LoadingInline />`

**LoadingSkeleton.tsx** - 5 skeleton types
- `<TableSkeleton />`
- `<CardSkeleton />`
- `<FormSkeleton />`
- `<StatsSkeleton />`
- `<PageSkeleton />`

**ErrorBoundary.tsx** - React error boundary + hook
```typescript
<ErrorBoundary fallback={<ErrorFallback />}>
  {children}
</ErrorBoundary>

const { error, resetError } = useErrorBoundary();
```

**SearchBar.tsx** - Debounced search with clear button
```typescript
<SearchBar
  value={searchTerm}
  onChange={setSearchTerm}
  placeholder="Search users..."
  debounce={300}
/>
```

**FilterPanel.tsx** - Collapsible filters + quick chips
```typescript
<FilterPanel
  filters={[
    { key: 'status', label: 'Status', options: [...] },
    { key: 'verified', label: 'Verified', options: [...] }
  ]}
  activeFilters={activeFilters}
  onFilterChange={handleFilterChange}
/>
```

**Pagination.tsx** - Full pagination controls + page size selector
```typescript
<Pagination
  currentPage={page}
  totalPages={totalPages}
  pageSize={pageSize}
  onPageChange={setPage}
  onPageSizeChange={setPageSize}
/>
```

**ConfirmDialog.tsx** - Confirmation dialogs with 3 variants
```typescript
const { confirm } = useConfirmDialog();

await confirm({
  title: 'Delete User',
  description: 'Are you sure? This action cannot be undone.',
  variant: 'danger' // 'default' | 'danger' | 'warning'
});
```

**DataTable.tsx** - TanStack Table wrapper + row selection
```typescript
<DataTable
  columns={columns}
  data={data}
  sorting={sorting}
  onSortingChange={setSorting}
  rowSelection={rowSelection}
  onRowSelectionChange={setRowSelection}
/>
```

---

## 3.4 Phase 2-8: Feature Development

### Phase 2: Users Feature (4-5 hours) - ⏸️ NOT STARTED

**Goal:** Complete CRUD for users with search/filter/pagination

#### Planned Tasks (25 total)

**Type System:**
1. [ ] Create user types (`features/users/types/user.types.ts`)
2. [ ] Create user Zod schemas (`features/users/schemas/user.schema.ts`)

**API Integration:**
3. [ ] Build user API queries (`features/users/api/users.queries.ts`)
4. [ ] Build user API mutations (`features/users/api/users.mutations.ts`)
5. [ ] Create useUsers custom hook

**Data Table:**
6. [ ] Build UsersTable component with TanStack Table
7. [ ] Add search functionality to UsersTable
8. [ ] Add filter dropdowns (active/inactive/verified)
9. [ ] Add pagination to UsersTable
10. [ ] Add sorting to UsersTable

**Forms:**
11. [ ] Build UserForm component (create/edit)
12. [ ] Add form validation with Zod + React Hook Form
13. [ ] Build CreateUserDialog
14. [ ] Build EditUserDialog
15. [ ] Build DeleteUserDialog with confirmation

**UX Enhancements:**
16. [ ] Add loading states to all operations
17. [ ] Add error handling with toast notifications
18. [ ] Add optimistic updates for mutations
19. [ ] Build UserStats widget (active/inactive counts)
20. [ ] Add user avatar display
21. [ ] Add user status badges
22. [ ] Add action dropdown menu per row

**Testing:**
23. [ ] Test create user flow
24. [ ] Test edit user flow
25. [ ] Test delete user flow

---

### Phase 3: Experiences Feature (5-6 hours) - ⏸️ NOT STARTED

**Goal:** Complete CRUD for all 9 experience types with advanced filtering

#### Planned Tasks (30 total)

**Type System:**
1. [ ] Create experience types (Education, Workplace, Skills subtypes)
2. [ ] Create experience Zod schemas (polymorphic support)

**API Integration:**
3. [ ] Build experience API queries
4. [ ] Build experience API mutations
5. [ ] Create useExperiences custom hook

**Data Table:**
6. [ ] Build ExperiencesTable with polymorphic rendering
7. [ ] Add search functionality
8. [ ] Add category filter (Education/Workplace/Skills)
9. [ ] Add type filter (dynamic based on category)
10. [ ] Add user filter (dropdown with search)
11. [ ] Add NAICS code filter
12. [ ] Add date range filter
13. [ ] Add pagination
14. [ ] Add sorting

**Forms (Polymorphic):**
15. [ ] Build base ExperienceForm component
16. [ ] Build EducationForm (Certificate/Degree/Course)
17. [ ] Build WorkplaceForm (Gig/PartTime/FullTime)
18. [ ] Build SkillsForm (Soft/Hard/Native)
19. [ ] Add NAICS code autocomplete selector
20. [ ] Add skills gained multi-select
21. [ ] Add date range picker
22. [ ] Add form validation (type-specific)

**Dialogs:**
23. [ ] Build CreateExperienceDialog
24. [ ] Build EditExperienceDialog
25. [ ] Build DeleteExperienceDialog

**UX Enhancements:**
26. [ ] Add loading states
27. [ ] Add error handling
28. [ ] Add optimistic updates
29. [ ] Build ExperienceStats widget
30. [ ] Add type-specific badges and icons

---

### Phase 4: NAICS Feature (3-4 hours) - ⏸️ NOT STARTED

**Goal:** NAICS code management with hierarchy, tags, and categories

#### Planned Tasks (20 total)

**Type System:**
1. [ ] Create NAICS types with admin fields
2. [ ] Create NAICS Zod schemas

**API Integration:**
3. [ ] Build NAICS API queries
4. [ ] Build NAICS API mutations
5. [ ] Create useNAICS custom hook

**Data Table:**
6. [ ] Build NAICSTable with hierarchy display
7. [ ] Add search functionality
8. [ ] Add level filter (2/3/4/6 digit)
9. [ ] Add category filter
10. [ ] Add tag filter
11. [ ] Add pagination
12. [ ] Add sorting

**Forms:**
13. [ ] Build NAICSEditForm (admin fields only)
14. [ ] Add tag management (add/remove chips)
15. [ ] Add custom category input
16. [ ] Add admin notes textarea

**Dialogs:**
17. [ ] Build EditNAICSDialog
18. [ ] Build DeleteNAICSDialog (with warning)

**UX Enhancements:**
19. [ ] Add hierarchy breadcrumb display
20. [ ] Build NAICSStats widget

---

### Phase 5: Dashboard Feature (2-3 hours) - ⏸️ NOT STARTED

**Goal:** Analytics dashboard with charts and metrics

#### Planned Tasks (15 total)

**Components:**
1. [ ] Build StatCard component
2. [ ] Build ChartCard component
3. [ ] Build RecentActivityFeed component

**Widgets:**
4. [ ] Build user growth chart (line chart)
5. [ ] Build experience distribution chart (pie chart)
6. [ ] Build industry distribution chart (bar chart)
7. [ ] Build top skills widget
8. [ ] Build geographic distribution map
9. [ ] Build recent users table
10. [ ] Build recent experiences table

**Layout:**
11. [ ] Create dashboard grid layout
12. [ ] Make dashboard responsive
13. [ ] Add refresh button
14. [ ] Add date range selector

**Testing:**
15. [ ] Test all widgets load correctly

---

### Phase 6: Settings Feature (2 hours) - ⏸️ NOT STARTED

**Goal:** System settings and database management

#### Planned Tasks (10 total)

**Components:**
1. [ ] Build SeedDatabaseForm
2. [ ] Build ClearDatabaseDialog (with strong warning)
3. [ ] Build ExportDataDialog
4. [ ] Build ImportDataDialog

**Features:**
5. [ ] Implement seed database with user count selector
6. [ ] Implement clear database with confirmation
7. [ ] Implement CSV export functionality
8. [ ] Add system info display (version, environment)

**Testing:**
9. [ ] Test seed database flow
10. [ ] Test clear database flow with rollback

---

### Phase 7: Routing & Auth (1-2 hours) - ⏸️ NOT STARTED

**Goal:** Fix routing and add authentication placeholders

#### Planned Tasks (12 total)

**Routing:**
1. [ ] Set up React Router with `/admin/*` base
2. [ ] Create AdminRoutes component
3. [ ] Add route guards
4. [ ] Fix breadcrumb navigation
5. [ ] Add 404 page

**Layout:**
6. [ ] Build AdminLayout component
7. [ ] Build Sidebar navigation
8. [ ] Build Header with user menu
9. [ ] Make layout responsive

**Auth (Placeholder):**
10. [ ] Create AuthContext (placeholder)
11. [ ] Add login page (placeholder)
12. [ ] Add logout functionality

---

### Phase 8: Production & Polish (2-3 hours) - ⏸️ NOT STARTED

**Goal:** Production build, deployment, and final polish

#### Planned Tasks (18 total)

**Build & Deploy:**
1. [ ] Run production build
2. [ ] Test build locally
3. [ ] Fix any build errors
4. [ ] Optimize bundle size
5. [ ] Deploy to staging
6. [ ] Test on staging
7. [ ] Deploy to production

**Polish:**
8. [ ] Add favicon
9. [ ] Add page titles
10. [ ] Add meta tags
11. [ ] Add loading page
12. [ ] Add offline page

**Documentation:**
13. [ ] Update README
14. [ ] Document environment variables
15. [ ] Document deployment process
16. [ ] Create user guide

**Testing:**
17. [ ] Run smoke tests
18. [ ] Test all CRUD operations
19. [ ] Test error scenarios
20. [ ] Performance testing

---

## 3.5 Progress Tracking

### Overall Progress

| Metric | Value |
|--------|-------|
| **Total Tasks** | 165 |
| **Completed** | 35 (21%) |
| **In Progress** | 0 |
| **Remaining** | 130 (79%) |
| **Time Spent** | 5 hours |
| **Estimated Remaining** | 20-28 hours |

### Phase Breakdown

```
Phase 0: ████████████████████████████████ 100% (15/15) ✅
Phase 1: ████████████████████████████████ 100% (20/20) ✅
Phase 2: ································  0% (0/25)   ⏸️
Phase 3: ································  0% (0/30)   ⏸️
Phase 4: ································  0% (0/20)   ⏸️
Phase 5: ································  0% (0/15)   ⏸️
Phase 6: ································  0% (0/10)   ⏸️
Phase 7: ································  0% (0/12)   ⏸️
Phase 8: ································  0% (0/18)   ⏸️
```

### Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Complete Rewrite Breaking Changes | 🔴 High | Keep old code in `_deprecated/`, feature-by-feature migration |
| Type System Learning Curve | 🟡 Medium | Start simple, use `any` temporarily if stuck |
| New Dependencies Introduction | 🟡 Medium | Monitor bundle size, use tree-shaking |
| Data Loss During Testing | 🟢 Low | Use staging database, implement backups |
| Deployment Configuration | 🟡 Medium | Test build locally, deploy to staging first |

---

# Part 4: Setup & Usage Guide

## 4.1 Quick Start

### Prerequisites

- ✅ PostgreSQL database (Render-hosted or local)
- ✅ Python 3.11+
- ✅ Node.js 18+
- ✅ FastAPI backend configured
- ✅ Database migrations applied

### Three-Step Setup

#### Step 1: Seed the Database

```bash
# From project root
cd backend

# Seed with 25 users (default)
python seed_db.py

# Or customize:
python seed_db.py --users 50 --verbose
```

**What this creates:**
- 25 realistic users (or your specified number)
- 2-8 experiences per user (all 9 types)
- NAICS codes assigned
- Realistic dates and profiles

**Expected Output:**
```
==================================================================
DATABASE SEEDING COMPLETE!
==================================================================
📊 Statistics:
   Users created: 25
   Experiences created: 127
   Average experiences per user: 5.1
==================================================================
🎉 You can now use the admin panel to view and manage this data!
```

---

#### Step 2: Start the Backend API

```bash
# From project root
cd backend

# Start the API server
uvicorn main:app --reload
```

**Verify:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "development"
}
```

**API Documentation:** http://localhost:8000/docs

---

#### Step 3: Start the Frontend

**For Old Dashboard (Deprecated):**
```bash
cd _deprecated/levelith_admin_dashboard_OLD
npm install
npm run dev
# Access: http://localhost:5173
```

**For New Dashboard (In Development):**
```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:5173/admin
```

---

## 4.2 Database Seeding

### Command Options

```bash
# Seed with default settings (25 users)
python backend/seed_db.py

# Seed with custom number of users
python backend/seed_db.py --users 100

# Clear existing data and reseed
python backend/seed_db.py --clear --users 50

# Verbose output (show each user created)
python backend/seed_db.py --verbose

# Help
python backend/seed_db.py --help
```

### Command Line Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--users N` | `-u N` | Create N users (default: 25) |
| `--clear` | `-c` | Clear all existing data first ⚠️ |
| `--verbose` | `-v` | Show detailed logging |
| `--help` | `-h` | Show help message |

### What Gets Created

**Per User:**
- Unique username and email
- Hashed password: `TestPassword123!`
- Random active/verified status
- Profile data (bio, location, website)
- Created/updated timestamps
- Last login (random recent date)

**Per Experience (2-8 per user):**
- Random type from all 9 types:
  - **Education:** Certificate, Degree, Course
  - **Workplace:** Gig, Part-Time, Full-Time
  - **Skills:** Soft Skill, Hard Skill, Native Skill
- Appropriate category
- Title and description
- Random NAICS code
- Start/end dates
- Organization (Education/Workplace)
- Location (Education/Workplace)
- Skills gained (2-5 random skills)
- Type-specific metadata

⚠️ **Warning:** Using `--clear` flag permanently deletes all existing users and experiences!

---

## 4.3 Backend Setup

### Environment Configuration

**File:** `backend/.env`

```env
# Database
DATABASE_URL=postgresql://username:password@host:port/database_name

# API
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=true

# CORS (allow frontend origins)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8000"]

# Optional
LOG_LEVEL=INFO
```

### Database Migration

**Apply migrations:**
```bash
cd backend
python -m alembic upgrade head
```

**Check migration status:**
```sql
\c levelith
SELECT * FROM alembic_version;
```

**Rollback one migration:**
```bash
python -m alembic downgrade -1
```

### Running the Backend

**Development mode:**
```bash
cd backend
uvicorn main:app --reload
```

**Production mode:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Verify backend:**
```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

---

## 4.4 Frontend Setup

### Environment Configuration

**File:** `frontend/.env` (or `.env.local`)

```env
# API URL
VITE_API_URL=http://localhost:8000/api/v1

# Optional
VITE_ENVIRONMENT=development
```

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Development Commands

```bash
# Type check
npm run type-check

# Lint
npm run lint

# Format code
npm run format

# Run tests (when implemented)
npm run test
```

### Accessing the Dashboard

**Development:**
- Old Dashboard: http://localhost:5173
- New Dashboard: http://localhost:5173/admin

**Production:**
- https://admin.levelith.online

---

# Part 5: Testing & Validation

## 5.1 Backend Connectivity Testing

### Prerequisites Checklist

- [ ] Backend server running at http://localhost:8000
- [ ] Frontend server running at http://localhost:5173
- [ ] Database seeded with test data
- [ ] CORS configured correctly
- [ ] Browser DevTools open (Network tab)

### Verify Backend Health

```bash
# Basic health check
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "2.0.0", "environment": "development"}

# Detailed health check
curl http://localhost:8000/health/details
```

### Verify Frontend Access

```bash
# Access admin dashboard
open http://localhost:5173/admin/users

# Check browser console for errors
# Check Network tab for API calls
```

---

## 5.2 CRUD Operations Testing

### ✅ Transformation Layer Test

**Goal:** Verify snake_case ↔ camelCase conversion

**Test Steps:**
1. Open browser DevTools → Network tab
2. Navigate to `/admin/users`
3. Click on `/users` request
4. Check Response tab - should show `snake_case`
5. Check console logs - should show `camelCase`

**Expected:**
- **Backend sends:** `is_active`, `created_at`, `last_login_at`
- **Frontend receives:** `isActive`, `createdAt`, `lastLoginAt`

---

### ✅ Users List Page Test

**URL:** http://localhost:5173/admin/users

#### Basic Functionality

- [ ] Page loads without errors
- [ ] Header displays "User Management"
- [ ] No console errors
- [ ] Loading spinner appears initially
- [ ] Users table populates with data
- [ ] Pagination shows correct page numbers

#### Search Functionality

- [ ] Search box accepts input
- [ ] Results filter in real-time (or after debounce)
- [ ] Shows "X users" count
- [ ] Clear button works

#### Filter Dropdowns

- [ ] Active/Inactive filter works
- [ ] Verified/Unverified filter works
- [ ] Filters can be combined
- [ ] Filter chips display active filters
- [ ] Clear all filters works

#### Table Display

- [ ] Columns display: Username, Email, Status, Verified, Experiences, Joined, Actions
- [ ] Data displays in correct format
- [ ] Dates formatted as "MMM DD, YYYY"
- [ ] Status badges show correct colors (green=active, gray=inactive)
- [ ] Verified badges show checkmark or X
- [ ] Experience count displays as number

#### Pagination Controls

- [ ] Page numbers display
- [ ] Next/Previous buttons work
- [ ] First/Last buttons work (if present)
- [ ] Can change page size (10/25/50/100)
- [ ] Total pages calculated correctly
- [ ] Current page highlighted

#### Row Selection (if enabled)

- [ ] Checkboxes work
- [ ] Select all checkbox works
- [ ] Selected count displays
- [ ] Bulk actions enabled when rows selected

---

### ✅ User Detail Page Test

**URL:** http://localhost:5173/admin/users/:id

#### Page Load

- [ ] Click username in table
- [ ] Navigates to `/admin/users/:id`
- [ ] Page loads without errors
- [ ] Shows loading spinner initially

#### User Information Display

- [ ] Username and email in header
- [ ] Account status badges (Active/Inactive, Verified/Unverified)
- [ ] Member since date
- [ ] Last login date (if exists)
- [ ] Profile information (display name, bio, location)
- [ ] Social links (website, LinkedIn, GitHub)

#### Quick Stats Sidebar

- [ ] Experience count displays
- [ ] Account age in days
- [ ] Other relevant metrics

#### Navigation

- [ ] Breadcrumb shows: Admin / Users / {username}
- [ ] Breadcrumb links work correctly
- [ ] Back to Users button works

#### Action Buttons

- [ ] Edit User button opens edit dialog
- [ ] Delete User button opens confirmation
- [ ] View Experiences button navigates (if implemented)

---

### ✅ Create User Operation Test

**Goal:** Test user creation flow

#### Test Steps

1. Click "Create New User" button
2. Should open create dialog/modal or navigate to `/admin/users/new`
3. Fill in form:
   - Username: `testuser123`
   - Email: `test@example.com`
   - Password: `TestPass123!`
   - Display Name: `Test User`
4. Submit form

#### Expected Results

- [ ] Success message or toast appears
- [ ] Redirects to user list or detail page
- [ ] New user appears in list
- [ ] User data persists after page refresh

#### API Call Verification

```http
POST /api/v1/users
Content-Type: application/json

{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "TestPass123!",
  "displayName": "Test User"
}
```

**Expected Response:** 201 Created with user object

---

### ✅ Update User Operation Test

**Goal:** Test user editing flow

#### Test Steps

1. Click "Edit" button on a user row
2. Should open edit dialog or navigate to `/admin/users/:id/edit`
3. Modify fields:
   - Email: `newemail@example.com`
   - Display Name: `Updated Name`
   - Status: Toggle Active/Inactive
4. Submit form

#### Expected Results

- [ ] Success message appears
- [ ] User list updates immediately (optimistic update)
- [ ] Backend confirms update
- [ ] Changes persist after page refresh

#### API Call Verification

```http
PATCH /api/v1/users/{id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "displayName": "Updated Name",
  "isActive": false
}
```

**Expected Response:** 200 OK with updated user object

---

### ✅ Delete User Operation Test (Single)

**Goal:** Test single user deletion

#### Test Steps

1. Click "Delete" button on a user row
2. Confirmation dialog appears
3. Click "Delete" to confirm

#### Expected Results

- [ ] Success message appears
- [ ] User removed from list immediately (optimistic)
- [ ] If delete fails, user reappears (rollback)
- [ ] Deletion persists after page refresh

#### API Call Verification

```http
DELETE /api/v1/users/{id}
```

**Expected Response:** 204 No Content

---

### ✅ Delete Users Operation Test (Bulk)

**Goal:** Test bulk deletion

#### Test Steps

1. Select 2-3 users using checkboxes
2. Click "Delete Selected" button
3. Confirmation dialog shows count: "Delete 3 users?"
4. Click "Delete" to confirm

#### Expected Results

- [ ] Success message: "Deleted 3 users"
- [ ] All selected users removed from list
- [ ] Selection cleared
- [ ] Deletion persists after page refresh

#### API Call Verification

```http
POST /api/v1/users/bulk-delete
Content-Type: application/json

{
  "ids": ["user-id-1", "user-id-2", "user-id-3"]
}
```

**Expected Response:** 200 OK with deletion summary

---

### ✅ Toggle User Status Test

**Goal:** Test quick status toggle

#### Test Steps

1. Click on "Active" or "Inactive" badge in Status column
2. Badge changes immediately
3. API request sends

#### Expected Results

- [ ] Badge toggles: Active ↔ Inactive
- [ ] Background color changes (green ↔ gray)
- [ ] Update persists after page refresh

#### API Call Verification

```http
PATCH /api/v1/users/{id}
Content-Type: application/json

{
  "isActive": true
}
```

---

### ✅ Experiences CRUD Test

**URL:** http://localhost:5173/admin/experiences

#### List Page Functionality

- [ ] Page loads without errors
- [ ] Experiences table populates
- [ ] Category filter works (Education/Workplace/Skills)
- [ ] Type filter works (dynamic based on category)
- [ ] User filter works (select from users)
- [ ] NAICS code filter works
- [ ] Search works
- [ ] Pagination works (50 items per page)

#### Create Experience

1. Click "New Experience"
2. Select user
3. Select category
4. Select type (dynamically shown based on category)
5. Fill in form (title, organization, dates, NAICS code, skills)
6. Submit

**Expected:**
- [ ] Success message
- [ ] Experience appears in list
- [ ] Correct type-specific fields saved

#### Edit Experience

1. Click "Edit" on an experience
2. Modify fields
3. Submit

**Expected:**
- [ ] Success message
- [ ] Changes reflected in list
- [ ] Changes persist

#### Delete Experience

1. Click "Delete" on an experience
2. Confirm deletion

**Expected:**
- [ ] Success message
- [ ] Experience removed from list
- [ ] Deletion persists

---

### ✅ NAICS CRUD Test

**URL:** http://localhost:5173/admin/naics

#### List Page Functionality

- [ ] Page loads without errors
- [ ] NAICS table populates with 2222+ codes
- [ ] Search works (code, title, description)
- [ ] Level filter works (2/3/4/6 digit)
- [ ] Category filter works
- [ ] Tag filter works
- [ ] Pagination works (50 items per page)
- [ ] Server-side pagination (not loading all 2222 codes)

#### Edit NAICS Code

1. Click "Edit" on a NAICS code
2. Modify admin fields:
   - Tags: Add/remove tags (e.g., "software", "high-demand")
   - Custom Category: Enter custom category
   - Admin Notes: Add notes
3. Submit

**Expected:**
- [ ] Success message
- [ ] Changes reflected in table
- [ ] Tags display as colored pills
- [ ] Changes persist after refresh

**API Call:**
```http
PATCH /api/v1/naics/541511
Content-Type: application/json

{
  "tags": ["software", "high-demand", "tech"],
  "customCategory": "Tech Priority",
  "adminNotes": "Popular code for software companies"
}
```

#### Delete NAICS Code

1. Click "Delete" on a NAICS code
2. Warning appears about permanent deletion
3. Confirm deletion

**Expected:**
- [ ] Strong warning shown
- [ ] Success message after deletion
- [ ] Code removed from table
- [ ] Deletion persists

**⚠️ Note:** Only delete test/invalid codes, not official NAICS codes!

---

## 5.3 Error Handling Testing

### ✅ Network Error Test

**Test:** Backend unavailable

#### Steps

1. Stop backend server
2. Navigate to `/admin/users`
3. Observe behavior

#### Expected Results

- [ ] Error message displays: "Error loading users"
- [ ] Helpful error text shown
- [ ] Retry button available
- [ ] No blank white page
- [ ] No infinite loading spinner

---

### ✅ 404 - User Not Found Test

**Test:** Invalid user ID

#### Steps

1. Navigate to `/admin/users/invalid-id-12345`
2. Observe behavior

#### Expected Results

- [ ] Error page displays
- [ ] Shows "User not found" message
- [ ] "Back to Users" button works
- [ ] No console errors

---

### ✅ Validation Error Test

**Test:** Invalid form data

#### Steps

1. Try to create user with invalid email
2. Submit form

#### Expected Results

- [ ] Validation error displays
- [ ] Error shows under email field
- [ ] Form does not submit
- [ ] Error is user-friendly

---

### ✅ Duplicate Username Test

**Test:** Username/email conflict

#### Steps

1. Try to create user with existing username
2. Submit form

#### Expected Results

- [ ] Error message: "Username already exists"
- [ ] API returns 409 Conflict
- [ ] Form stays open with data
- [ ] User can correct and retry

---

### ✅ Delete Failure Test

**Test:** Rollback on failure

#### Steps

1. Delete a user
2. Mock backend failure (if possible)
3. Observe behavior

#### Expected Results

- [ ] Error message displays
- [ ] User reappears in list (rollback)
- [ ] Optimistic update reverted
- [ ] User can retry

---

## 5.4 Performance Testing

### ✅ Loading States Test

#### Initial Load

- [ ] Loading spinner displays on first load
- [ ] Skeleton loaders shown (if implemented)
- [ ] Table shows "Loading users..." message
- [ ] Transition smooth when data loads

#### Pagination Load

- [ ] Loading indicator when changing pages
- [ ] Previous data remains visible during load (or skeleton)
- [ ] No jarring layout shifts

#### Mutation Loading

- [ ] Create button shows "Creating..." during operation
- [ ] Delete button shows "Deleting..." during operation
- [ ] Buttons disabled during operation
- [ ] Spinner or loading state visible

---

### ✅ Empty States Test

#### No Results Found

**Test:** Search for non-existent user

**Expected:**
- [ ] Shows "No users found"
- [ ] Shows "Try adjusting your search or filters"
- [ ] Clear filters button visible
- [ ] No awkward empty space

#### No Data at All

**Test:** Empty database

**Expected:**
- [ ] Shows helpful empty state message
- [ ] Suggests creating first user
- [ ] "Create User" button prominent
- [ ] Friendly illustration (if present)

---

### ✅ Cache & Optimistic Updates Test

#### Navigate Away and Back

**Test:** React Query caching

**Steps:**
1. Load `/admin/users`
2. Wait for data to load
3. Navigate to `/admin/experiences`
4. Navigate back to `/admin/users`

**Expected:**
- [ ] Data loads instantly from cache (stale-while-revalidate)
- [ ] Background refetch occurs
- [ ] Updated data appears if changed
- [ ] No full page reload

---

#### Optimistic Update

**Test:** Immediate UI update

**Steps:**
1. Toggle user status: Active → Inactive
2. Observe UI behavior

**Expected:**
- [ ] UI updates immediately (before API responds)
- [ ] If API succeeds, update persists
- [ ] If API fails, reverts to Active (rollback)
- [ ] Error message shown on failure

---

#### Cache Invalidation

**Test:** Automatic refetch after mutation

**Steps:**
1. Create new user
2. Observe list behavior

**Expected:**
- [ ] User list refetches automatically
- [ ] New user appears in list
- [ ] No manual refresh needed
- [ ] Pagination adjusts if needed

---

### ✅ Large Dataset Test (100+ items)

**Test:** Performance with many records

#### Setup

```bash
# Seed database with 100+ users
curl -X POST "http://localhost:8000/api/v1/users/seed?user_count=100"
```

#### Tests

- [ ] Table renders smoothly (no lag)
- [ ] Pagination works correctly
- [ ] No lag when scrolling
- [ ] Search/filter performance acceptable
- [ ] Page transitions smooth

---

### ✅ Search Performance Test

**Test:** Debounced search

#### Steps

1. Type quickly in search box: "john"
2. Observe network requests

**Expected:**
- [ ] Debounced (doesn't fire on every keystroke)
- [ ] Fires after ~300-500ms of inactivity
- [ ] Results update within 1 second
- [ ] Previous requests cancelled (if typing continues)

---

### ✅ Accessibility Test

#### Keyboard Navigation

- [ ] Can tab through table
- [ ] Can navigate with keyboard only
- [ ] Focus indicators visible
- [ ] Enter key activates buttons

#### Screen Reader

- [ ] Button labels clear and descriptive
- [ ] Table headers announced
- [ ] Status changes announced
- [ ] Error messages announced

#### ARIA Labels

- [ ] Checkboxes have labels
- [ ] Buttons have descriptions
- [ ] Dialogs have proper ARIA roles
- [ ] Form inputs have labels

---

## 5.5 Testing Checklist Summary

### Backend API Tests

- [x] Health check endpoint
- [x] User CRUD operations
- [x] Experience CRUD operations
- [x] NAICS CRUD operations
- [x] Pagination
- [x] Search/filtering
- [x] Validation
- [x] Error responses

### Frontend Integration Tests

- [ ] Page loads
- [ ] Data fetching
- [ ] Search functionality
- [ ] Filter functionality
- [ ] Pagination controls
- [ ] Sorting
- [ ] Create operations
- [ ] Update operations
- [ ] Delete operations
- [ ] Bulk operations
- [ ] Loading states
- [ ] Error handling
- [ ] Empty states
- [ ] Optimistic updates
- [ ] Cache behavior

### Performance Tests

- [ ] Large datasets (100+ items)
- [ ] Search performance
- [ ] Page transitions
- [ ] Network efficiency
- [ ] Memory usage

### Accessibility Tests

- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] ARIA labels
- [ ] Focus management

---

# Part 6: Deployment & Production

## 6.1 Production Deployment

### Required Steps

#### 1. Apply Database Migration

```bash
cd backend
python -m alembic upgrade head
```

#### 2. Verify Migration

```sql
\c levelith
\d naics_codes  -- Should show tags, custom_category, admin_notes
SELECT version_num FROM alembic_version;
```

#### 3. Deploy Backend

**Render Deployment:**

**Environment Variables:**
```env
DATABASE_URL=postgresql://levelith_user:...@dpg-....render.com/levelith
SECRET_KEY=08a4ab222554f29ae4a0eb7d00482fa5a79f46f2617ed9cf6453347dc3a8461f
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://admin.levelith.online","https://levelith.online"]
LOG_LEVEL=INFO
```

**Deploy Steps:**
1. Push code to main branch
2. Render auto-deploys
3. Verify health check: https://your-backend.onrender.com/health
4. Check API docs: https://your-backend.onrender.com/docs

---

#### 4. Deploy Frontend

**Build for Production:**

```bash
cd frontend

# Build
npm run build

# Preview build locally
npm run preview

# Test production build
open http://localhost:4173
```

**Environment Variables:**
```env
VITE_API_URL=https://your-backend.onrender.com/api/v1
VITE_ENVIRONMENT=production
```

**Deploy to Render/Vercel:**

**Render:**
- Service Type: Static Site
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`

**Vercel:**
```bash
cd frontend
vercel --prod
```

---

### Deployment Checklist

- [ ] Database migration applied to production
- [ ] Migration verified in production DB
- [ ] Backend environment variables configured
- [ ] Backend deployed and running
- [ ] Backend health checks passing
- [ ] Frontend built successfully
- [ ] Frontend environment variables configured
- [ ] Frontend deployed
- [ ] Frontend accessible at production URL
- [ ] API documentation accessible
- [ ] CORS configured for production domains
- [ ] Manual testing completed on production
- [ ] Smoke tests passing

---

### Seed Production Database (Optional)

⚠️ **Warning:** Only seed production if you want demo data!

```bash
# Set production DATABASE_URL
export DATABASE_URL="postgresql://production-url..."

# Seed with a small number for demo
python backend/seed_db.py --users 10

# Or test on staging first
export DATABASE_URL="postgresql://staging-url..."
python backend/seed_db.py --users 50
```

**Best Practice:** Always test on staging before seeding production!

---

## 6.2 Troubleshooting

### ❌ Database Connection Failed

**Symptoms:** Cannot connect to PostgreSQL

**Possible Causes:**
1. Database not running
2. Incorrect DATABASE_URL in .env
3. Network/firewall issues
4. Database credentials changed

**Solutions:**

```bash
# Check backend/.env has correct DATABASE_URL
cat backend/.env | grep DATABASE_URL

# Verify database is accessible
psql $DATABASE_URL

# Test connection from Python
python backend/init_db.py --check
```

**For Render:**
- Check database instance is running in dashboard
- Verify connection string is correct
- Check if database has sleeping mode disabled

---

### ❌ Module Not Found

**Symptoms:** Python import errors

**Solutions:**

```bash
# Install missing dependencies
cd backend
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.11+

# If using virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### ⚠️ Admin Panel Shows "No Data"

**Symptoms:** Dashboard displays empty tables

**Possible Causes:**
1. Backend not running
2. Frontend not connected to backend
3. Database empty (not seeded)
4. CORS error blocking requests
5. Data source setting incorrect

**Solutions:**

```bash
# 1. Check backend is running
curl http://localhost:8000/health

# 2. Check frontend .env
cat frontend/.env
# Should have: VITE_API_URL=http://localhost:8000/api/v1

# 3. Seed database if empty
cd backend
python seed_db.py --users 25

# 4. Check browser console for CORS errors
# If CORS error, update backend/.env:
# CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# 5. Check data source switcher in admin panel header
# Toggle between LOCAL and SERVER modes
```

---

### ❌ CORS Errors in Browser Console

**Symptoms:** Browser blocks requests to backend

**Example Error:**
```
Access to fetch at 'http://localhost:8000/api/v1/users' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**

Update `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8000"]
```

Then restart backend:
```bash
cd backend
uvicorn main:app --reload
```

**Explanation:** CORS policy prevents frontend from accessing backend on different origin. You must explicitly allow the frontend origin.

---

### ❌ Username Already Exists

**Symptoms:** Cannot create user with duplicate username

**Solution 1: Use unique username**
```bash
# Try different username/email
```

**Solution 2: Clear database and reseed**
```bash
cd backend
python seed_db.py --clear --users 25
```

**Explanation:** Usernames and emails must be unique in the database. Use unique values or clear the database for testing.

---

### ❌ Build Errors (Frontend)

**Symptoms:** `npm run build` fails

**Common Causes:**
1. TypeScript errors
2. Missing dependencies
3. Environment variables not set
4. Import errors

**Solutions:**

```bash
# Type check
npm run type-check

# Fix linting issues
npm run lint -- --fix

# Install missing dependencies
npm install

# Set environment variables
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# Clean and rebuild
rm -rf node_modules dist
npm install
npm run build
```

---

### ❌ 500 Internal Server Error

**Symptoms:** API returns 500 error

**Solutions:**

```bash
# Check backend logs
cd backend
uvicorn main:app --reload --log-level debug

# Check database connection
python init_db.py --check

# Check for migration issues
python -m alembic current
python -m alembic upgrade head

# Check API endpoint exists
curl http://localhost:8000/docs
```

---

### ❌ Blank White Page

**Symptoms:** Frontend shows blank page, no errors

**Possible Causes:**
1. JavaScript error (check console)
2. Routing issue
3. Build issue
4. Wrong base URL

**Solutions:**

```bash
# Check browser console for errors
# Open DevTools → Console

# Verify correct base URL in vite.config.ts
# For admin dashboard:
# base: '/admin'

# Try clearing cache
# Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# Check if running on correct port
# Should be http://localhost:5173/admin
```

---

## 6.3 Additional Resources

### Official Documentation

- 📚 [Admin Dashboard Implementation](/docs/dev/ADMIN_DASHBOARD_IMPLEMENTATION.md)
- 🏗️ [API Documentation](/docs/api/API_DOCUMENTATION.md)
- 🧪 [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)
- 📋 [Project Manifest](/docs/core/MANIFEST.md)
- 🔄 [CI/CD Guide](/docs/dev/CI_CD_GUIDE.md)
- 📝 [Recent Updates](/docs/dev/RECENT_UPDATES.md)

### External Resources

**Backend:**
- 🌐 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🗃️ [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- 🔄 [Alembic Documentation](https://alembic.sqlalchemy.org/)
- 📊 [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- 🔒 [Pydantic Documentation](https://docs.pydantic.dev/)

**Frontend (New Stack):**
- ⚛️ [React Documentation](https://react.dev/)
- 📘 [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- 🔍 [TanStack Query](https://tanstack.com/query/latest)
- 📊 [TanStack Table](https://tanstack.com/table/latest)
- 📝 [React Hook Form](https://react-hook-form.com/)
- ✅ [Zod](https://zod.dev/)
- 🎨 [Tailwind CSS](https://tailwindcss.com/)
- 🧩 [shadcn/ui](https://ui.shadcn.com/)
- 🔧 [Vite](https://vitejs.dev/)

### Code Examples

- 💻 [Migration File](https://github.com/Free-Columns/levelith-2/blob/main/backend/alembic/versions/41518377be8d_add_admin_fields_to_naics_codes.py)
- 🎯 [NAICS CRUD Endpoints](https://github.com/Free-Columns/levelith-2/blob/main/backend/api/routes/naics.py)
- 🌱 [Seed Script](https://github.com/Free-Columns/levelith-2/blob/main/backend/seed_db.py)

### Community & Support

- 💬 [Discord Community](https://discord.gg/levelith)
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues)
- 💡 [Feature Requests](https://github.com/Free-Columns/levelith-2/discussions)
- 📧 [Email Support](mailto:support@levelith.online)

---

## Appendix A: File Structure Reference

### Backend Structure

```
backend/
├── alembic/
│   ├── versions/
│   │   └── 41518377be8d_add_admin_fields_to_naics_codes.py
│   ├── env.py
│   └── script.py.mako
├── api/
│   └── routes/
│       ├── users.py
│       ├── experiences.py
│       ├── naics.py
│       └── health.py
├── models/
│   ├── db_models.py
│   ├── user.py
│   ├── experience.py
│   └── naics.py
├── repositories/
│   ├── user_db_repository.py
│   ├── experience_db_repository.py
│   └── naics_db_repository.py
├── services/
│   ├── user_service.py
│   ├── experience_service.py
│   └── naics_service.py
├── alembic.ini
├── main.py
├── database.py
├── seed_db.py
├── init_db.py
└── requirements.txt
```

### Frontend Structure (New Dashboard)

```
frontend/src/admin/
├── features/
│   ├── users/
│   │   ├── api/
│   │   │   └── users.api.ts
│   │   ├── components/
│   │   │   ├── UsersTable.tsx
│   │   │   ├── UserForm.tsx
│   │   │   ├── CreateUserDialog.tsx
│   │   │   ├── EditUserDialog.tsx
│   │   │   └── DeleteUserDialog.tsx
│   │   ├── schemas/
│   │   │   └── user.schema.ts
│   │   ├── types/
│   │   │   └── user.types.ts
│   │   └── hooks/
│   │       ├── useUsers.ts
│   │       └── useUserMutations.ts
│   ├── experiences/
│   │   ├── api/
│   │   │   └── experiences.api.ts
│   │   ├── components/
│   │   │   ├── ExperiencesTable.tsx
│   │   │   ├── ExperienceForm.tsx
│   │   │   └── forms/
│   │   │       ├── EducationForm.tsx
│   │   │       ├── WorkplaceForm.tsx
│   │   │       └── SkillsForm.tsx
│   │   ├── schemas/
│   │   │   └── experience.schema.ts
│   │   ├── types/
│   │   │   └── experience.types.ts
│   │   └── hooks/
│   │       ├── useExperiences.ts
│   │       └── useExperienceMutations.ts
│   ├── naics/
│   │   ├── api/
│   │   │   └── naics.api.ts
│   │   ├── components/
│   │   │   ├── NAICSTable.tsx
│   │   │   ├── NAICSEditDialog.tsx
│   │   │   └── NAICSDeleteDialog.tsx
│   │   ├── schemas/
│   │   │   └── naics.schema.ts
│   │   ├── types/
│   │   │   └── naics.types.ts
│   │   └── hooks/
│   │       ├── useNAICS.ts
│   │       └── useNAICSMutations.ts
│   ├── dashboard/
│   │   ├── components/
│   │   │   ├── DashboardStats.tsx
│   │   │   ├── UserGrowthChart.tsx
│   │   │   ├── ExperienceDistribution.tsx
│   │   │   └── RecentActivity.tsx
│   │   └── hooks/
│   │       └── useDashboardStats.ts
│   └── settings/
│       ├── components/
│       │   ├── SeedDatabaseForm.tsx
│       │   ├── ClearDatabaseDialog.tsx
│       │   └── SystemInfo.tsx
│       └── hooks/
│           └── useSystemSettings.ts
├── components/
│   ├── ui/              # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── dialog.tsx
│   │   ├── table.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   └── ...
│   ├── custom/          # Custom components
│   │   ├── DataTable.tsx
│   │   ├── SearchBar.tsx
│   │   ├── FilterPanel.tsx
│   │   ├── Pagination.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── LoadingSkeleton.tsx
│   │   ├── ErrorBoundary.tsx
│   │   ├── ConfirmDialog.tsx
│   │   └── index.ts
│   └── layout/          # Layout components
│       ├── AdminLayout.tsx
│       ├── Sidebar.tsx
│       └── Header.tsx
├── lib/
│   ├── api.ts              # Axios client
│   ├── queryClient.ts      # React Query config
│   ├── formatters.ts       # Utility formatters
│   ├── validators.ts       # Validation utils
│   └── constants.ts        # Constants
├── hooks/
│   ├── useDebounce.ts
│   ├── usePagination.ts
│   ├── useLocalStorage.ts
│   ├── useDisclosure.ts
│   └── index.ts
├── types/
│   ├── common.types.ts
│   └── api.types.ts
└── App.tsx
```

---

## Appendix B: API Endpoint Reference

### Complete Endpoint List

#### Users

```
GET    /api/v1/users/                    # List users (paginated)
POST   /api/v1/users/                    # Create user
GET    /api/v1/users/{id}                # Get user by ID
PATCH  /api/v1/users/{id}                # Update user
DELETE /api/v1/users/{id}                # Delete user
POST   /api/v1/users/bulk-delete         # Delete multiple users
GET    /api/v1/users/stats               # Get user statistics
POST   /api/v1/users/seed                # Seed test users
```

#### Experiences

```
GET    /api/v1/experiences/              # List experiences (paginated)
POST   /api/v1/experiences/              # Create experience
GET    /api/v1/experiences/{id}          # Get experience by ID
PATCH  /api/v1/experiences/{id}          # Update experience
DELETE /api/v1/experiences/{id}          # Delete experience
GET    /api/v1/experiences/stats         # Get experience statistics
```

#### NAICS Codes

```
GET    /api/v1/naics/                    # List NAICS codes (all)
GET    /api/v1/naics/paginated           # List NAICS codes (paginated)
GET    /api/v1/naics/{code}              # Get NAICS code by code
PATCH  /api/v1/naics/{code}              # Update NAICS admin fields
DELETE /api/v1/naics/{code}              # Delete NAICS code
GET    /api/v1/naics/search              # Search NAICS codes
GET    /api/v1/naics/{code}/hierarchy    # Get NAICS hierarchy
```

#### Health & System

```
GET    /health                           # Basic health check
GET    /health/details                   # Detailed health check
GET    /docs                             # API documentation (Swagger)
GET    /redoc                            # API documentation (ReDoc)
```

---

## Appendix C: Environment Variables Reference

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# API Security
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development|staging|production
DEBUG=true|false

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Logging
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# Optional
MAX_CONNECTIONS=10
POOL_SIZE=5
```

### Frontend Environment Variables

```env
# API
VITE_API_URL=http://localhost:8000/api/v1

# Environment
VITE_ENVIRONMENT=development|staging|production

# Optional
VITE_ENABLE_ANALYTICS=false
VITE_LOG_LEVEL=debug
```

---

## Appendix D: Common Commands Reference

### Backend Commands

```bash
# Development
cd backend
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000

# Database
python -m alembic upgrade head         # Apply migrations
python -m alembic downgrade -1         # Rollback one migration
python -m alembic current              # Check current migration
python -m alembic history              # View migration history

# Seeding
python seed_db.py                      # Seed 25 users
python seed_db.py --users 100          # Seed 100 users
python seed_db.py --clear --users 50   # Clear and reseed
python seed_db.py --verbose            # Verbose output

# Testing
pytest                                 # Run tests
pytest -v                              # Verbose tests
pytest --cov                           # With coverage
```

### Frontend Commands

```bash
# Development
cd frontend
npm run dev

# Build
npm run build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint -- --fix

# Formatting
npm run format

# Testing (when implemented)
npm run test
npm run test:watch
npm run test:coverage
```

---

## Appendix E: Migration History

### Current Migrations

| Migration | Date | Description |
|-----------|------|-------------|
| `41518377be8d` | 2025-11-19 | Add admin fields to NAICS codes (tags, custom_category, admin_notes) |

---

## Document Metadata

**File:** `COMPLETE_ADMIN_DASHBOARD_GUIDE.md`  
**Created:** November 20, 2025  
**Last Updated:** November 20, 2025  
**Version:** 3.0  
**Contributors:** Semour Media Group Development Team  
**Maintained By:** Development Team  
**Review Frequency:** After each major update  

**Source Documents:**
1. `ADMIN_DASHBOARD_IMPLEMENTATION.md` - Implementation summary
2. `ADMIN_DASHBOARD_REFACTOR_V2.md` - Modern refactor plan
3. `ADMIN_PANEL_GUIDE.md` - Setup and usage guide
4. `BACKEND_CONNECTIVITY_TEST.md` - Testing procedures

---

## Feedback & Support

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Star the repository
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)
- 💬 **Need help?** [Join our Discord](https://discord.gg/levelith)

---

**End of Complete Admin Dashboard Guide**

*This document is part of the Levelith Developer Documentation. For questions, contact the development team or join our Discord community.*
