/**
 * ONETRUTH - Single Source of Truth for Levelith Branding
 *
 * This is the authoritative branding configuration for the entire application.
 * ALL components must reference this file for theming - NO hardcoded values!
 *
 * CRITICAL REQUIREMENT: All UI components, styles, and theming MUST import
 * values from this configuration. Never hardcode colors, fonts, or spacing.
 */

export const ONETRUTH = {
  /**
   * Color palette - Primary brand colors
   */
  colors: {
    // Primary brand colors
    primary: "#007EA7", //  main brand color
    primaryDark: "#2980b9", // Darker blue for hover states
    primaryLight: "#5dade2", // Lighter blue for backgrounds

    // Secondary colors
    secondary: "#088732", // Green - success, positive actions
    secondaryDark: "#0b752eff",
    secondaryLight: "#58d68d",

    // Accent colors
    accent: "#e74c3c", // Red - alerts, important actions
    accentDark: "#c0392b",
    accentLight: "#ec7063",

    // Neutral colors
    background: "#FFFFFF", // Light gray background
    backgroundDark: "#1f1f1fff", // Dark background for dark mode
    surface: "#F4F4F9", // White surface for cards, modals
    surfaceDark: "#2c3e50",

    // Text colors
    text: "#2c3e50", // Dark gray for body text
    textLight: "#FFFFFF", // Light gray for secondary text
    textDark: "#0f151bff", // Almost black for headings
    textInverse: "#ffffff", // White text on dark backgrounds

    // Status colors
    success: "#2ecc71",
    warning: "#f39c12",
    error: "#e74c3c",
    info: "#3498db",

    // Experience type colors (for gamification)
    education: "#088732", // Purple for education
    workplace: "#007EA7", // Orange for workplace
    skills: "#F24236 ", // Teal for skills

    // Borders and dividers
    border: "#bdc3c7",
    borderLight: "#ecf0f1",
    divider: "#d5dbdb",

    // Markdown & Documentation specific colors
    codeText: "#ffd500", // Golden yellow for inline code text
    codeBackground: "#0f151b", // Dark blue-black for inline code background
    codeBlockBackground: "#2c3e50", // Dark surface for code blocks
    codeBlockText: "#ffffff", // White text for code blocks

    blockquoteText: "#7f8c8d", // Light gray for blockquote text
    blockquoteBackground: "rgba(0, 126, 167, 0.05)", // Subtle blue tint
    blockquoteBorder: "#007EA7", // Primary color for left border

    tableHeaderBackground: "#000000", // Black background for table headers
    tableHeaderText: "#ffd500", // Golden yellow for table header text
    tableRowEven: "#f8f9fa", // Very light gray for alternating table rows

    linkText: "#007EA7", // Primary color for links
    linkHover: "#2980b9", // Darker blue for link hover

    // Additional semantic text colors
    textMuted: "#95a5a6", // Muted text for less important content
    textSubdued: "#7f8c8d", // Subdued text for captions, meta info
    textHighlight: "#ffd500", // Highlight color for important text
    textCode: "#e74c3c", // Red for inline code mentions in text
  },

  /**
   * Typography - Font families and sizes
   */
  fonts: {
    // Font families
    heading: '"Montserrat", "Helvetica Neue", Arial, sans-serif',
    body: '"Open Sans", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    monospace: '"Fira Code", "Courier New", Courier, monospace',

    // Font sizes
    sizes: {
      xs: "0.75rem", // 12px
      sm: "0.875rem", // 14px
      base: "1rem", // 16px
      lg: "1.125rem", // 18px
      xl: "1.25rem", // 20px
      "2xl": "1.5rem", // 24px
      "3xl": "1.875rem", // 30px
      "4xl": "2.25rem", // 36px
      "5xl": "3rem", // 48px
    },

    // Font weights
    weights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },

    // Line heights
    lineHeights: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
      loose: 2,
    },
  },

  /**
   * Spacing - Consistent spacing scale
   */
  spacing: {
    xs: "0.25rem", // 4px
    sm: "0.5rem", // 8px
    md: "1rem", // 16px
    lg: "1.5rem", // 24px
    xl: "2rem", // 32px
    "2xl": "3rem", // 48px
    "3xl": "4rem", // 64px
    "4xl": "6rem", // 96px
  },

  /**
   * Border radius - Consistent rounded corners
   */
  borderRadius: {
    none: "0",
    sm: "0.125rem", // 2px
    base: "0.25rem", // 4px
    md: "0.375rem", // 6px
    lg: "0.5rem", // 8px
    xl: "0.75rem", // 12px
    "2xl": "1rem", // 16px
    full: "9999px", // Fully rounded
  },

  /**
   * Shadows - Elevation and depth
   */
  shadows: {
    none: "none",
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    base: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    inner: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
  },

  /**
   * Breakpoints - Responsive design breakpoints
   */
  breakpoints: {
    xs: "320px", // Small mobile
    sm: "640px", // Mobile
    md: "768px", // Tablet
    lg: "1024px", // Desktop
    xl: "1280px", // Large desktop
    "2xl": "1536px", // Extra large desktop
  },

  /**
   * Z-index - Layering hierarchy
   */
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },

  /**
   * Transitions - Animation timings
   */
  transitions: {
    fast: "150ms ease-in-out",
    base: "300ms ease-in-out",
    slow: "500ms ease-in-out",
  },

  /**
   * Gamification - Game-specific styling
   */
  gamification: {
    // Level colors (progression tiers)
    levels: {
      beginner: "#95a5a6", // Gray
      intermediate: "#3498db", // Blue
      advanced: "#9b59b6", // Purple
      expert: "#e67e22", // Orange
      master: "#e74c3c", // Red
      legend: "#f39c12", // Gold
    },

    // Achievement badge colors
    achievements: {
      bronze: "#cd7f32",
      silver: "#c0c0c0",
      gold: "#ffd700",
      platinum: "#e5e4e2",
      diamond: "#b9f2ff",
    },

    // Progress bar colors
    progress: {
      low: "#e74c3c", // Red (0-33%)
      medium: "#f39c12", // Orange (34-66%)
      high: "#2ecc71", // Green (67-100%)
    },
  },

  /**
   * NAICS - Industry classification styling
   */
  naics: {
    general: "#95a5a6", // Gray for fallback code 123456
    education: "#9b59b6", // Purple
    technology: "#3498db", // Blue
    healthcare: "#e74c3c", // Red
    finance: "#27ae60", // Green
    retail: "#e67e22", // Orange
    manufacturing: "#34495e", // Dark gray
    services: "#1abc9c", // Teal
  },
} as const;

/**
 * Type-safe theme access
 *
 * Example usage:
 * ```typescript
 * import { ONETRUTH } from './config/ONETRUTH';
 *
 * const Header = styled.header`
 *   background-color: ${ONETRUTH.colors.primary};
 *   font-family: ${ONETRUTH.fonts.heading};
 *   padding: ${ONETRUTH.spacing.lg};
 * `;
 * ```
 */
export type OneTruthTheme = typeof ONETRUTH;

export default ONETRUTH;
