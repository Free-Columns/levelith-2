# Levelith Admin Dashboard

## Overview

A comprehensive development and debugging tool for the Levelith backend API services, built with React, Vite, and Tailwind CSS.

## Features

### ✅ Completed Features

1. **ONETRUTH Brand Integration**
   - Dynamic styling from `frontend/src/config/ONETRUTH.ts`
   - Consistent color palette, typography, and spacing
   - Theme utilities for category and status colors

2. **Data Source Management**
   - Switchable data sources (Local Mock / Server API)
   - Data source switcher in header
   - Context-based data management
   - Ready for backend API integration

3. **Mock Data System**
   - Realistic user data generation
   - All 9 experience types (Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill)
   - NAICS codes dataset
   - Statistics and analytics

4. **Comprehensive User CRUD**
   - User list with search and filtering
   - Create new users with full profile data
   - Edit existing users
   - Delete with confirmation
   - Real-time statistics (total, active, verified, inactive)

5. **NAICS Code Management**
   - Browse all NAICS codes
   - Search and filter by industry
   - Industry distribution statistics
   - Color-coded by industry type

6. **Reusable Components**
   - FormInput, FormSelect, FormTextarea, TagInput
   - Button component with multiple variants
   - Modal component for dialogs
   - Styled with ONETRUTH theme

7. **Complete Experiences CRUD** ✅ **COMPLETED**
   - Full create/edit/delete workflows for all 9 experience types
   - Hybrid form with common + type-specific fields
   - Dynamic field rendering based on category and type
   - Education types: Certificate (credential ID), Degree (major, level), Course
   - Workplace types: Gig (duration), Part-Time (job title), Full-Time (job title)
   - Skills types: Soft Skill (proficiency), Hard Skill (years, level), Native Skill (fluency)
   - NAICS code selection with full code database
   - Skills gained and achievements tracking with tag input
   - Date range validation (start/end dates)
   - Category filtering (all, education, workplace, skills)
   - Search functionality

8. **Enhanced Dashboard Visualizations** ✅ **COMPLETED**
   - User statistics overview (total, active, verified, inactive)
   - Experience distribution by category (pie chart)
   - Experience distribution by type (bar chart)
   - Industry distribution (NAICS-based)
   - **User growth over time** (area chart - last 12 months)
   - **User activity timeline** (line chart - last 30 days of logins)
   - **Top skills trending** (horizontal bar chart - top 10 skills)
   - **Geographic distribution** (progress bars showing user locations)
   - Quick action links to all management pages

9. **Backend API Integration Layer** ✅ **COMPLETED**
   - Complete API service abstraction (`src/services/apiService.js`)
   - Axios HTTP client with request/response interceptors
   - JWT authentication with automatic token refresh
   - Global error handling (401, 403, 404, 500+)
   - All CRUD operations ready for backend
   - Bulk operations support prepared
   - CSV export/import endpoints defined
   - Easy data source switching (local mock ↔ server API)
   - Seamless integration with DataSourceContext

## Project Structure

```
src/
├── components/
│   ├── DataSourceSwitcher.jsx    # Toggle between local/server data
│   ├── Modal.jsx                 # Reusable modal component
│   └── forms/
│       ├── Button.jsx            # Styled button with variants
│       ├── FormInput.jsx         # Form input with validation
│       ├── FormSelect.jsx        # Dropdown select component
│       ├── FormTextarea.jsx      # Multi-line text input
│       └── TagInput.jsx          # Tag/chip input component
├── config/
│   └── theme.js                  # ONETRUTH brand integration
├── context/
│   └── DataSourceContext.jsx    # Data management & API integration
├── data/
│   └── mockData.js               # Mock data generators & statistics
├── layouts/
│   └── AdminLayout.jsx           # Main layout with navigation
├── pages/
│   ├── Dashboard.jsx             # ✅ Analytics & visualizations
│   ├── Users.jsx                 # ✅ Complete user CRUD
│   ├── Experiences.jsx           # ✅ Complete experience CRUD (all 9 types)
│   ├── NAICSCodes.jsx            # ✅ NAICS code browser
│   ├── Settings.jsx              # Settings page (stub)
│   └── Login.jsx                 # Login page (stub)
├── services/
│   └── apiService.js             # ✅ Backend API abstraction layer
└── main.jsx                      # App entry point
```

## Getting Started

### Installation

```bash
cd dev/dev-frontend/levelith_admin_dashboard
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:5173` to view the dashboard.

### Build

```bash
npm run build
```

## Data Sources

### Local Mock Data (Default)

- Immediate testing and development
- 25 sample users with realistic profiles
- Randomly generated experiences across all 9 types
- 18 NAICS codes from various industries

### Server API (Coming Soon)

- Connect to backend API at `http://localhost:8000`
- Real-time data synchronization
- Full CRUD operations on actual data
- JWT authentication support

## API Endpoints (Planned Integration)

Based on `backend/API_DOCUMENTATION.md`:

- `POST /auth/register` - Register new user
- `POST /auth/login` - Authenticate user
- `GET /users` - List users
- `POST /users` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `GET /experiences` - List experiences
- `POST /experiences` - Create experience
- `PUT /experiences/{id}` - Update experience
- `DELETE /experiences/{id}` - Delete experience

## Experience Types

### Education
- **Certificate**: Short-term certifications
- **Degree**: Formal academic degrees
- **Course**: Individual courses and workshops

### Workplace
- **Gig**: Short-term contract work
- **PartTime**: Regular part-time employment
- **FullTime**: Primary career positions

### Skills
- **SoftSkill**: Interpersonal abilities
- **HardSkill**: Technical competencies
- **NativeSkill**: Natural talents and languages

## Technologies

- **React 18** - UI library
- **Vite 5** - Build tool
- **Tailwind CSS 3** - Utility-first CSS
- **React Router 6** - Routing
- **Axios** - HTTP client (for API integration)
- **Recharts** - Data visualization

## ONETRUTH Integration

All styling uses the ONETRUTH configuration:

```javascript
import ONETRUTH from './config/theme';

// Colors
ONETRUTH.colors.primary
ONETRUTH.colors.secondary
ONETRUTH.colors.success
ONETRUTH.colors.error

// Typography
ONETRUTH.fonts.heading
ONETRUTH.fonts.body

// Spacing
ONETRUTH.spacing.md
ONETRUTH.spacing.lg
```

## Next Steps

The following features are ready for implementation when needed:

1. **Backend Connection** (Infrastructure ready)
   - Update `.env` with `VITE_API_URL=http://localhost:8000/api/v1`
   - Start backend server
   - Switch data source to "Server API" in dashboard header
   - All API calls will automatically route to backend

2. **Advanced Features** (Optional enhancements)
   - Bulk operations UI (backend endpoints already defined)
   - CSV export/import UI (backend endpoints already defined)
   - Advanced table filtering and sorting
   - Activity logs and audit trail system
   - Real-time notifications
   - User role and permission management

3. **Production Deployment**
   - Configure production API URL
   - Set up environment variables
   - Build and deploy frontend
   - Connect to production database

## Development Notes

- All components use ONETRUTH for consistent styling
- Data source switching is implemented but server integration pending
- Form validation follows backend API requirements
- Mock data matches backend data model structure

## License

Part of the Levelith project by Semour Media Group.
