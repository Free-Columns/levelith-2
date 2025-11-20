/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ONETRUTH color palette - Synced with frontend/src/config/ONETRUTH.ts
        primary: {
          DEFAULT: '#007EA7',
          dark: '#2980b9',
          light: '#5dade2',
        },
        secondary: {
          DEFAULT: '#088732',
          dark: '#0b752eff',
          light: '#58d68d',
        },
        accent: {
          DEFAULT: '#e74c3c',
          dark: '#c0392b',
          light: '#ec7063',
        },
        background: {
          DEFAULT: '#FFFFFF',
          dark: '#000000',
          surface: '#F4F4F9',
        },
        surface: {
          DEFAULT: '#F4F4F9',
          dark: '#2c3e50',
        },
        text: {
          DEFAULT: '#2c3e50',
          light: '#FFFFFF',
          dark: '#0f151bff',
          inverse: '#ffffff',
          muted: '#95a5a6',
          subdued: '#7f8c8d',
          highlight: '#ffd500',
          code: '#e74c3c',
        },
        // Experience type colors
        education: '#088732',
        workplace: '#007EA7',
        skills: '#F24236',
        // Status colors
        success: '#2ecc71',
        warning: '#f39c12',
        error: '#e74c3c',
        info: '#3498db',
        // Markdown & Documentation specific colors
        code: {
          text: '#ffd500',
          background: '#0f151b',
          block: {
            background: '#2c3e50',
            text: '#ffffff',
          },
        },
        blockquote: {
          text: '#7f8c8d',
          background: 'rgba(0, 126, 167, 0.05)',
          border: '#007EA7',
        },
        table: {
          header: {
            background: '#000000',
            text: '#ffd500',
          },
          rowEven: '#f8f9fa',
        },
        link: {
          text: '#007EA7',
          hover: '#2980b9',
        },
        // Borders
        border: {
          DEFAULT: '#bdc3c7',
          light: '#ecf0f1',
        },
        divider: '#d5dbdb',
      },
      fontFamily: {
        heading: ['"Montserrat"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        body: ['"Open Sans"', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        mono: ['"Fira Code"', '"Courier New"', 'Courier', 'monospace'],
      },
    },
  },
  plugins: [],
}
