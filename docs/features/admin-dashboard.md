# Admin Dashboard

> **Complete technical documentation for the Levelith admin dashboard covering setup, features, API integration, and deployment.**

**Status:** ✅ Active Development | **Last Updated:** December 8, 2025

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
  - [User Management](#user-management)
  - [Experience Management](#experience-management)
  - [NAICS Code Management](#naics-code-management)
  - [Dashboard Analytics](#dashboard-analytics)
- [Backend API](#backend-api)
- [Frontend](#frontend)
  - [Components](#components)
  - [Hooks](#hooks)
  - [API Client](#api-client)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Levelith admin dashboard is a full-stack application for managing users, experiences, and NAICS industry codes. Built with React (frontend) and FastAPI (backend), it provides complete CRUD operations, pagination, filtering, and analytics.

### Tech Stack

**Frontend:**
- React 18+ with TypeScript
- TanStack Table for data tables
- TanStack Query (React Query) for API state management
- Tailwind CSS for styling
- Axios for HTTP requests
- shadcn/ui component library

**Backend:**
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM
- Alembic for migrations

### Key Features

- ✅ **Full CRUD Operations** - Create, read, update, delete for all entities
- ✅ **Pagination** - Server-side pagination (50-200 items per page)
- ✅ **Search & Filtering** - Real-time search with debouncing
- ✅ **Type Safety** - Full TypeScript support
- ✅ **Analytics** - User statistics and experience distribution
- ✅ **Database Seeding** - Mock data generation for testing

---

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  React Frontend │
│   (TypeScript)  │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│  FastAPI Server │
│    (Python)     │
└────────┬────────┘
         │ SQLAlchemy
         ↓
┌─────────────────┐
│   PostgreSQL    │
│    Database     │
└─────────────────┘
```

### Frontend Architecture

```
frontend/src/admin/
├── features/           # Feature-based modules
│   ├── users/
│   │   ├── api/       # API client methods
│   │   ├── components/# UI components
│   │   ├── hooks/     # Custom hooks
│   │   ├── types/     # TypeScript types
│   │   └── schemas/   # Zod validation schemas
│   ├── experiences/
│   └── naics/
├── components/
│   ├── ui/            # shadcn/ui components
│   └── custom/        # Reusable custom components
├── hooks/             # Shared hooks
└── lib/               # Utilities (API client, etc.)
```

### Backend Architecture

```
backend/
├── api/
│   └── routes/        # FastAPI route handlers
│       ├── users.py
│       ├── experiences.py
│       └── naics.py
├── models/
│   ├── db_models.py   # SQLAlchemy models
│   └── schemas.py     # Pydantic schemas
├── repositories/      # Data access layer
├── services/          # Business logic layer
└── alembic/           # Database migrations
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Free-Columns/levelith-2.git
cd levelith-2
```

### 2. Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations
python -m alembic upgrade head

# Seed database with mock data
python seed_db.py --users 25

# Start backend server
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

API docs at: `http://localhost:8000/docs`

### 3. Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

Admin dashboard at: `http://localhost:5173/admin`

---

## Features

## User Management

**Endpoint:** `/admin/users`

### Features

- ✅ View all users with pagination
- ✅ Search by username or email
- ✅ Filter by active/inactive status
- ✅ Filter by verified/unverified status
- ✅ Create new users
- ✅ Edit user information
- ✅ Delete users (with confirmation)
- ✅ View user statistics

### User Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `username` | String | Unique username |
| `email` | String | Unique email address |
| `password_hash` | String | Bcrypt hashed password |
| `is_active` | Boolean | Account active status |
| `is_verified` | Boolean | Email verified status |
| `profile_data` | JSON | Profile information |
| `created_at` | DateTime | Account creation timestamp |
| `updated_at` | DateTime | Last update timestamp |
| `last_login` | DateTime | Last login timestamp (nullable) |

### Creating a User

```typescript
const newUser = await createUser({
  username: 'johndoe',
  email: 'john@example.com',
  password: 'SecurePass123!',
  isActive: true,
  profile: {
    firstName: 'John',
    lastName: 'Doe',
    bio: 'Software developer',
  },
})
```

---

## Experience Management

**Endpoint:** `/admin/experiences`

### Features

- ✅ View all experiences with pagination
- ✅ Filter by category (Education, Workplace, Skills)
- ✅ Filter by experience type (9 types)
- ✅ Filter by NAICS code
- ✅ Search by title
- ✅ Create polymorphic experiences
- ✅ Edit experiences
- ✅ Delete experiences

### Experience Types

**Education Category:**
- Certificate - Professional certifications
- Degree - Academic degrees (Bachelor's, Master's, PhD)
- Course - Training courses and workshops

**Workplace Category:**
- Gig - Short-term contract work
- Part-Time - Part-time employment
- Full-Time - Full-time employment

**Skills Category:**
- Soft Skills - Communication, leadership, teamwork
- Hard Skills - Technical abilities (programming, tools)
- Native Skills - Language fluency, cultural knowledge

### Experience Fields (Common)

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `user_id` | UUID | Owner user ID |
| `category` | Enum | Education/Workplace/Skills |
| `type` | Enum | Specific type (9 variants) |
| `title` | String | Experience title |
| `description` | Text | Detailed description |
| `naics_code` | String | Industry code (optional) |
| `start_date` | Date | Start date |
| `end_date` | Date | End date (nullable) |
| `is_current` | Boolean | Currently active |
| `metadata` | JSON | Type-specific fields |

### Creating an Experience

```typescript
// Education - Certificate
const cert = await createExperience({
  userId: 'user-id',
  category: 'Education',
  type: 'Certificate',
  title: 'AWS Certified Developer',
  institution: 'Amazon Web Services',
  naicsCode: '541511',
  startDate: '2024-01-01',
  endDate: '2024-03-01',
  credentialId: 'AWS-CERT-12345',
})

// Workplace - Full-Time
const job = await createExperience({
  userId: 'user-id',
  category: 'Workplace',
  type: 'Full-Time',
  title: 'Senior Software Engineer',
  company: 'Tech Corp',
  naicsCode: '541511',
  startDate: '2020-01-01',
  isCurrent: true,
  responsibilities: ['Lead development', 'Code review'],
})
```

---

## NAICS Code Management

**Endpoint:** `/admin/naics`

### Features

- ✅ Browse 2222+ industry codes
- ✅ Server-side pagination (50 per page)
- ✅ Search by code, title, or description
- ✅ Filter by level (2, 3, 4, or 6 digit)
- ✅ Filter by custom category
- ✅ Edit admin fields (tags, category, notes)
- ✅ Delete codes (with warning)
- ✅ View usage statistics

### NAICS Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `code` | String | NAICS code (2-6 digits) |
| `title` | String | Industry title |
| `description` | Text | Industry description |
| `level` | Integer | Code level (2/3/4/6) |
| `parent_code` | String | Parent code (nullable) |
| `tags` | JSON Array | Admin-defined tags |
| `custom_category` | String | Admin category |
| `admin_notes` | Text | Internal notes |
| `is_active` | Boolean | Active status |

### Admin Fields

Only admin-specific fields can be edited. Official NAICS fields (`code`, `title`, `description`) are read-only.

**Editable Fields:**
- `tags` - Array of keywords for organization
- `custom_category` - Your own classification
- `admin_notes` - Internal comments

**Example:**
```typescript
await updateNAICS('541511', {
  tags: ['technology', 'software', 'it'],
  customCategory: 'High-Demand Tech',
  adminNotes: 'Popular code for software development',
})
```

---

## Dashboard Analytics

**Endpoint:** `/admin/dashboard`

### Available Statistics

**User Statistics:**
- Total users
- Active users
- Inactive users
- Verified users
- Recent signups (last 30 days)

**Experience Statistics:**
- Total experiences
- Distribution by category
- Distribution by type
- Recently added experiences

**NAICS Statistics:**
- Total codes
- Distribution by level
- Top categories
- Most used codes

### Fetching Stats

```typescript
const userStats = await getUserStats()
// {
//   totalUsers: 100,
//   activeUsers: 85,
//   verifiedUsers: 60,
//   recentSignups: 12
// }

const expStats = await getExperienceStats()
// {
//   totalExperiences: 450,
//   byCategory: { Education: 150, Workplace: 200, Skills: 100 },
//   recentlyAdded: 23
// }
```

---

## Backend API

### Base URL

Development: `http://localhost:8000/api/v1`
Production: `https://your-backend.onrender.com/api/v1`

### Authentication

Currently, the API does not require authentication. JWT authentication will be added in future versions.

### Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
  "data": [...],
  "total": 100,
  "page": 1,
  "pageSize": 50,
  "totalPages": 2
}
```

**Error Response:**
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

### User Endpoints

```
GET    /api/v1/users              # List users (paginated)
GET    /api/v1/users/{id}         # Get user by ID
POST   /api/v1/users              # Create user
PATCH  /api/v1/users/{id}         # Update user
DELETE /api/v1/users/{id}         # Delete user
GET    /api/v1/users/stats        # User statistics
POST   /api/v1/users/seed         # Seed database
```

### Experience Endpoints

```
GET    /api/v1/experiences         # List experiences (paginated)
GET    /api/v1/experiences/{id}    # Get experience by ID
POST   /api/v1/experiences         # Create experience
PATCH  /api/v1/experiences/{id}    # Update experience
DELETE /api/v1/experiences/{id}    # Delete experience
GET    /api/v1/experiences/stats   # Experience statistics
```

### NAICS Endpoints

```
GET    /api/v1/naics              # List NAICS codes
GET    /api/v1/naics/paginated    # Paginated search with filters
GET    /api/v1/naics/{code}       # Get specific code
PATCH  /api/v1/naics/{code}       # Update admin fields
DELETE /api/v1/naics/{code}       # Delete code (permanent)
GET    /api/v1/naics/stats        # NAICS statistics
```

### Pagination Parameters

All list endpoints support pagination:

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | Integer | 1 | - | Page number (1-indexed) |
| `page_size` | Integer | 50 | 200 | Items per page |
| `search` | String | - | - | Search query |

**Example:**
```bash
curl "http://localhost:8000/api/v1/users?page=1&page_size=20&search=john"
```

---

## Frontend

## Components

### Custom Components

Location: `frontend/src/admin/components/custom/`

#### DataTable

TanStack Table wrapper with sorting, selection, and loading states.

```tsx
import { DataTable } from '@/admin/components/custom'

<DataTable
  columns={columns}
  data={users}
  isLoading={isLoading}
  error={error}
  enableRowSelection
  onRowSelectionChange={setSelected}
/>
```

#### SearchBar

Debounced search input with clear button.

```tsx
import { SearchBar } from '@/admin/components/custom'

<SearchBar
  placeholder="Search users..."
  onSearch={setQuery}
  debounceDelay={500}
/>
```

#### Pagination

Full pagination controls with page size selector.

```tsx
import { Pagination } from '@/admin/components/custom'

<Pagination
  currentPage={page}
  totalPages={totalPages}
  onPageChange={setPage}
  pageSize={pageSize}
  onPageSizeChange={setPageSize}
  totalItems={totalItems}
  showPageSize
/>
```

#### LoadingSpinner & LoadingSkeleton

Loading states for async operations.

```tsx
import { LoadingSpinner, TableSkeleton } from '@/admin/components/custom'

{isLoading ? (
  <TableSkeleton rows={5} columns={4} />
) : (
  <DataTable data={data} columns={columns} />
)}
```

#### ConfirmDialog

Promise-based confirmation dialogs.

```tsx
import { useConfirmDialog } from '@/admin/components/custom'

const confirm = useConfirmDialog()

const handleDelete = async () => {
  const confirmed = await confirm.show({
    title: 'Delete User',
    description: 'Are you sure? This cannot be undone.',
    variant: 'destructive',
  })

  if (confirmed) {
    await deleteUser(id)
  }
}

return <confirm.ConfirmDialog />
```

#### ErrorBoundary

React error boundary for graceful error handling.

```tsx
import { ErrorBoundary } from '@/admin/components/custom'

<ErrorBoundary>
  <MyComponent />
</ErrorBoundary>
```

---

## Hooks

### Custom Hooks

Location: `frontend/src/admin/hooks/`

#### useDebounce

Delay updating a value for optimization.

```typescript
import { useDebounce } from '@/admin/hooks'

const [search, setSearch] = useState('')
const debouncedSearch = useDebounce(search, 500)

useEffect(() => {
  fetchResults(debouncedSearch)
}, [debouncedSearch])
```

#### usePagination

Manage pagination state.

```typescript
import { usePagination } from '@/admin/hooks'

const pagination = usePagination(totalItems, 20)

<Pagination
  currentPage={pagination.page}
  totalPages={pagination.totalPages}
  onPageChange={pagination.setPage}
  pageSize={pagination.pageSize}
  onPageSizeChange={pagination.setPageSize}
/>
```

#### useLocalStorage

Type-safe localStorage with cross-tab sync.

```typescript
import { useLocalStorage } from '@/admin/hooks'

const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light')

<button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
  Toggle Theme
</button>
```

#### useDisclosure

Manage open/close state for modals, dropdowns, etc.

```typescript
import { useDisclosure } from '@/admin/hooks'

const modal = useDisclosure()

<button onClick={modal.open}>Open Modal</button>
{modal.isOpen && <Modal onClose={modal.close}>...</Modal>}
```

---

## API Client

### API Methods

Location: `frontend/src/admin/features/*/api/`

#### User API

```typescript
import * as UsersAPI from '@/admin/features/users/api/users.api'

// List users
const users = await UsersAPI.getUsers({ page: 1, pageSize: 20 })

// Get user by ID
const user = await UsersAPI.getUserById('user-id')

// Create user
const newUser = await UsersAPI.createUser({
  username: 'johndoe',
  email: 'john@example.com',
  password: 'SecurePass123!',
})

// Update user
const updated = await UsersAPI.updateUser('user-id', {
  isActive: false,
})

// Delete user
await UsersAPI.deleteUser('user-id')

// Get statistics
const stats = await UsersAPI.getUserStats()
```

#### Experience API

```typescript
import * as ExperiencesAPI from '@/admin/features/experiences/api/experiences.api'

// List experiences
const experiences = await ExperiencesAPI.getExperiences({
  category: 'Education',
  page: 1,
})

// Create experience
const newExp = await ExperiencesAPI.createExperience({
  userId: 'user-id',
  category: 'Education',
  type: 'Certificate',
  title: 'AWS Certified Developer',
})
```

#### NAICS API

```typescript
import * as NAICSAPI from '@/admin/features/naics/api/naics.api'

// List NAICS codes
const codes = await NAICSAPI.getNAICSCodes({
  search: 'software',
  level: 6,
  page: 1,
})

// Update NAICS
const updated = await NAICSAPI.updateNAICS('541511', {
  tags: ['tech', 'software'],
  customCategory: 'IT Services',
})
```

### With React Query

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

function UsersList() {
  // Query
  const { data, isLoading } = useQuery({
    queryKey: ['users', { page: 1 }],
    queryFn: () => UsersAPI.getUsers({ page: 1 }),
  })

  // Mutation
  const queryClient = useQueryClient()
  const createUser = useMutation({
    mutationFn: UsersAPI.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  return <DataTable data={data?.data} columns={columns} isLoading={isLoading} />
}
```

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id VARCHAR(32) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    profile_data JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

### Experiences Table

```sql
CREATE TABLE experiences (
    id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    naics_code VARCHAR(6),
    start_date DATE NOT NULL,
    end_date DATE NULL,
    is_current BOOLEAN DEFAULT FALSE,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_experiences_user_id ON experiences(user_id);
CREATE INDEX idx_experiences_category ON experiences(category);
CREATE INDEX idx_experiences_naics_code ON experiences(naics_code);
```

### NAICS Codes Table

```sql
CREATE TABLE naics_codes (
    id VARCHAR(32) PRIMARY KEY,
    code VARCHAR(6) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    level INTEGER NOT NULL,
    parent_code VARCHAR(6),
    tags JSON DEFAULT '[]',
    custom_category VARCHAR(100),
    admin_notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_naics_code ON naics_codes(code);
CREATE INDEX idx_naics_level ON naics_codes(level);
```

### Migrations

Run migrations with Alembic:

```bash
cd backend

# Apply all migrations
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "Description"

# Rollback one migration
python -m alembic downgrade -1
```

---

## Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_create_user
```

### Frontend Testing

```bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e
```

### Manual Testing Checklist

#### Users Feature

- [ ] List users loads with pagination
- [ ] Search filters results
- [ ] Status filter works (active/inactive)
- [ ] Verified filter works
- [ ] Create user form validates
- [ ] Create user succeeds
- [ ] Edit user updates correctly
- [ ] Delete user with confirmation
- [ ] Pagination controls work
- [ ] User stats display correctly

#### Experiences Feature

- [ ] List experiences loads
- [ ] Category filter works
- [ ] Type filter works
- [ ] NAICS filter works
- [ ] Create experience form validates
- [ ] Polymorphic fields show correctly
- [ ] Edit experience updates
- [ ] Delete experience works

#### NAICS Feature

- [ ] List NAICS codes loads
- [ ] Search NAICS works
- [ ] Level filter works
- [ ] Edit modal opens
- [ ] Tags save correctly
- [ ] Custom category saves
- [ ] Admin notes save
- [ ] Delete confirmation works

---

## Deployment

### Backend Deployment (Render)

1. **Create Web Service**
   - Connect GitHub repository
   - Select `backend/` directory
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   ENVIRONMENT=production
   DEBUG=false
   CORS_ORIGINS=["https://your-frontend.com"]
   ```

3. **Apply Migrations**
   ```bash
   python -m alembic upgrade head
   ```

### Frontend Deployment (Vercel/Netlify)

1. **Build Configuration**
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: 18

2. **Environment Variables**
   ```
   VITE_API_URL=https://your-backend.onrender.com/api/v1
   ```

3. **Deploy**
   ```bash
   npm run build
   vercel --prod
   ```

### Database Seeding (Production)

```bash
# Connect to production database
export DATABASE_URL="postgresql://..."

# Seed with limited data
python backend/seed_db.py --users 10

# Verify
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

---

## Troubleshooting

### Backend Issues

#### Database Connection Failed

**Symptoms:** Cannot connect to PostgreSQL

**Solutions:**
- Check `DATABASE_URL` in `.env`
- Verify database is running
- Test connection: `psql $DATABASE_URL`
- Check firewall/network settings

#### Module Not Found

**Symptoms:** Python import errors

**Solutions:**
```bash
pip install -r backend/requirements.txt
```

#### Migration Conflicts

**Symptoms:** Alembic migration errors

**Solutions:**
```bash
# Check current version
python -m alembic current

# Rollback and reapply
python -m alembic downgrade -1
python -m alembic upgrade head
```

### Frontend Issues

#### CORS Errors

**Symptoms:** Browser blocks API requests

**Solutions:**
Update `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```
Restart backend.

#### API Not Found

**Symptoms:** 404 errors on API calls

**Solutions:**
- Verify `VITE_API_URL` in `.env`
- Check backend is running
- Test API: `curl http://localhost:8000/health`

#### Components Not Rendering

**Symptoms:** Blank pages or missing data

**Solutions:**
- Check browser console for errors
- Verify API responses in Network tab
- Check React Query DevTools
- Ensure proper error boundaries

### Database Issues

#### Unique Constraint Violation

**Symptoms:** Cannot create user with duplicate username/email

**Solutions:**
- Use unique values
- Or delete existing user
- Or clear database: `python seed_db.py --clear`

#### Missing Columns

**Symptoms:** SQL errors about missing columns

**Solutions:**
```bash
# Apply latest migrations
python -m alembic upgrade head

# Verify schema
psql $DATABASE_URL -c "\d users"
```

---

## Additional Resources

### Related Documentation

- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Database Guide](/docs/backend/database/DATABASE_OVERVIEW.md)
- [MVP Guide](/MVP_GUIDE.md)
- [Deployment Guide](/RENDER_XP_DEPLOYMENT.md)

### External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TanStack Table](https://tanstack.com/table/latest)
- [TanStack Query](https://tanstack.com/query/latest)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated:** December 8, 2025 | **Version:** 3.0 | **Maintained By:** Semour Media Group
