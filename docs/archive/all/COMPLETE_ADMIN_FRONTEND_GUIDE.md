

# Admin Dashboard – Frontend Master Guide ✅

**Date:** November 20, 2025  
**Author:** Semour Media Group  
**Version:** 1.0  
**Category:** Frontend  
**Difficulty:** 🟡 Intermediate  
**Reading Time:** ~90 minutes  

---

## 📌 Table of Contents

1. [Infrastructure Overview](#infrastructure-overview)  
2. [Technology Stack](#technology-stack)  
3. [Folder Structure](#folder-structure)  
4. [Architecture Principles](#architecture-principles)  
5. [API Client Guide](#api-client-guide)  
   - Users API  
   - Experiences API  
   - NAICS API  
   - Error Handling & Best Practices  
6. [Components Guide](#components-guide)  
   - DataTable, SearchBar, FilterPanel, Pagination  
   - Loading states, ErrorBoundary, ConfirmDialog  
   - Form Components (FormButton, FormInput, FormTextarea)  
7. [Hooks Guide](#hooks-guide)  
   - useDebounce, usePagination, useLocalStorage, useDisclosure  
8. [Common Patterns](#common-patterns)  
9. [Troubleshooting](#troubleshooting)  
10. [Next Steps](#next-steps)  
11. [Related Documentation](#related-documentation)  

---

## 1. Infrastructure Overview

The admin dashboard frontend was built in **two phases**:

- **Phase 0:** Setup, configuration, types, schemas, utilities  
- **Phase 1:** API clients, hooks, reusable components  

**Goals Achieved:**
- ✅ TypeScript configuration with path aliases  
- ✅ ESLint + Prettier setup  
- ✅ Feature-based folder structure  
- ✅ Type definitions for backend entities  
- ✅ Zod validation schemas  
- ✅ Utility functions (formatters, validators, constants)  
- ✅ API client methods for all endpoints  
- ✅ Custom React hooks  
- ✅ Reusable UI components  

---

## 2. Technology Stack

- **React 18+** – UI library  
- **TypeScript 5+** – Type safety  
- **Vite 5+** – Build tool  
- **Tailwind CSS 3+** – Styling  
- **React Query 5+** – Server state management  
- **TanStack Table 8+** – Data tables  
- **Axios 1.6+** – HTTP client  
- **React Hook Form + Zod** – Forms & validation  
- **Radix UI, Lucide React, Sonner, date-fns** – UI primitives, icons, notifications, date utilities  
- **ESLint + Prettier** – Code quality  

---

## 3. Folder Structure

```
frontend/src/admin/
├── features/
│   ├── users/
│   ├── experiences/
│   ├── naics/
│   ├── dashboard/
│   └── settings/
├── components/
│   ├── ui/
│   ├── custom/
│   └── forms/
├── hooks/
├── lib/
└── types/
```

---

## 4. Architecture Principles

- **Feature-based organization** – Each feature self-contained  
- **Type safety first** – Full TypeScript coverage  
- **Composition over configuration** – Small, composable components  
- **Accessibility first** – WCAG compliance  
- **Performance optimized** – Caching, debouncing, lazy loading  

---

## 5. API Client Guide

### Users API
- `getUsers` – Paginated list with filters  
- `getUserById` – Fetch single user  
- `createUser` – Create new user  
- `updateUser` – Update existing user  
- `deleteUser` – Delete user  
- `getUserStats` – Statistics  
- `bulkDeleteUsers` – Batch delete  

### Experiences API
- Polymorphic CRUD across **Education, Workplace, Skills**  
- `getExperiences`, `getExperienceById`, `getExperiencesByUser`  
- `createExperience`, `updateExperience`, `deleteExperience`  
- `getExperienceStats`, `bulkDeleteExperiences`  

### NAICS API
- `getNAICSCodes`, `getNAICSById`, `getNAICSByCode`  
- `searchNAICS`, `getNAICSHierarchy`  
- `createNAICS`, `updateNAICS`, `deleteNAICS`  
- `getNAICSStats`  

### Error Handling
- Centralized interceptors  
- Try/catch with toast notifications  
- React Query `onError` callbacks  

---

## 6. Components Guide

### Core Components
- **DataTable** – TanStack Table wrapper  
- **SearchBar** – Debounced search input  
- **FilterPanel** – Collapsible filters  
- **Pagination** – Full pagination controls  

### Loading & Error
- **LoadingSpinner** – Inline, overlay, sizes  
- **LoadingSkeleton** – Table, card, form, stats skeletons  
- **ErrorBoundary** – Catch rendering errors  

### Confirmation
- **ConfirmDialog** – Promise-based confirmation modals  

### Form Components
- **FormButton** – Primary, secondary, danger variants  
- **FormInput** – Input with label, validation, error display  
- **FormTextarea** – Textarea with label, validation  

---

## 7. Hooks Guide

- **useDebounce** – Delay updates (search optimization)  
- **usePagination** – Manage pagination state  
- **useLocalStorage** – Persistent state with sync  
- **useDisclosure** – Open/close state for modals, dropdowns  

---

## 8. Common Patterns

- **CRUD Table** – DataTable + SearchBar + Pagination + ConfirmDialog  
- **Filtered List** – SearchBar + FilterPanel + DataTable  
- **Debounced Search with Pagination** – useDebounce + usePagination + DataTable  
- **Persisted Filter State** – useLocalStorage + FilterPanel  
- **Multi-Step Form with Persistence** – useLocalStorage across steps  

---

## 9. Troubleshooting

- **DataTable not sorting** – Ensure `enableSorting` enabled  
- **SearchBar not debouncing** – Check `debounceDelay` and memoized callback  
- **ConfirmDialog not showing** – Ensure `<confirm.ConfirmDialog />` rendered  
- **Skeleton flashing** – Add minimum loading time  
- **useDebounce not working** – Use debounced value, not original  
- **usePagination out of bounds** – Ensure `totalItems` correct  
- **useLocalStorage not syncing** – Same key across tabs  
- **useDisclosure not resetting** – Reset state on unmount  

---

## 10. Next Steps

- **Phase 2:** Users CRUD interface (table, forms, stats, bulk ops)  
- **Phase 3:** Experiences CRUD (9 forms, NAICS integration, timeline)  
- **Phase 4:** NAICS browsing/editing (hierarchy, tags, categories)  
- **Phase 5–8:** Dashboard, settings, routing, production polish  

---

## 11. Related Documentation

- **Components Guide** – UI components reference  
- **Hooks Guide** – Custom hooks documentation  
- **API Client Guide** – API methods and usage  
- **Refactor Plan (ADMIN_DASHBOARD_REFACTOR_V2.md)** – Implementation roadmap  
- **MANIFEST.md** – Project vision and conventions  

---

## 🎉 Summary

This **master guide** merges infrastructure, API clients, components, and hooks into one cohesive reference. It provides:

- ✅ Complete overview of frontend architecture  
- ✅ Type-safe API client methods  
- ✅ Reusable UI components  
- ✅ Custom hooks for state management  
- ✅ Best practices, patterns, troubleshooting  

**Status:** Production-ready foundation for Admin Dashboard 🚀  
