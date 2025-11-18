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

### 🚧 In Progress

1. **Experiences CRUD** (Stub created)
   - Placeholder for comprehensive experience management
   - Supports all 9 experience types
   - Category-based organization

2. **Dashboard** (Stub created)
   - Placeholder for data visualizations
   - Statistics overview
   - Charts and graphs (using Recharts)

## Project Structure

```
src/
├── components/
│   ├── DataSourceSwitcher.jsx
│   ├── Modal.jsx
│   └── forms/
│       ├── Button.jsx
│       ├── FormInput.jsx
│       ├── FormSelect.jsx
│       ├── FormTextarea.jsx
│       └── TagInput.jsx
├── config/
│   └── theme.js                 # ONETRUTH integration
├── context/
│   └── DataSourceContext.jsx    # Data management
├── data/
│   └── mockData.js               # Mock data generators
├── layouts/
│   └── AdminLayout.jsx           # Main layout with navigation
├── pages/
│   ├── Dashboard.jsx             # Statistics and visualizations
│   ├── Users.jsx                 # User CRUD interface
│   ├── Experiences.jsx           # Experience CRUD (stub)
│   ├── NAICSCodes.jsx            # NAICS code browser
│   ├── Settings.jsx              # Settings page (stub)
│   └── Login.jsx                 # Login page (stub)
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

1. **Complete Experiences CRUD**
   - Build full experience management interface
   - Type-specific form fields
   - NAICS code integration

2. **Dashboard Visualizations**
   - User activity charts
   - Experience distribution graphs
   - Industry analytics
   - Growth trends

3. **Backend Integration**
   - Connect to FastAPI backend
   - Implement JWT authentication
   - Real-time data synchronization
   - Error handling and validation

4. **Advanced Features**
   - Bulk operations
   - CSV export/import
   - Advanced filtering and sorting
   - Activity logs and audit trail

## Development Notes

- All components use ONETRUTH for consistent styling
- Data source switching is implemented but server integration pending
- Form validation follows backend API requirements
- Mock data matches backend data model structure

## License

Part of the Levelith project by Semour Media Group.
