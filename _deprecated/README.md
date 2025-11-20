# Deprecated Admin Dashboard

**Status:** 🔴 DEPRECATED - Do Not Use
**Moved Date:** November 20, 2025
**Reason:** Replaced by Plan C refactor (Modern Stack rebuild)

---

## Why This Was Moved

This admin dashboard (`levelith_admin_dashboard_OLD/`) was the original implementation located at `dev/dev-frontend/levelith_admin_dashboard/`. It has been deprecated and moved to `_deprecated/` as part of the **AdminDashboardRefactorv2** initiative.

### Problems with Old Dashboard
1. ❌ JavaScript only (no TypeScript type safety)
2. ❌ Manual state management (no React Query)
3. ❌ Mock data switching (LOCAL/SERVER modes)
4. ❌ Custom components (no component library)
5. ❌ Inline styles (no Tailwind CSS)
6. ❌ Manual form handling (no React Hook Form + Zod)
7. ❌ Basic tables (no TanStack Table features)
8. ❌ No proper error handling or loading states

### New Dashboard Location

The new admin dashboard is being built at:
```
frontend/src/admin/
```

It is a complete rewrite using modern best practices (Plan C):
- ✅ TypeScript everywhere
- ✅ React Query for API state management
- ✅ TanStack Table for advanced tables
- ✅ React Hook Form + Zod for type-safe forms
- ✅ Tailwind CSS for styling
- ✅ shadcn/ui component library
- ✅ Server-only (no mock data)
- ✅ Proper error boundaries and loading states

---

## Migration Status

See [ADMIN_DASHBOARD_REFACTOR_V2.md](../docs/development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md) for complete migration plan.

**Current Phase:** Planning (Phase 0)

---

## Can I Use This Old Dashboard?

**NO.** This dashboard is deprecated and will not receive updates. It is kept for reference only.

If you need to reference the old implementation:
- Location: `_deprecated/levelith_admin_dashboard_OLD/`
- Last working state: Before November 20, 2025
- Note: May have bugs and broken features

---

## What If I Need to Rollback?

If the new dashboard migration fails catastrophically, you can temporarily restore this:

```bash
# Emergency rollback (use with caution)
cp -r _deprecated/levelith_admin_dashboard_OLD dev/dev-frontend/levelith_admin_dashboard
```

**Important:** This is only for emergency rollback. The old dashboard has known issues and should not be used long-term.

---

## Questions?

- **Migration Plan:** See [ADMIN_DASHBOARD_REFACTOR_V2.md](../docs/development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md)
- **Current Progress:** Check inline `AdminDashboardRefactorv2` TODOs in `frontend/src/admin/`
- **Issues:** Report in GitHub issues with tag `admin-dashboard-refactor`

---

**Last Updated:** November 20, 2025
**Deprecated By:** AdminDashboardRefactorv2 (Plan C)
