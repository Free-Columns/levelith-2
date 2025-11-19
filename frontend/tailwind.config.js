/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ONETRUTH color palette
        primary: {
          DEFAULT: '#3498db',
          dark: '#2980b9',
          light: '#5dade2',
        },
        secondary: {
          DEFAULT: '#2ecc71',
          dark: '#27ae60',
          light: '#58d68d',
        },
        accent: {
          DEFAULT: '#e74c3c',
          dark: '#c0392b',
          light: '#ec7063',
        },
        background: {
          DEFAULT: '#ecf0f1',
          dark: '#34495e',
          light: '#ffffff',
        },
        surface: {
          DEFAULT: '#ffffff',
          dark: '#2c3e50',
        },
        text: {
          DEFAULT: '#2c3e50',
          light: '#7f8c8d',
          dark: '#1a252f',
          inverse: '#ffffff',
        },
        education: '#9b59b6',
        workplace: '#e67e22',
        skills: '#1abc9c',
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
