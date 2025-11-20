# Frontend Development Guide

---
title: "Frontend Development Guide"
description: "Comprehensive guide for developing the Levelith frontend application using React, TypeScript, and the ONETRUTH branding system."
category: "guides"
tags: ["frontend", "react", "typescript", "onetruth", "vite", "development"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 25
relatedPages:
  - "/docs/api/API_DOCUMENTATION.md"
  - "/docs/DEVELOPER_GUIDE.md"
  - "/docs/backend/BACKEND_GUIDE.md"
nextPage: "/docs/api/API_DOCUMENTATION.md"
prevPage: "/docs/DEVELOPER_GUIDE.md"
searchKeywords:
  - "frontend"
  - "react"
  - "typescript"
  - "onetruth"
  - "vite"
  - "tailwind"
  - "admin dashboard"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Frontend Development Guide

> **TL;DR:** Build modern React applications for Levelith using TypeScript, Vite, and the ONETRUTH branding system. All styling must use ONETRUTH (no hardcoded values), admin dashboard uses inline styles, and main app can use Tailwind CSS.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [ONETRUTH Branding System](#onetruth-branding-system)
- [Creating New Pages](#creating-new-pages)
- [Updating Existing Pages](#updating-existing-pages)
- [Component Development](#component-development)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Routing](#routing)
- [Tailwind CSS Setup](#tailwind-css-setup)
- [Styling Guidelines](#styling-guidelines)
- [Testing](#testing)
- [Build and Deployment](#build-and-deployment)
- [Common Patterns](#common-patterns)
- [Admin Dashboard Styling Guidelines](#admin-dashboard-styling-guidelines)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)
- [Related Documentation](#related-documentation)
- [Feedback](#feedback)

---

## Overview

The Levelith frontend is a modern React application built with TypeScript, focusing on user experience, performance, and maintainability.

### Key Features

- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **React Router v6** for client-side routing
- **ONETRUTH** branding system for consistent theming
- **Axios** for API communication
- **Recharts** for data visualization
- **React Markdown** for documentation rendering
- **Tailwind CSS** for utility-first styling (main app only)

### Core Principles

1. ✅ **Type Safety** - Everything is typed with TypeScript
2. ✅ **Consistency** - All styling uses ONETRUTH configuration
3. ✅ **Reusability** - Components are modular and composable
4. ✅ **Performance** - Lazy loading, code splitting, and optimization
5. ✅ **Accessibility** - ARIA labels, keyboard navigation, semantic HTML

:::info
**Note:** The admin dashboard strictly enforces inline styles with ONETRUTH (no Tailwind classes), while the main application can use Tailwind CSS utilities.
:::

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface (React)            │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Pages   │  │Components│  │ Layouts  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                             │
├─────────────────────────────────────────────┤
│            State Management                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Context  │  │ useState │  │useEffect │  │
│  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────┤
│             API Layer (Axios)               │
│  ┌──────────────────────────────────────┐  │
│  │       apiService.js                  │  │
│  │  (Authentication, CRUD, Interceptors)│  │
│  └──────────────────────────────────────┘  │
├─────────────────────────────────────────────┤
│          Backend API (FastAPI)              │
└─────────────────────────────────────────────┘
```

### Application Structure

- **Main App**: User-facing pages (Landing, Docs)
- **Admin App**: Administration dashboard (separate entry point)
- **Shared**: ONETRUTH config, utilities, types

---

## Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | UI framework |
| **TypeScript** | 5.3.2 | Type safety |
| **Vite** | 5.0.6 | Build tool and dev server |
| **React Router** | 6.22.0 | Client-side routing |
| **Axios** | 1.6.0 | HTTP client |
| **Recharts** | 2.9.0 | Charts and visualizations |
| **React Markdown** | Latest | Markdown rendering |
| **Tailwind CSS** | 3.4.0 | Utility-first CSS |
| **Vitest** | 1.0.2 | Unit testing |
| **Playwright** | 1.40.1 | E2E testing |

---

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx                 # Main app entry point
│   ├── App.tsx                  # Main app router
│   ├── config/
│   │   └── ONETRUTH.ts         # ⚠️ SINGLE SOURCE OF TRUTH for branding
│   ├── pages/
│   │   ├── Landing.tsx         # Landing page
│   │   └── Docs.tsx           # Documentation viewer
│   ├── components/            # Reusable UI components
│   ├── hooks/                 # Custom React hooks
│   ├── services/              # API services
│   ├── utils/                 # Utility functions
│   ├── types/                 # TypeScript type definitions
│   │
│   └── admin/                 # Admin dashboard (separate app)
│       ├── main.jsx          # Admin entry point
│       ├── App.jsx           # Admin router
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── Users.jsx
│       │   ├── Experiences.jsx
│       │   ├── NAICSCodes.jsx
│       │   ├── Settings.jsx
│       │   └── Login.jsx
│       ├── components/
│       │   ├── DataSourceSwitcher.jsx
│       │   ├── Modal.jsx
│       │   └── forms/        # Form components
│       ├── layouts/
│       │   └── AdminLayout.jsx
│       ├── services/
│       │   └── apiService.js  # API client with interceptors
│       ├── context/
│       │   └── DataSourceContext.jsx
│       ├── config/
│       │   ├── theme.js      # ONETRUTH theme
│       │   └── mockData.js
│       └── data/
│           └── mockData.js
│
├── public/                    # Static assets
├── index.html                 # Main HTML template
├── admin.html                 # Admin HTML template
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Dependencies and scripts
└── tailwind.config.js        # Tailwind CSS config
```

---

## ONETRUTH Branding System

### What is ONETRUTH?

ONETRUTH is the **single source of truth** for all branding, theming, and styling in the Levelith application.

**Benefits:**

- ✅ Consistent colors, fonts, spacing across all components
- ✅ Easy theme updates (change once, apply everywhere)
- ✅ No hardcoded values scattered throughout the codebase
- ✅ Dynamic theme switching capability
- ✅ Future-ready for dark mode

**Location:** `/frontend/src/config/ONETRUTH.ts`

:::warning
**Warning:** Never hardcode colors, fonts, or spacing values. Always use ONETRUTH. Hardcoded values caused blank screen bugs in the admin dashboard modals.
:::

### ONETRUTH Structure

```typescript
export const ONETRUTH = {
  // Colors
  colors: {
    primary: "#3498db",        // Main brand color (blue)
    secondary: "#2ecc71",      // Success green
    accent: "#e74c3c",         // Alert red
    background: "#ecf0f1",     // Light gray background
    surface: "#ffffff",        // White surfaces
    textDark: "#2c3e50",      // Dark text
    textLight: "#7f8c8d",     // Light text
    textInverse: "#ffffff",   // Inverse text
    // ... many more colors
  },

  // Typography
  fonts: {
    heading: "Montserrat, sans-serif",
    body: "Open Sans, sans-serif",
    monospace: "Fira Code, monospace",

    sizes: {
      xs: "12px",
      sm: "14px",
      base: "16px",
      lg: "18px",
      xl: "20px",
      "2xl": "24px",
      "3xl": "30px",
      "4xl": "36px",
      "5xl": "48px",
    },

    weights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },

    lineHeights: {
      tight: "1.25",
      normal: "1.5",
      relaxed: "1.75",
      loose: "2",
    },
  },

  // Spacing
  spacing: {
    xs: "4px",
    sm: "8px",
    md: "16px",
    lg: "24px",
    xl: "32px",
    "2xl": "48px",
    "3xl": "64px",
    "4xl": "96px",
  },

  // Border Radius
  borderRadius: {
    sm: "4px",
    md: "8px",
    lg: "12px",
    xl: "16px",
    "2xl": "24px",
    full: "9999px",
  },

  // Shadows
  shadows: {
    sm: "0 1px 2px rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px rgba(0, 0, 0, 0.1)",
    lg: "0 10px 15px rgba(0, 0, 0, 0.1)",
    xl: "0 20px 25px rgba(0, 0, 0, 0.1)",
    "2xl": "0 25px 50px rgba(0, 0, 0, 0.25)",
  },

  // Transitions
  transitions: {
    fast: "150ms ease",
    base: "300ms ease",
    slow: "500ms ease",
  },

  // Experience Type Colors
  experienceTypes: {
    education: "#9b59b6",
    workplace: "#e67e22",
    skills: "#1abc9c",
  },

  // NAICS Industry Colors
  naicsColors: {
    technology: "#3498db",
    healthcare: "#e74c3c",
    finance: "#27ae60",
  },

  // Z-Index
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },
};
```

### Using ONETRUTH

**Always import and use ONETRUTH values:**

```typescript
import { ONETRUTH } from '../config/ONETRUTH';

// ✅ CORRECT
const styles = {
  container: {
    backgroundColor: ONETRUTH.colors.background,
    padding: ONETRUTH.spacing.lg,
    borderRadius: ONETRUTH.borderRadius.md,
    fontFamily: ONETRUTH.fonts.body,
  },
};

// ❌ WRONG - Never hardcode values
const badStyles = {
  container: {
    backgroundColor: "#ecf0f1",
    padding: "24px",
    borderRadius: "8px",
    fontFamily: "Open Sans",
  },
};
```

:::tip
**Pro Tip:** Use your IDE's autocomplete with ONETRUTH to discover available theme values. Most IDEs will show you all available options when you type `ONETRUTH.colors.` or `ONETRUTH.spacing.`
:::

---

## Creating New Pages

### Step-by-Step Guide

#### 1. Create the Page Component

Create a new file in `/frontend/src/pages/`:

```typescript
// src/pages/NewPage.tsx

import React from 'react';
import { ONETRUTH } from '../config/ONETRUTH';

const NewPage: React.FC = () => {
  const styles = {
    container: {
      padding: ONETRUTH.spacing['2xl'],
      backgroundColor: ONETRUTH.colors.background,
      minHeight: '100vh',
    },
    title: {
      fontSize: ONETRUTH.fonts.sizes['4xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      color: ONETRUTH.colors.textDark,
      marginBottom: ONETRUTH.spacing.xl,
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>New Page</h1>
      <p>Your content here...</p>
    </div>
  );
};

export default NewPage;
```

#### 2. Add Route to App.tsx

```typescript
// src/App.tsx

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Docs from './pages/Docs';
import NewPage from './pages/NewPage';  // Import your new page

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/docs" element={<Docs />} />
        <Route path="/docs/:docPath" element={<Docs />} />
        <Route path="/new-page" element={<NewPage />} />  {/* Add route */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
```

#### 3. Test the Page

```bash
# Start dev server
npm run dev

# Navigate to http://localhost:5173/new-page
```

:::info
**Note:** Always test your new pages locally before committing. Check for TypeScript errors, proper ONETRUTH usage, and responsive design.
:::

---

## Updating Existing Pages

### Example: Updating the Landing Page

**1. Open the file:** `/frontend/src/pages/Landing.tsx`

**2. Make changes using ONETRUTH:**

```typescript
// Landing.tsx

import { ONETRUTH } from '../config/ONETRUTH';

const styles = {
  hero: {
    backgroundColor: ONETRUTH.colors.primary,
    padding: ONETRUTH.spacing['3xl'],
    textAlign: 'center' as const,
  },
  title: {
    fontSize: ONETRUTH.fonts.sizes['5xl'],
    color: ONETRUTH.colors.textInverse,
    fontFamily: ONETRUTH.fonts.heading,
  },
};

return (
  <div style={styles.hero}>
    <h1 style={styles.title}>Welcome to Levelith</h1>
  </div>
);
```

**3. Test locally:**

```bash
npm run dev
```

**4. Build for production:**

```bash
npm run build
```

---

## Component Development

### Creating Reusable Components

Components should be:
- **Typed** with TypeScript
- **Styled** using ONETRUTH
- **Documented** with JSDoc comments
- **Testable** with clear props

**Example: Button Component**

```typescript
// src/components/Button.tsx

import React from 'react';
import { ONETRUTH } from '../config/ONETRUTH';

interface ButtonProps {
  /** Button text */
  children: React.ReactNode;
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Click handler */
  onClick?: () => void;
  /** Disabled state */
  disabled?: boolean;
}

/**
 * Reusable button component following ONETRUTH styling
 */
export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
}) => {
  const variantColors = {
    primary: ONETRUTH.colors.primary,
    secondary: ONETRUTH.colors.secondary,
    danger: ONETRUTH.colors.error,
  };

  const styles = {
    button: {
      backgroundColor: variantColors[variant],
      color: ONETRUTH.colors.textInverse,
      padding: `${ONETRUTH.spacing.sm} ${ONETRUTH.spacing.lg}`,
      borderRadius: ONETRUTH.borderRadius.md,
      border: 'none',
      fontSize: ONETRUTH.fonts.sizes.base,
      fontWeight: ONETRUTH.fonts.weights.medium,
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1,
      transition: ONETRUTH.transitions.fast,
    },
  };

  return (
    <button
      style={styles.button}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

**Usage:**

```typescript
import { Button } from './components/Button';

<Button variant="primary" onClick={handleClick}>
  Click Me
</Button>
```

---

## State Management

### Local State (useState)

For component-specific state:

```typescript
import { useState } from 'react';

const MyComponent = () => {
  const [count, setCount] = useState<number>(0);
  const [name, setName] = useState<string>('');

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};
```

### Context API

For shared state across multiple components:

```typescript
// src/context/UserContext.tsx

import React, { createContext, useContext, useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
};
```

**Usage:**

```typescript
// Wrap app with provider
import { UserProvider } from './context/UserContext';

<UserProvider>
  <App />
</UserProvider>

// Use in components
import { useUser } from '../context/UserContext';

const Profile = () => {
  const { user, setUser } = useUser();

  return <div>{user?.name}</div>;
};
```

---

## API Integration

### API Service Configuration

**Location:** `/frontend/src/admin/services/apiService.js`

```javascript
import axios from 'axios';

const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL ||
           "https://levelith-backend.onrender.com/api/v1",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
};

const apiClient = axios.create(API_CONFIG);
```

### Environment Variables

Create `.env.local` file:

```bash
# Development
VITE_API_URL=http://localhost:8000/api/v1

# Production (automatic from env)
# VITE_API_URL=https://levelith-backend.onrender.com/api/v1
```

:::warning
**Warning:** Never commit `.env.local` to git. This file contains environment-specific configuration and should be listed in `.gitignore`.
:::

### API Data Transformation Layer ⭐

**Location:** `/frontend/src/lib/transformers.ts`

The frontend includes a global transformation layer that automatically converts between frontend camelCase and backend snake_case conventions.

#### How It Works

All API requests and responses are automatically transformed via axios interceptors:

```typescript
// Frontend code uses camelCase
const userData = {
  firstName: 'John',
  lastName: 'Doe',
  isActive: true
}

// Request interceptor transforms to snake_case
api.post('/users', userData)
// → Backend receives: { first_name: 'John', last_name: 'Doe', is_active: true }

// Backend responds with snake_case
// { user_id: 123, first_name: 'John', created_at: '2025-01-01T00:00:00Z' }

// Response interceptor transforms to camelCase
// → Frontend receives: { userId: 123, firstName: 'John', createdAt: '2025-01-01T00:00:00Z' }
```

#### Available Utilities

```typescript
import {
  snakeToCamel,
  camelToSnake,
  keysToCamel,
  keysToSnake,
  transformPaginatedResponse
} from '@/lib/transformers'

// String transformations
snakeToCamel('user_name')    // → 'userName'
camelToSnake('userName')     // → 'user_name'

// Object transformations (deep/recursive)
keysToCamel({ user_name: 'John', is_active: true })
// → { userName: 'John', isActive: true }

keysToSnake({ userName: 'John', isActive: true })
// → { user_name: 'John', is_active: true }

// Paginated response normalization
transformPaginatedResponse(response)
// Handles both array responses and { items: [...], total: N } format
// Returns: { data: [...], total: N, page: 1, pageSize: 50, totalPages: N }
```

#### Automatic Transformation

The transformation is automatic via axios interceptors in `frontend/src/lib/api.ts`:

```typescript
// Request interceptor - transforms outgoing data
apiClient.interceptors.request.use((config) => {
  if (config.data) {
    config.data = keysToSnake(config.data)
  }
  if (config.params) {
    config.params = keysToSnake(config.params)
  }
  return config
})

// Response interceptor - transforms incoming data
apiClient.interceptors.response.use((response) => {
  if (response.data) {
    response.data = keysToCamel(response.data)
  }
  return response
})
```

#### Smart Handling

The transformers handle complex scenarios:

- ✅ **Nested objects** - Recursively transforms all levels
- ✅ **Arrays** - Transforms all items in arrays
- ✅ **Date objects** - Preserves Date instances
- ✅ **Null/undefined** - Safely handles missing values
- ✅ **Primitives** - Leaves strings, numbers, booleans unchanged
- ✅ **Type safety** - Full TypeScript support with generics

#### Example Usage

```typescript
// No manual transformation needed!
// Just write code in camelCase, transformation happens automatically

import { useUsers } from '@/admin/features/users/hooks/useUsers'

function UsersPage() {
  const { data, isLoading } = useUsers({
    pageSize: 50,        // Sent as page_size
    sortBy: 'createdAt'  // Sent as sort_by
  })

  // data.users is already in camelCase
  return (
    <div>
      {data.users.map(user => (
        <div key={user.id}>
          {user.firstName} {user.lastName}  {/* Already camelCase! */}
          {user.isActive ? '✅' : '❌'}
        </div>
      ))}
    </div>
  )
}
```

:::success
**Benefit:** Write clean, idiomatic JavaScript/TypeScript code without worrying about backend naming conventions. The transformation layer handles everything automatically!
:::

### Making API Calls

**Example: Fetching Users**

```typescript
import { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: string;
  name: string;
  email: string;
}

const UsersPage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL ||
                      'https://levelith-backend.onrender.com/api/v1';
        const response = await axios.get(`${apiUrl}/users`);
        setUsers(response.data.results);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch users');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

---

## Routing

### React Router v6 Setup

**Main Routes (`App.tsx`):**

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/docs" element={<Docs />} />
        <Route path="/docs/:docPath" element={<Docs />} />
        <Route path="/admin/*" element={<AdminApp />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};
```

### Navigation

**Link Component:**

```typescript
import { Link } from 'react-router-dom';

<Link to="/docs" style={{ color: ONETRUTH.colors.primary }}>
  Documentation
</Link>
```

**Programmatic Navigation:**

```typescript
import { useNavigate } from 'react-router-dom';

const MyComponent = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/dashboard');
  };

  return <button onClick={handleClick}>Go to Dashboard</button>;
};
```

### Route Parameters

```typescript
import { useParams } from 'react-router-dom';

const DocPage = () => {
  const { docPath } = useParams<{ docPath: string }>();

  return <div>Viewing: {docPath}</div>;
};
```

---

## Tailwind CSS Setup

### Overview

Levelith uses **Tailwind CSS** as the primary styling framework for the main application, integrated with the ONETRUTH design system.

:::info
**Note:** Tailwind CSS is used for the main application (Landing, Docs). The admin dashboard uses inline styles with ONETRUTH exclusively.
:::

### Configuration

**tailwind.config.js** (Root level):

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ONETRUTH color palette mapped to Tailwind
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
      },
      fontFamily: {
        heading: ['"Montserrat"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        body: ['"Open Sans"', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"Fira Code"', '"Courier New"', 'Courier', 'monospace'],
      },
    },
  },
  plugins: [],
}
```

### Using Tailwind Classes

Tailwind classes can be used directly in JSX (main app only):

```tsx
// Example: Card Component
export function Card({ title, children }) {
  return (
    <div className="p-6 rounded-lg shadow bg-surface">
      <h3 className="text-lg font-semibold mb-4 text-text-dark">
        {title}
      </h3>
      <div className="text-text">
        {children}
      </div>
    </div>
  );
}
```

### Common Tailwind Classes

**Layout:**
- `flex`, `grid`: Layout systems
- `w-64`, `h-screen`: Width/height
- `p-6`, `px-4`, `py-2`: Padding
- `m-4`, `mx-auto`, `my-2`: Margin

**Typography:**
- `text-2xl`, `text-lg`: Font sizes
- `font-bold`, `font-semibold`: Font weights
- `font-heading`, `font-body`: Custom font families
- `text-primary`, `text-text-dark`: Text colors

**Effects:**
- `shadow-sm`, `shadow-lg`: Box shadows
- `rounded-lg`, `rounded-md`: Border radius
- `hover:bg-primary`: Hover states
- `transition-all`: Transitions

### Responsive Design

```tsx
<div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
  {/* Responsive width */}
</div>

<nav className="space-y-2 lg:flex lg:space-y-0 lg:space-x-4">
  {/* Stack on mobile, horizontal on large screens */}
</nav>
```

---

## Styling Guidelines

### 1. Always Use ONETRUTH

```typescript
// ✅ CORRECT
const styles = {
  container: {
    backgroundColor: ONETRUTH.colors.background,
    padding: ONETRUTH.spacing.lg,
  },
};

// ❌ WRONG
const styles = {
  container: {
    backgroundColor: "#ecf0f1",
    padding: "24px",
  },
};
```

### 2. Inline Styles for Dynamic Values

```typescript
const styles = {
  box: {
    width: '100%',
    padding: ONETRUTH.spacing.md,
    backgroundColor: isActive ? ONETRUTH.colors.primary : ONETRUTH.colors.surface,
  },
};
```

### 3. Responsive Design

```typescript
const styles = {
  container: {
    padding: ONETRUTH.spacing.md,
    '@media (min-width: 768px)': {
      padding: ONETRUTH.spacing.xl,
    },
  },
};
```

---

## Testing

### Unit Tests (Vitest)

**Example Test:**

```typescript
// src/components/__tests__/Button.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

**Run Tests:**

```bash
npm run test          # Run tests in watch mode
npm run test:ci       # Run tests once with coverage
```

### E2E Tests (Playwright)

```typescript
// tests/e2e/landing.spec.ts

import { test, expect } from '@playwright/test';

test('landing page loads', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Levelith');
});

test('navigation to docs works', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Documentation');
  await expect(page).toHaveURL('/docs');
});
```

**Run E2E Tests:**

```bash
npm run test:e2e       # Run E2E tests
npm run test:e2e:ui    # Run with UI
```

---

## Build and Deployment

### Development

```bash
npm run dev            # Start dev server at http://localhost:5173
```

### Production Build

```bash
npm run build          # Build for production
npm run start          # Preview production build
```

### Build Output

```
dist/
├── assets/
│   ├── index-[hash].js      # Main bundle
│   ├── admin-[hash].js      # Admin bundle
│   └── styles-[hash].css    # Styles
├── index.html               # Main app
└── admin.html              # Admin app
```

### Deployment (Render.com)

**Build Command:** `npm run build`
**Publish Directory:** `dist`

**Environment variables in Render:**
- `VITE_API_URL`: Backend API URL

:::tip
**Pro Tip:** Always test the production build locally with `npm run start` before deploying to ensure there are no build-specific issues.
:::

---

## Common Patterns

### 1. Loading States

```typescript
const [loading, setLoading] = useState(true);

{loading ? (
  <div style={{
    textAlign: 'center',
    padding: ONETRUTH.spacing.xl,
    color: ONETRUTH.colors.primary
  }}>
    Loading...
  </div>
) : (
  <Content />
)}
```

### 2. Error Handling

```typescript
const [error, setError] = useState<string | null>(null);

{error && (
  <div style={{
    backgroundColor: ONETRUTH.colors.error,
    color: 'white',
    padding: ONETRUTH.spacing.lg,
    borderRadius: ONETRUTH.borderRadius.md,
  }}>
    Error: {error}
  </div>
)}
```

### 3. Conditional Rendering

```typescript
{user ? (
  <UserProfile user={user} />
) : (
  <LoginPrompt />
)}
```

### 4. Lists

```typescript
{items.map((item) => (
  <div key={item.id}>
    {item.name}
  </div>
))}
```

---

## Admin Dashboard Styling Guidelines

### NO HARDCODED CSS RULE

:::danger
**Critical:** The admin dashboard enforces strict ONETRUTH styling with NO hardcoded CSS classes or values. Violations caused blank screen bugs in modal components.
:::

#### Why This Matters

1. **Dynamic Theming** - Allows site-wide theme changes from one config file
2. **Consistency** - Ensures all components follow the same design system
3. **Maintainability** - Changes to theme propagate automatically
4. **Future Dark Mode** - Prepared for theme switching features

#### The Problem with className

**❌ BAD - Using Tailwind className:**

```jsx
// This caused blank screens in modals!
<div className="bg-white p-6 rounded-lg shadow-md">
  <h2 className="text-2xl font-semibold">Title</h2>
</div>
```

**Why this is bad:**
- Tailwind classes may not be compiled/available
- No dynamic theme switching capability
- Hardcoded values scattered throughout codebase
- Caused blank screen bugs in Modal components

#### The Solution: Inline Styles + ONETRUTH

**✅ GOOD - Using inline styles with ONETRUTH:**

```jsx
import ONETRUTH from '../config/theme';

<div style={{
  backgroundColor: ONETRUTH.colors.surface,
  padding: ONETRUTH.spacing.lg,
  borderRadius: ONETRUTH.borderRadius.md,
  boxShadow: ONETRUTH.shadows.md
}}>
  <h2 style={{
    fontSize: ONETRUTH.fonts.sizes['2xl'],
    fontWeight: ONETRUTH.fonts.weights.semibold,
    color: ONETRUTH.colors.textDark,
    fontFamily: ONETRUTH.fonts.heading
  }}>
    Title
  </h2>
</div>
```

**Why this is good:**
- All values come from centralized theme
- Dynamic theme switching works
- No dependency on Tailwind compilation
- Consistent across all components

#### Real-World Example: Modal Component

**Before (Broken):**

```jsx
// This caused blank screens!
export default function Modal({ children }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center">
      <div className="bg-black/50" onClick={onClose} />
      <div className="bg-white rounded-lg shadow-xl">
        {children}
      </div>
    </div>
  );
}
```

**After (Fixed):**

```jsx
import ONETRUTH from '../config/theme';

export default function Modal({ children }) {
  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: ONETRUTH.zIndex.modal
    }}>
      <div style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        zIndex: ONETRUTH.zIndex.modalBackdrop
      }} onClick={onClose} />
      <div style={{
        backgroundColor: ONETRUTH.colors.surface,
        borderRadius: ONETRUTH.borderRadius.md,
        boxShadow: ONETRUTH.shadows['2xl'],
        zIndex: ONETRUTH.zIndex.modal
      }}>
        {children}
      </div>
    </div>
  );
}
```

#### Component Checklist

Before committing any admin dashboard component, verify:

- [ ] NO `className` attributes (except for markdown rendering)
- [ ] All colors use `ONETRUTH.colors.*`
- [ ] All spacing uses `ONETRUTH.spacing.*`
- [ ] All fonts use `ONETRUTH.fonts.*`
- [ ] All borders/shadows use ONETRUTH values
- [ ] Component imports ONETRUTH theme
- [ ] No hardcoded hex colors (#ffffff, etc.)
- [ ] No hardcoded pixel values (24px, etc.)

:::info
**Note:** The main Levelith application (Landing page, Docs) can use Tailwind CSS classes. This rule applies specifically to the **admin dashboard** (`/admin` routes).
:::

---

## Troubleshooting

<details>
<summary><strong>❌ Error: CORS Errors</strong></summary>

**Symptoms:** "Access to XMLHttpRequest has been blocked by CORS policy"

**Causes:**
1. Backend CORS configuration not including frontend domain
2. API URL misconfigured
3. Missing credentials in request

**Solutions:**

```python
# backend/config.py
cors_origins: list[str] = [
    "http://localhost:5173",
    "https://levelith.online",
]
```

**Explanation:** Ensure backend CORS configuration includes all frontend domains (local and production).
</details>

<details>
<summary><strong>❌ Error: TypeScript Property Errors</strong></summary>

**Symptoms:** "Property 'X' does not exist on type 'Y'"

**Solutions:**

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

const user: User = { id: '1', name: 'John', email: 'john@example.com' };
```

**Explanation:** Define proper TypeScript interfaces for all data structures.
</details>

<details>
<summary><strong>❌ Error: Build Failures - Module Not Found</strong></summary>

**Symptoms:** "Module not found" during build

**Solutions:**

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Explanation:** Clear dependencies and reinstall to resolve version conflicts.
</details>

<details>
<summary><strong>⚠️ Warning: Hot Reload Not Working</strong></summary>

**Symptoms:** Changes not appearing in browser

**Solutions:**
1. Restart dev server: `npm run dev`
2. Clear browser cache
3. Check file watching limits on Linux: `echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf`

**Additional context:** Vite uses native ES modules and HMR for fast refresh.
</details>

<details>
<summary><strong>ℹ️ Question: When to use Tailwind vs inline styles?</strong></summary>

**Answer:** Use Tailwind for the main application (Landing, Docs). Use inline styles with ONETRUTH for the admin dashboard. This separation ensures the admin dashboard has no dependency on Tailwind compilation.

**Example:**

```tsx
// Main app - Tailwind OK
<div className="p-6 bg-surface rounded-lg">Content</div>

// Admin dashboard - Inline styles only
<div style={{
  padding: ONETRUTH.spacing.lg,
  backgroundColor: ONETRUTH.colors.surface,
  borderRadius: ONETRUTH.borderRadius.md
}}>Content</div>
```
</details>

---

## Best Practices

### ✅ DO

1. **Use TypeScript for all new code**
   ```typescript
   // ✅ GOOD - Typed function
   function fetchUser(id: string): Promise<User> {
     return apiClient.get(`/users/${id}`);
   }
   ```

2. **Import and use ONETRUTH for all styling**
   ```typescript
   // ✅ GOOD - ONETRUTH styling
   const styles = {
     button: {
       backgroundColor: ONETRUTH.colors.primary,
       padding: ONETRUTH.spacing.md,
     },
   };
   ```

3. **Write tests for new components**
   ```typescript
   // ✅ GOOD - Component test
   it('renders correctly', () => {
     render(<Button>Click me</Button>);
     expect(screen.getByText('Click me')).toBeInTheDocument();
   });
   ```

### ❌ DON'T

1. **Hardcode colors, fonts, or spacing values**
   ```typescript
   // ❌ BAD - Hardcoded values
   const styles = {
     button: {
       backgroundColor: "#3498db",
       padding: "16px",
     },
   };
   ```

2. **Use `any` type in TypeScript**
   ```typescript
   // ❌ BAD - any type
   function processData(data: any) {
     return data.value;
   }

   // ✅ GOOD - proper typing
   interface Data {
     value: string;
   }
   function processData(data: Data) {
     return data.value;
   }
   ```

3. **Use className with Tailwind for admin dashboard**
   ```jsx
   // ❌ BAD - Tailwind in admin
   <div className="bg-white p-6">Admin content</div>

   // ✅ GOOD - Inline styles in admin
   <div style={{
     backgroundColor: ONETRUTH.colors.surface,
     padding: ONETRUTH.spacing.lg
   }}>Admin content</div>
   ```

---

## Additional Resources

### Official Documentation

- 📚 [API Documentation](/docs/api/API_DOCUMENTATION.md)
- 🏗️ [Developer Guide](/docs/DEVELOPER_GUIDE.md)
- 🧪 [Backend Guide](/docs/backend/BACKEND_GUIDE.md)
- 📖 [Testing Guide](/docs/testing/TESTING_GUIDE.md)

### External Resources

- 🌐 [React Documentation](https://react.dev)
- 📖 [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- 📊 [Vite Guide](https://vitejs.dev/guide/)
- 🎨 [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Code Examples

- 💻 [Frontend Source Code](../../frontend/src)
- 🎯 [Admin Dashboard Examples](../../frontend/src/admin)
- 🧩 [Component Library](../../frontend/src/components)

### Community

- 💬 Discord: #frontend-dev
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues)
- ❓ [Discussions](https://github.com/Free-Columns/levelith-2/discussions)

---

## Related Documentation

- **Previous:** [Developer Guide](/docs/DEVELOPER_GUIDE.md)
- **Next:** [API Documentation](/docs/api/API_DOCUMENTATION.md)

**Other related documentation:**

- [Backend Guide](/docs/backend/BACKEND_GUIDE.md)
- [Testing Guide](/docs/testing/TESTING_GUIDE.md)
- [Deployment Guide](/docs/DEPLOYMENT.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via the reaction buttons below
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
