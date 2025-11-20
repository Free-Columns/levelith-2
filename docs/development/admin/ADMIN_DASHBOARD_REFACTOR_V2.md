# Admin Dashboard Refactor V2 - Complete Migration Plan

**Status:** 📋 Planning Phase
**Strategy:** Plan C - Modern Stack Complete Rebuild
**Timeline:** 20-30 hours
**Risk Level:** High (Complete rewrite)
**Last Updated:** 2025-11-20

---

## Executive Summary

Complete rebuild of admin dashboard (`frontend/src/admin/`) using modern 2025 best practices:
- **TypeScript** everywhere (full type safety)
- **React Query** for API state management
- **TanStack Table** for advanced data tables
- **React Hook Form + Zod** for type-safe forms
- **Tailwind CSS** for styling (replacing inline styles)
- **shadcn/ui** component library
- **Remove ALL mock data** (server-only)
- **Fix routing** to use `/admin/*` prefix

---

## 🎯 Goals

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

## 📊 Migration Phases

### Phase 0: Preparation & Setup (2-3 hours)
**Goal:** Set up infrastructure, install dependencies, create folder structure

#### Tasks (15 total)
1. [] Install new dependencies (see dependency list below)
2. [] Configure TypeScript (`tsconfig.json`)
3. [] Set up Tailwind CSS
4. [] Install shadcn/ui CLI and components
5. [] Configure React Query client
6. [] Set up Vite for `/admin` base path
7. [] Create new feature-based folder structure
8. [] Set up path aliases in `tsconfig.json`
9. [] Configure ESLint for TypeScript
10. [] Set up Prettier with Tailwind plugin
11. [] Create type definition files for backend API
12. [] Set up Zod schemas for all entities
13. [] Create utility functions (cn, formatters, etc.)
14. [] Configure build for production deployment
15. [] Create migration checklist tracking system

**Dependencies to Install:**
```json
{
  "dependencies": {
    "@tanstack/react-query": "^5.17.0",
    "@tanstack/react-table": "^8.11.0",
    "react-hook-form": "^7.49.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "tailwindcss": "^3.4.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.303.0",
    "sonner": "^1.3.0",
    "date-fns": "^3.0.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-toast": "^1.1.5"
  }
}
```

---

### Phase 1: Core Infrastructure (3-4 hours)
**Goal:** Build reusable foundation (API client, React Query setup, base components)

#### Tasks (20 total)
1. [] Create TypeScript API client (`lib/api.ts`)
2. [] Set up React Query with providers
3. [] Install shadcn/ui base components (button, input, dialog, table, etc.)
4. [] Create custom DataTable wrapper for TanStack Table
5. [] Build SearchBar component
6. [] Build FilterPanel component
7. [] Build Pagination component
8. [] Build LoadingSpinner component
9. [] Build ErrorBoundary component
10. [] Create toast notification system
11. [] Build ConfirmDialog component
12. [] Create utility hooks (useDebounce, usePagination)
13. [] Create formatters (date, currency, etc.)
14. [] Create validators
15. [] Set up error handling utilities
16. [] Create constants file (enums, config)
17. [] Build AuthProvider (if needed)
18. [] Create route guards
19. [] Set up layout components
20. [] Test all base components

---

### Phase 2: Users Feature (4-5 hours)
**Goal:** Complete CRUD for users with search/filter/pagination

#### Tasks (25 total)
1. [] Create user types (`features/users/types/user.types.ts`)
2. [] Create user Zod schemas (`features/users/schemas/user.schema.ts`)
3. [] Build user API queries (`features/users/api/users.queries.ts`)
4. [] Build user API mutations (`features/users/api/users.mutations.ts`)
5. [] Create useUsers custom hook
6. [] Build UsersTable component with TanStack Table
7. [] Add search functionality to UsersTable
8. [] Add filter dropdowns (active/inactive/verified)
9. [] Add pagination to UsersTable
10. [] Add sorting to UsersTable
11. [] Build UserForm component (create/edit)
12. [] Add form validation with Zod + React Hook Form
13. [] Build CreateUserDialog
14. [] Build EditUserDialog
15. [] Build DeleteUserDialog with confirmation
16. [] Add loading states to all operations
17. [] Add error handling with toast notifications
18. [] Add optimistic updates for mutations
19. [] Build UserStats widget (active/inactive counts)
20. [] Add user avatar display
21. [] Add user status badges
22. [] Add action dropdown menu per row
23. [] Test create user flow
24. [] Test edit user flow
25. [] Test delete user flow

