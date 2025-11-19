# Levelith Frontend

The main frontend application for Levelith - a gamified social-resume platform.

## Features

- **Landing Page**: Main entry point showcasing Levelith's value proposition
- **Documentation Wiki**: Dynamic documentation viewer with sidebar navigation and search
- **Admin Dashboard**: Comprehensive admin panel for managing users, experiences, and NAICS codes

## Architecture

### Technology Stack

- **Framework**: React 18.2 with TypeScript
- **Build Tool**: Vite 5.0
- **Routing**: React Router DOM 6.22
- **HTTP Client**: Axios 1.6
- **Charts**: Recharts 2.9
- **Styling**: TailwindCSS + ONETRUTH design system

### Project Structure

```
frontend/
├── src/
│   ├── admin/                    # Admin dashboard (integrated from dev)
│   │   ├── pages/                # Admin pages (Dashboard, Users, Experiences, etc.)
│   │   ├── components/           # Reusable admin components
│   │   ├── services/             # API service layer
│   │   ├── context/              # React context (DataSource)
│   │   ├── layouts/              # Admin layout wrapper
│   │   └── data/                 # Mock data (fallback)
│   ├── pages/                    # Main application pages
│   │   ├── Landing.tsx           # Home/landing page
│   │   └── Docs.tsx              # Documentation viewer
│   ├── config/                   # Configuration files
│   │   └── ONETRUTH.ts           # Design system (colors, fonts, spacing)
│   ├── App.tsx                   # Main app with routing
│   ├── main.tsx                  # Application entry point
│   └── index.css                 # Global styles
├── index.html                    # HTML template
├── vite.config.ts                # Vite configuration
├── tsconfig.json                 # TypeScript configuration
├── package.json                  # Dependencies and scripts
└── .env                          # Environment variables

```

## Routes

- `/` - Landing page
- `/docs` - Documentation index
- `/docs/:docPath` - Specific documentation page
- `/admin` - Admin dashboard
- `/admin/users` - User management
- `/admin/experiences` - Experience management
- `/admin/naics` - NAICS code management
- `/admin/settings` - Admin settings

## Development

### Prerequisites

- Node.js 18+
- npm 9+

### Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm start
```

### Environment Variables

Create a `.env.local` file for local development:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Levelith
VITE_ENVIRONMENT=development
```

For production, the `.env` file is configured to use the hosted backend:

```env
VITE_API_URL=https://levelith-backend.onrender.com/api/v1
```

## Design System

All components use the **ONETRUTH** configuration located at `src/config/ONETRUTH.ts`.

### ONETRUTH Principles

- **Single Source of Truth**: All colors, fonts, spacing defined in one place
- **No Hardcoded Values**: Components must import from ONETRUTH
- **Consistency**: Ensures uniform branding across the entire application

### Usage Example

```typescript
import { ONETRUTH } from '@/config/ONETRUTH';

const styles = {
  container: {
    backgroundColor: ONETRUTH.colors.primary,
    padding: ONETRUTH.spacing.lg,
    borderRadius: ONETRUTH.borderRadius.md,
  },
  title: {
    fontFamily: ONETRUTH.fonts.heading,
    fontSize: ONETRUTH.fonts.sizes['3xl'],
    color: ONETRUTH.colors.textDark,
  },
};
```

## Admin Dashboard

The admin dashboard was integrated from `dev/dev-frontend/levelith_admin_dashboard/` and now lives at `/admin/*` routes.

### Key Features

- **Data Source Switching**: Can toggle between SERVER (PostgreSQL) and LOCAL (mock data)
- **User Management**: CRUD operations for users
- **Experience Management**: Manage all experience types
- **NAICS Code Browser**: Search and view industry classifications
- **Statistics Dashboard**: Real-time analytics and charts

### Default Configuration

- **Data Source**: SERVER (connected to hosted PostgreSQL database)
- **API URL**: `https://levelith-backend.onrender.com/api/v1`

## Testing

```bash
# Run unit tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:ci

# Run E2E tests
npm run test:e2e
```

## Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Type check
npm run type-check

# Run all checks (CI)
npm run ci
```

## Deployment

The frontend is deployed to Render.com and accessible at:
- Production: https://levlith.online

### Build Process

```bash
# Production build
npm run build

# Output: dist/
```

## Documentation

Documentation is stored in `/docs/` and organized by category:

- **Core**: Project manifest, AI agent rules, known issues
- **Development**: Development priorities, codebase analysis, guides
- **API**: API documentation
- **Backend**: Backend-specific documentation

The documentation viewer (`/docs`) provides:
- Wiki-style sidebar navigation
- Search functionality
- Category grouping
- Responsive design

## Contributing

When adding new features:

1. Follow the AI Agent Golden Rules (see `/docs/core/AI_AGENT_GOLDEN_RULES.md`)
2. Use ONETRUTH for all styling
3. Write tests for new components
4. Update documentation as needed
5. Ensure TypeScript types are properly defined

## Architecture Decisions

### Why Integrated Admin Dashboard?

The admin dashboard was moved from `dev/dev-frontend/` to `frontend/src/admin/` to:
- Consolidate the codebase
- Share dependencies and build tooling
- Simplify deployment
- Enable code reuse between admin and main app

### Why ONETRUTH Design System?

- Ensures brand consistency across all components
- Simplifies theme updates (change once, apply everywhere)
- Prevents hardcoded style values
- Makes the codebase more maintainable

### Why Vite?

- Fast development server with HMR
- Optimized production builds
- Native TypeScript support
- Modern, actively maintained

## License

Copyright © 2025 Semour Media Group
