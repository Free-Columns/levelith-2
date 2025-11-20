/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // shadcn/ui color system (CSS variables)
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          // ONETRUTH variants
          dark: '#2980b9',
          light: '#5dade2',
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
          // ONETRUTH variants
          dark: '#0b752eff',
          light: '#58d68d',
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
          // ONETRUTH variants
          dark: '#c0392b',
          light: '#ec7063',
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // ONETRUTH specific colors (legacy support)
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
        // Border variants (legacy support)
        'border-light': '#ecf0f1',
        divider: '#d5dbdb',
      },
      fontFamily: {
        heading: ['"Montserrat"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        body: ['"Open Sans"', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        mono: ['"Fira Code"', '"Courier New"', 'Courier', 'monospace'],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
