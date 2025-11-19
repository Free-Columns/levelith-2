# Frontend Development Guide

**Last Updated:** 2025-11-19
**Version:** 1.0
**Maintained By:** Levelith Development Team

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [ONETRUTH Branding System](#onetruth-branding-system)
6. [Creating New Pages](#creating-new-pages)
7. [Updating Existing Pages](#updating-existing-pages)
8. [Component Development](#component-development)
9. [State Management](#state-management)
10. [API Integration](#api-integration)
11. [Routing](#routing)
12. [Styling Guidelines](#styling-guidelines)
13. [Testing](#testing)
14. [Build and Deployment](#build-and-deployment)
15. [Common Patterns](#common-patterns)
16. [Troubleshooting](#troubleshooting)

---

## Overview

The Levelith frontend is a modern React application built with TypeScript, focusing on user experience, performance, and maintainability. It features:

- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **React Router v6** for client-side routing
- **ONETRUTH** branding system for consistent theming
- **Axios** for API communication
- **Recharts** for data visualization
- **React Markdown** for documentation rendering

### Key Principles

1. **Type Safety**: Everything is typed with TypeScript
2. **Consistency**: All styling uses ONETRUTH configuration
3. **Reusability**: Components are modular and composable
4. **Performance**: Lazy loading, code splitting, and optimization
5. **Accessibility**: ARIA labels, keyboard navigation, semantic HTML

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
| **Tailwind CSS** | 3.4.0 | Utility-first CSS (optional) |
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
│   ├── components/            # Reusable UI components (future)
│   ├── hooks/                 # Custom React hooks (future)
│   ├── services/              # API services (future)
│   ├── utils/                 # Utility functions (future)
│   ├── types/                 # TypeScript type definitions (future)
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
│       │   ├── theme.js      # ⚠️ TODO: Merge with ONETRUTH
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

ONETRUTH is the **single source of truth** for all branding, theming, and styling in the Levelith application. It ensures:

- ✅ Consistent colors, fonts, spacing across all components
- ✅ Easy theme updates (change once, apply everywhere)
- ✅ No hardcoded values scattered throughout the codebase

**Location:** `/frontend/src/config/ONETRUTH.ts`

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
      // ... up to 5xl
    },

    weights: {
      light: 300,
      normal: 400,
      // ... up to extrabold
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
    // ... up to 4xl
  },

  // Border Radius
  borderRadius: {
    sm: "4px",
    md: "8px",
    lg: "12px",
    // ... up to full
  },

  // Shadows
  shadows: {
    sm: "0 1px 2px rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px rgba(0, 0, 0, 0.1)",
    // ... up to 2xl
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
    // ... more industries
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
        {/* ... other routes */}
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

---

## Updating Existing Pages

### Example: Updating the Landing Page

1. **Open the file:** `/frontend/src/pages/Landing.tsx`

2. **Make changes using ONETRUTH:**

```typescript
// Landing.tsx

const styles = {
  hero: {
    backgroundColor: ONETRUTH.colors.primary,  // Use ONETRUTH
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

3. **Test locally:**

```bash
npm run dev
```

4. **Build for production:**

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

### 3. CSS Classes for Complex Styling

For markdown or complex layouts, use CSS classes:

```typescript
const markdownStyles = `
  .markdown-content h1 {
    font-size: ${ONETRUTH.fonts.sizes['3xl']};
    color: ${ONETRUTH.colors.textDark};
  }
`;

return (
  <>
    <style>{markdownStyles}</style>
    <div className="markdown-content">
      {/* content */}
    </div>
  </>
);
```

### 4. Responsive Design

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

Environment variables in Render:
- `VITE_API_URL`: Backend API URL

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

## Troubleshooting

### Common Issues

#### 1. CORS Errors

**Problem:** "Access to XMLHttpRequest has been blocked by CORS policy"

**Solution:** Ensure backend CORS configuration includes your frontend domain:

```python
# backend/config.py
cors_origins: list[str] = [
    "http://localhost:5173",
    "https://levelith.online",
]
```

#### 2. TypeScript Errors

**Problem:** "Property 'X' does not exist on type 'Y'"

**Solution:** Define proper interfaces:

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

const user: User = { id: '1', name: 'John', email: 'john@example.com' };
```

#### 3. Build Failures

**Problem:** "Module not found" during build

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 4. Hot Reload Not Working

**Solution:**
```bash
# Restart dev server
npm run dev
```

---

## Best Practices

### DO ✅

- Use TypeScript for all new code
- Import and use ONETRUTH for all styling
- Write tests for new components
- Use semantic HTML (header, main, nav, etc.)
- Add ARIA labels for accessibility
- Handle loading and error states
- Use environment variables for API URLs
- Keep components small and focused (<300 lines)
- Document complex logic with comments

### DON'T ❌

- Hardcode colors, fonts, or spacing values
- Use `any` type in TypeScript
- Ignore TypeScript errors
- Skip error handling for API calls
- Create god components (>500 lines)
- Duplicate ONETRUTH values locally
- Commit `.env.local` to git
- Use inline event handlers for complex logic

---

## Quick Reference

### File Locations

- **ONETRUTH Config:** `/frontend/src/config/ONETRUTH.ts`
- **Pages:** `/frontend/src/pages/`
- **Admin Pages:** `/frontend/src/admin/pages/`
- **API Service:** `/frontend/src/admin/services/apiService.js`
- **Environment:** `.env.local` (create if missing)

### NPM Scripts

```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run start        # Preview build
npm run test         # Unit tests
npm run test:e2e     # E2E tests
npm run lint         # Lint code
npm run format       # Format code
npm run type-check   # TypeScript check
```

### Import Paths

```typescript
import { ONETRUTH } from '../config/ONETRUTH';
import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
```

---

## Getting Help

- **Documentation:** Read this guide and [docs/README.md](../README.md)
- **Code Examples:** Check existing pages (`Landing.tsx`, `Docs.tsx`)
- **ONETRUTH Reference:** See `/frontend/src/config/ONETRUTH.ts`
- **API Documentation:** See [docs/api/API_DOCUMENTATION.md](../api/API_DOCUMENTATION.md)

---

**End of Frontend Development Guide**
