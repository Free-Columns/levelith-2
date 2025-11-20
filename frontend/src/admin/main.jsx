// AdminDashboardRefactorv2: REPLACE - Convert to TypeScript and add React Query + ErrorBoundary
// What: Rename to main.tsx, add QueryClientProvider, Toaster, ErrorBoundary
// Why: Type safety, automatic API caching/refetching, toast notifications, error handling
// Risk: Breaking change - need to install @tanstack/react-query, sonner, configure QueryClient
// Phase: 1 (Core Infrastructure)
// Complexity: Medium
// Depends: Phase 0 (dependency installation)
//
// NEW STRUCTURE:
// import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
// import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
// import { Toaster } from 'sonner';
// import { ErrorBoundary } from './components/custom/ErrorBoundary';
//
// const queryClient = new QueryClient({
//   defaultOptions: {
//     queries: { staleTime: 5 * 60 * 1000, retry: 1 },
//     mutations: { retry: 0 },
//   },
// });
//
// <QueryClientProvider client={queryClient}>
//   <ErrorBoundary>
//     <App />
//     <Toaster position="top-right" />
//   </ErrorBoundary>
//   <ReactQueryDevtools />
// </QueryClientProvider>

import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
// AdminDashboardRefactorv2: DELETE - Remove DataSourceContext completely
// What: Delete this import and the provider wrapper below
// Why: Replacing with React Query (no more LOCAL/SERVER switching)
// Risk: None - this is the goal (remove mock data)
// Phase: 1 (Core Infrastructure)
import { DataSourceProvider } from "./context/DataSourceContext";
import App from "./App";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    {/* AdminDashboardRefactorv2: DELETE - Remove DataSourceProvider wrapper */}
    <DataSourceProvider>
      <App />
    </DataSourceProvider>
  </BrowserRouter>
);
