// AdminDashboardRefactorv2: REPLACE - Convert to TypeScript with /admin prefix routing
// What: Rename to App.tsx, add /admin base route, add route guards, fix import paths
// Why: Type safety, correct routing (/admin/users not /users), authentication protection
// Risk: Medium - all navigation links need updating, may break existing bookmarks
// Phase: 7 (Routing & Layout)
// Complexity: Medium
// Depends: Phase 1 (infrastructure), all page migrations complete
//
// NEW STRUCTURE:
// import type { FC } from 'react';
// import { Routes, Route, Navigate } from 'react-router-dom';
// import { ProtectedRoute } from './components/auth/ProtectedRoute';
// import { AdminLayout } from './components/layout/AdminLayout';
// import { Dashboard } from './features/dashboard/Dashboard';
// import { Users } from './features/users/Users';
// import { Experiences } from './features/experiences/Experiences';
// import { NAICSCodes } from './features/naics/NAICSCodes';
// import { Settings } from './features/settings/Settings';
// import { Login } from './features/auth/Login';
// import { NotFound } from './components/layout/NotFound';
//
// <Routes>
//   <Route path="/login" element={<Login />} />
//   <Route path="/admin" element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
//     <Route index element={<Dashboard />} />
//     <Route path="users" element={<Users />} />
//     <Route path="experiences" element={<Experiences />} />
//     <Route path="naics" element={<NAICSCodes />} />
//     <Route path="settings" element={<Settings />} />
//   </Route>
//   <Route path="/" element={<Navigate to="/admin" replace />} />
//   <Route path="*" element={<NotFound />} />
// </Routes>

import React from "react";
import { Routes, Route } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
// AdminDashboardRefactorv2: BUG - Import paths are incorrect!
// What: These imports show "./pages/admin/Dashboard" but files are at "./pages/Dashboard.jsx"
// Why: Broken imports will cause runtime errors
// Risk: High - app won't load
// Phase: 0 (should fix immediately if blocking)
// Complexity: Low (just fix the paths)
// FIX: Change to "./pages/Dashboard", "./pages/Users", etc.
import Dashboard from "./pages/admin/Dashboard";
import Users from "./pages/admin/Users";
import Experiences from "./pages/admin/Experiences";
import NAICSCodes from "./pages/admin/NAICSCodes";
import Settings from "./pages/admin/Settings";
import Login from "./pages/Login";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      {/* AdminDashboardRefactorv2: FIX - Wrong base route! Should be /admin not /
       * What: Change path="/" to path="/admin" and add redirect from / to /admin
       * Why: Admin dashboard should be at /admin/* not root level
       * Risk: Low - just needs navigation link updates in AdminLayout
       * Phase: 7 (Routing & Layout)
       * Complexity: Low
       */}
      <Route path="/" element={<AdminLayout />}>
        <Route index element={<Dashboard />} />
        {/* AdminDashboardRefactorv2: NOTE - These routes will become /admin/users, /admin/experiences, etc.
         * Currently: /users, /experiences, /naics, /settings
         * After fix: /admin/users, /admin/experiences, /admin/naics, /admin/settings
         */}
        <Route path="users" element={<Users />} />
        <Route path="experiences" element={<Experiences />} />
        <Route path="naics" element={<NAICSCodes />} />
        <Route path="settings" element={<Settings />} />
      </Route>
      {/* AdminDashboardRefactorv2: ADD - Missing routes
       * What: Add redirect and 404 routes
       * Why: Better UX (/ redirects to /admin, catch-all for typos)
       * Phase: 7 (Routing & Layout)
       * ADD:
       * <Route path="/" element={<Navigate to="/admin" replace />} />
       * <Route path="*" element={<NotFound />} />
       */}
    </Routes>
  );
}
