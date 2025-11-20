// ============================================================================
// AdminDashboardRefactorv2: DELETE - This entire file must be DELETED!
// ============================================================================
// What: Delete DataSourceSwitcher.jsx completely (95 lines)
// Why: No more LOCAL/SERVER switching - server-only mode
// Risk: Low - only used in AdminLayout header
// Phase: 1 (Core Infrastructure - final step)
// Complexity: Low
// Depends: DataSourceContext must be deleted first
//
// FILES THAT IMPORT THIS:
// - frontend/src/admin/layouts/AdminLayout.jsx (header component)
//
// REMOVAL STEPS:
// 1. Remove <DataSourceSwitcher /> from AdminLayout header
// 2. Delete this file
//
// OPTIONAL REPLACEMENT:
// Could add environment indicator instead (dev/staging/prod badge)
// - Example: <Badge variant="outline">Production</Badge>
// ============================================================================

/**
 * Data Source Switcher Component
 *
 * Allows switching between local mock data and server API data.
 * Displays in the application header.
 */

import React from "react";
// AdminDashboardRefactorv2: DELETE - Will be removed when DataSourceContext is deleted
import { useDataSource, DATA_SOURCES } from "../context/DataSourceContext";
import ONETRUTH from "../config/theme";

export default function DataSourceSwitcher() {
  const { dataSource, switchDataSource } = useDataSource();

  const isLocal = dataSource === DATA_SOURCES.LOCAL;

  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
      <span style={{fontSize: '14px', fontWeight: 500, color: ONETRUTH.colors.textDark}}>Data Source:</span>
      <div style={{
        display: 'inline-flex',
        borderRadius: '8px',
        border: `1px solid ${ONETRUTH.colors.border}`,
        backgroundColor: ONETRUTH.colors.surface,
        padding: '4px'
      }}>
        <button
          onClick={() => switchDataSource(DATA_SOURCES.LOCAL)}
          style={{
            padding: '6px 16px',
            fontSize: '14px',
            fontWeight: 500,
            borderRadius: '6px',
            transition: 'all 0.2s',
            backgroundColor: isLocal ? ONETRUTH.colors.primary : "transparent",
            color: isLocal ? ONETRUTH.colors.textInverse : ONETRUTH.colors.text,
            border: 'none',
            cursor: 'pointer',
            boxShadow: isLocal ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'
          }}
        >
          <span style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
            <svg
              style={{width: '16px', height: '16px'}}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Local (Mock)
          </span>
        </button>
        <button
          onClick={() => switchDataSource(DATA_SOURCES.SERVER)}
          style={{
            padding: '6px 16px',
            fontSize: '14px',
            fontWeight: 500,
            borderRadius: '6px',
            transition: 'all 0.2s',
            backgroundColor: !isLocal ? ONETRUTH.colors.primary : "transparent",
            color: !isLocal ? ONETRUTH.colors.textInverse : ONETRUTH.colors.text,
            border: 'none',
            cursor: 'pointer',
            boxShadow: !isLocal ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'
          }}
        >
          <span style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
            <svg
              style={{width: '16px', height: '16px'}}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"
              />
            </svg>
            Server API
          </span>
        </button>
      </div>
    </div>
  );
}
