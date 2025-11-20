// AdminDashboardRefactorv2: REPLACE - Convert to TypeScript, fix import, use Tailwind
// What: Rename to theme.ts, fix ONETRUTH import, migrate to Tailwind CSS
// Why: Type safety, eliminate inline styles, use utility classes
// Risk: Medium - all components using ONETRUTH for inline styles need migration
// Phase: 1 (Core Infrastructure)
// Complexity: High (affects all components)
// Depends: Phase 0 (Tailwind installation)
//
// CURRENT ISSUE:
// - Line 9: import { ONETRUTH } - uses NAMED export, but ONETRUTH.ts uses DEFAULT export
// - This causes ONETRUTH to be undefined at runtime
// - Modal.jsx crashes trying to access ONETRUTH.zIndex.modal
//
// IMMEDIATE FIX (before full migration):
// Change line 9 to: import ONETRUTH from '../../config/ONETRUTH';
// Change line 45 to: export default ONETRUTH; (not named export)
//
// LONG-TERM PLAN (Tailwind migration):
// - Phase 0: Install Tailwind, configure with ONETRUTH colors
// - Phase 1-7: Migrate all inline styles to Tailwind classes
// - Example: style={{color: ONETRUTH.colors.primary}} → className="text-primary"
// - Delete this file once all components use Tailwind
// ============================================================================

/**
 * Theme Configuration - Integrated with ONETRUTH
 *
 * This file imports the ONETRUTH configuration from the main frontend
 * and provides theme utilities for the admin dashboard.
 */

// AdminDashboardRefactorv2: BUG - Wrong import syntax!
// ISSUE: Using named import { ONETRUTH } but ONETRUTH.ts exports as default
// FIX: Change to: import ONETRUTH from '../../config/ONETRUTH';
import { ONETRUTH } from '../../config/ONETRUTH';

/**
 * Get category color from ONETRUTH
 */
export const getCategoryColor = (category) => {
  const colors = {
    education: ONETRUTH.colors.education,
    workplace: ONETRUTH.colors.workplace,
    skills: ONETRUTH.colors.skills,
  };
  return colors[category] || ONETRUTH.colors.text;
};

/**
 * Get NAICS industry color
 */
export const getNAICSColor = (industry) => {
  return ONETRUTH.naics[industry] || ONETRUTH.naics.general;
};

/**
 * Get status color
 */
export const getStatusColor = (status) => {
  const colors = {
    success: ONETRUTH.colors.success,
    warning: ONETRUTH.colors.warning,
    error: ONETRUTH.colors.error,
    info: ONETRUTH.colors.info,
    active: ONETRUTH.colors.success,
    inactive: ONETRUTH.colors.error,
  };
  return colors[status] || ONETRUTH.colors.text;
};

export default ONETRUTH;