---

### Phase 3: Experiences Feature (5-6 hours)
**Goal:** Complete CRUD for all 9 experience types with advanced filtering

#### Tasks (30 total)
1. [] Create experience types for all 9 variants
2. [] Create experience Zod schemas (polymorphic)
3. [] Build experience API queries
4. [] Build experience API mutations
5. [] Create useExperiences custom hook
6. [] Build ExperiencesTable component
7. [] Add category filter (Education/Workplace/Skills)
8. [] Add type filter (9 specific types)
9. [] Add NAICS code filter
10. [] Add date range filter
11. [] Add search by title/description
12. [] Add pagination
13. [] Add sorting by multiple columns
14. [] Build ExperienceForm component
15. [] Implement dynamic form fields based on type
16. [] Add certificate-specific fields
17. [] Add degree-specific fields
18. [] Add course-specific fields
19. [] Add gig-specific fields
20. [] Add part-time-specific fields
21. [] Add full-time-specific fields
22. [] Add soft-skill-specific fields
23. [] Add hard-skill-specific fields
24. [] Add native-skill-specific fields
25. [] Integrate NAICS code selector
26. [] Add skills-gained multi-select
27. [] Build CreateExperienceDialog
28. [] Build EditExperienceDialog
29. [] Build DeleteExperienceDialog
30. [] Test all 9 experience type flows

---

### Phase 4: NAICS Feature (3-4 hours)
**Goal:** NAICS browsing with tag/category editing

#### Tasks (20 total)
1. [] Create NAICS types
2. [] Create NAICS Zod schemas
3. [] Build NAICS API queries (paginated)
4. [] Build NAICS API mutations (update tags/category)
5. [] Create useNAICS custom hook
6. [] Build NAICSTable component
7. [] Add server-side search
8. [] Add category filter
9. [] Add level filter (2/3/4/6 digit)
10. [] Add pagination (50 per page)
11. [] Display tags column
12. [] Build NAICSEditDialog
13. [] Add TagInput component for tags
14. [] Add custom category input
15. [] Add admin notes textarea
16. [] Add save functionality
17. [] Build DeleteNAICSDialog with warning
18. [] Add NAICS code badge styling
19. [] Add industry color coding
20. [] Test NAICS edit/delete flows

---

### Phase 5: Dashboard & Analytics (2-3 hours)
**Goal:** Overview dashboard with statistics and charts

#### Tasks (15 total)
1. [] Create dashboard types
2. [] Build stats API queries
3. [] Create useDashboard hook
4. [] Build StatsCard component
5. [] Display total users stat
6. [] Display active users stat
7. [] Display total experiences stat
8. [] Build user growth chart (recharts)
9. [] Build experience distribution chart
10. [] Build NAICS industry chart
11. [] Build recent activity feed
12. [] Add quick action buttons
13. [] Add refresh functionality
14. [] Add loading states
15. [] Add empty states

---

### Phase 6: Settings & Utilities (2 hours)
**Goal:** Settings page with database seeding

#### Tasks (10 total)
1. [] Build Settings page layout
2. [] Add seed database form
3. [] Add user count input (default 50)
4. [] Add seed button with loading state
5. [] Add seed API mutation
6. [] Display seed statistics after completion
7. [] Add environment info display
8. [] Add API base URL display
9. [] Add clear cache button (React Query)
10. [] Add about/version info

---

### Phase 7: Routing & Layout (1-2 hours)
**Goal:** Fix routing with `/admin` prefix, proper layouts

#### Tasks (12 total)
1. [] Update App.tsx with `/admin` base route
2. [] Update all navigation links to include `/admin`
3. [] Create AdminLayout with sidebar
4. [] Add navigation menu
5. [] Add breadcrumbs
6. [] Add user menu in header
7. [] Add logout functionality
8. [] Create login page (if needed)
9. [] Add route guards for authentication
10. [] Add 404 page
11. [] Configure Vite base path
12. [] Test all routes

---

### Phase 8: Polish & Production (2-3 hours)
**Goal:** Error handling, loading states, responsive design, deployment

#### Tasks (18 total)
1. [] Add comprehensive error boundaries
2. [] Add loading skeletons for all tables
3. [] Add empty states for all lists
4. [] Test responsive design on mobile
5. [] Test responsive design on tablet
6. [] Add keyboard shortcuts
7. [] Add accessibility labels
8. [] Test screen reader compatibility
9. [] Add rate limiting UI feedback
10. [] Add offline detection
11. [] Configure production build
12. [] Optimize bundle size
13. [] Add source maps
14. [] Configure deployment to admin.levelith.online
15. [] Test production build locally
16. [] Deploy to staging
17. [] Smoke test on staging
18. [] Deploy to production

---

## 🗂️ New Folder Structure

```
frontend/src/admin/
├── features/                    # Feature-based organization
│   ├── users/
│   │   ├── api/
│   │   │   ├── users.queries.ts      # React Query hooks
│   │   │   └── users.mutations.ts    # Mutation hooks
│   │   ├── components/
│   │   │   ├── UsersTable.tsx        # Main table
│   │   │   ├── UserForm.tsx          # Create/edit form
│   │   │   ├── UserFilters.tsx       # Filter panel
│   │   │   ├── UserStats.tsx         # Stats widget
│   │   │   └── UserActions.tsx       # Action dropdown
│   │   ├── schemas/
│   │   │   └── user.schema.ts        # Zod validation
│   │   ├── types/
│   │   │   └── user.types.ts         # TypeScript types
│   │   └── hooks/
│   │       └── useUsers.ts           # Custom hook
│   ├── experiences/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── ExperiencesTable.tsx
│   │   │   ├── ExperienceForm.tsx
│   │   │   ├── ExperienceFilters.tsx
│   │   │   ├── ExperienceTypeSelector.tsx
│   │   │   └── forms/
│   │   │       ├── CertificateForm.tsx
│   │   │       ├── DegreeForm.tsx
│   │   │       ├── CourseForm.tsx
│   │   │       ├── GigForm.tsx
│   │   │       ├── PartTimeForm.tsx
│   │   │       ├── FullTimeForm.tsx
│   │   │       ├── SoftSkillForm.tsx
│   │   │       ├── HardSkillForm.tsx
│   │   │       └── NativeSkillForm.tsx
│   │   ├── schemas/
│   │   ├── types/
│   │   └── hooks/
│   ├── naics/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── NAICSTable.tsx
│   │   │   ├── NAICSEditDialog.tsx
│   │   │   ├── NAICSFilters.tsx
│   │   │   └── NAICSBadge.tsx
│   │   ├── schemas/
│   │   ├── types/
│   │   └── hooks/
│   ├── dashboard/
│   │   ├── components/
│   │   │   ├── StatsCard.tsx
│   │   │   ├── UserGrowthChart.tsx
│   │   │   ├── ExperienceDistributionChart.tsx
│   │   │   └── RecentActivity.tsx
│   │   └── hooks/
│   │       └── useDashboard.ts
│   └── settings/
│       ├── components/
│       │   ├── SeedDatabaseForm.tsx
│       │   └── EnvironmentInfo.tsx
│       └── hooks/
├── components/                  # Shared components
│   ├── ui/                      # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── select.tsx
│   │   ├── table.tsx
│   │   ├── toast.tsx
│   │   ├── form.tsx
│   │   ├── label.tsx
│   │   ├── badge.tsx
│   │   ├── card.tsx
│   │   ├── separator.tsx
│   │   └── ... (50+ components)
│   ├── custom/
│   │   ├── DataTable.tsx        # Wrapper for TanStack Table
│   │   ├── SearchBar.tsx        # Reusable search
│   │   ├── FilterPanel.tsx      # Reusable filters
│   │   ├── Pagination.tsx       # Reusable pagination
│   │   ├── LoadingSpinner.tsx   # Loading states
│   │   ├── ErrorBoundary.tsx    # Error handling
│   │   ├── ConfirmDialog.tsx    # Confirmation modals
│   │   └── TagInput.tsx         # Tag input field
│   └── layout/
│       ├── AdminLayout.tsx      # Main layout
│       ├── Sidebar.tsx          # Navigation sidebar
│       ├── Header.tsx           # Top header
│       └── Breadcrumbs.tsx      # Breadcrumb navigation
├── lib/                         # Utilities
│   ├── api.ts                   # Axios instance + config
│   ├── queryClient.ts           # React Query config
│   ├── utils.ts                 # Helper functions (cn, etc.)
│   ├── formatters.ts            # Date, currency formatters
│   ├── validators.ts            # Validation helpers
│   └── constants.ts             # App-wide constants
├── hooks/                       # Shared hooks
│   ├── useDebounce.ts
│   ├── usePagination.ts
│   └── useAuth.ts
├── types/                       # Global types
│   ├── api.types.ts
│   └── common.types.ts
├── App.tsx                      # Main app component
├── main.tsx                     # Entry point
└── index.css                    # Tailwind imports
```

---

## 🔧 Configuration Files

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/admin/*": ["./src/admin/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### tailwind.config.js
```javascript
module.exports = {
  content: [
    "./src/admin/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#007EA7",
        secondary: "#088732",
        accent: "#e74c3c",
        // ... ONETRUTH colors
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

---

## 📝 Inline TODO Format

All inline TODOs follow this format:

```typescript
// AdminDashboardRefactorv2: [ACTION] - [DESCRIPTION]
// What: [What needs to happen]
// Why: [Reason for the change]
// Risk: [What could go wrong]
// Phase: [Phase number from plan]
// Complexity: [Low/Medium/High]
// Depends: [Dependencies, if any]
```

**Example:**
```typescript
// AdminDashboardRefactorv2: REPLACE - Convert to TypeScript with React Query
// What: Rename DataSourceContext.jsx → useUsersQuery.ts, replace with React Query
// Why: Eliminate mock data, get automatic caching/refetching, type safety
// Risk: Breaking change - all components using this context need updating
// Phase: 2 (Users Feature)
// Complexity: Medium
// Depends: Phase 1 (React Query setup)
```

---

## ⚠️ Migration Risks & Mitigation

### Risk 1: Complete Rewrite Breaking Changes
**Risk Level:** High
**Impact:** All existing code needs replacement
**Mitigation:**
- Keep old code in `_deprecated/` for reference
- Migrate feature-by-feature (users → experiences → NAICS)
- Test each feature thoroughly before moving to next
- Create rollback plan

### Risk 2: Type System Learning Curve
**Risk Level:** Medium
**Impact:** Slower initial development
**Mitigation:**
- Start with simple types, add complexity gradually
- Use `any` temporarily if stuck, refine later
- Leverage TypeScript autocomplete
- Reference shadcn/ui source code for examples

### Risk 3: New Dependencies Introduction
**Risk Level:** Medium
**Impact:** Bundle size increase, potential conflicts
**Mitigation:**
- Monitor bundle size with vite-bundle-visualizer
- Use tree-shaking compatible libraries
- Lazy load heavy components
- Regular dependency audits

### Risk 4: Data Loss During Testing
**Risk Level:** Low
**Impact:** Test data corruption
**Mitigation:**
- Use separate staging database
- Implement database backup before testing
- Use seed data for development
- Never test on production

### Risk 5: Deployment Configuration
**Risk Level:** Medium
**Impact:** Admin dashboard not accessible after deploy
**Mitigation:**
- Test build locally first
- Deploy to staging environment
- Verify `/admin/*` routing works
- Document deployment process

---

## 🎯 Success Criteria

### Definition of Done - Each Phase
- [] All tasks completed
- [] TypeScript compilation successful (0 errors)
- [] ESLint passes (0 errors, minimal warnings)
- [] Components render without errors
- [] API integration tested
- [] Loading states functional
- [] Error handling tested
- [] Responsive design verified
- [] Documentation updated

### Definition of Done - Complete Project
- [] All 8 phases completed
- [] All mock data removed
- [] Full TypeScript coverage
- [] All CRUD operations functional
- [] Search/filtering on all tables
- [] NAICS tag/category editing working
- [] Seed database form functional
- [] Production build successful
- [] Deployed to admin.levelith.online
- [] Smoke tests passing
- [] Documentation complete

---

## 📚 Reference Documentation

### Dependency Documentation
- [TanStack Query](https://tanstack.com/query/latest)
- [TanStack Table](https://tanstack.com/table/latest)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Radix UI](https://www.radix-ui.com/)

### Internal Documentation
- [MANIFEST.md](../../agent/MANIFEST.md) - Project vision
- [AI_AGENT_GOLDEN_RULES.md](../../agent/AI_AGENT_GOLDEN_RULES.md) - Development rules
- [ADMIN_PANEL_GUIDE.md](./ADMIN_PANEL_GUIDE.md) - Current admin guide (to be updated)
- [API_DOCUMENTATION.md](../../api/API_DOCUMENTATION.md) - Backend API reference

---

## 🔄 Migration Strategy

### Step-by-Step Migration

**Week 1: Foundation**
- Day 1-2: Phase 0 (Setup)
- Day 3-4: Phase 1 (Infrastructure)
- Day 5: Testing & validation

**Week 2: Core Features**
- Day 1-2: Phase 2 (Users)
- Day 3-4: Phase 3 (Experiences)
- Day 5: Testing & validation

**Week 3: Polish & Deploy**
- Day 1-2: Phase 4 (NAICS)
- Day 3: Phase 5 (Dashboard)
- Day 4: Phases 6-7 (Settings, Routing)
- Day 5: Phase 8 (Production)

### Rollback Plan
If migration fails catastrophically:
1. Revert to `_deprecated/levelith_admin_dashboard_OLD`
2. Copy back to `dev/dev-frontend/levelith_admin_dashboard`
3. Redeploy old version
4. Document what went wrong
5. Plan fixes before retry

---

## 📊 Progress Tracking

| Phase | Tasks | Completed | Status | ETA |
|-------|-------|-----------|--------|-----|
| Phase 0: Setup | 15 | 0 | ⏸️ Not Started | 2-3 hrs |
| Phase 1: Infrastructure | 20 | 0 | ⏸️ Not Started | 3-4 hrs |
| Phase 2: Users | 25 | 0 | ⏸️ Not Started | 4-5 hrs |
| Phase 3: Experiences | 30 | 0 | ⏸️ Not Started | 5-6 hrs |
| Phase 4: NAICS | 20 | 0 | ⏸️ Not Started | 3-4 hrs |
| Phase 5: Dashboard | 15 | 0 | ⏸️ Not Started | 2-3 hrs |
| Phase 6: Settings | 10 | 0 | ⏸️ Not Started | 2 hrs |
| Phase 7: Routing | 12 | 0 | ⏸️ Not Started | 1-2 hrs |
| Phase 8: Production | 18 | 0 | ⏸️ Not Started | 2-3 hrs |
| **TOTAL** | **165** | **0** | ⏸️ **Not Started** | **25-33 hrs** |

---

## 🚀 Quick Start Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Lint
npm run lint

# Format
npm run format
```

---

**Last Updated:** 2025-11-20
**Document Owner:** Development Team
**Review Frequency:** After each phase completion
