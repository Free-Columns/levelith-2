# Levelith Admin Panel Integration Guide

---
title: "Levelith Admin Panel Integration Guide"
description: "Complete guide for setting up and using the admin dashboard with PostgreSQL database integration and full CRUD operations."
category: "guides"
tags: ["admin-panel", "dashboard", "backend", "frontend", "database", "crud", "naics", "users", "experiences"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 20
relatedPages:
  - "/docs/dev/ADMIN_DASHBOARD_IMPLEMENTATION.md"
  - "/docs/api/API_DOCUMENTATION.md"
  - "/docs/deployment/DATABASE_SETUP_NOTES.md"
nextPage: "/docs/dev/ADMIN_DASHBOARD_IMPLEMENTATION.md"
prevPage: "/docs/dev/CI_CD_GUIDE.md"
searchKeywords:
  - "admin panel"
  - "dashboard"
  - "crud operations"
  - "user management"
  - "experience management"
  - "naics codes"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Levelith Admin Panel Integration Guide

:::danger
**⚠️ DEPRECATED - November 20, 2025**

This guide describes the OLD admin dashboard which has been DEPRECATED and moved to `_deprecated/levelith_admin_dashboard_OLD/`.

**DO NOT USE THE OLD DASHBOARD** - It has critical issues:
- ❌ CRUD operations broken (blank white pages)
- ❌ Routing incorrect (/users instead of /admin/users)
- ❌ Mock data everywhere
- ❌ No TypeScript type safety

**NEW DASHBOARD:** See [ADMIN_DASHBOARD_REFACTOR_V2.md](./ADMIN_DASHBOARD_REFACTOR_V2.md) for the modern rebuild (Plan C).

**Current Status:** Planning complete - 165 tasks documented - Ready for implementation
:::

> **TL;DR (OUTDATED):** Complete setup guide for the Levelith admin dashboard with full CRUD operations for users, experiences, and NAICS codes, backed by PostgreSQL and featuring real-time analytics.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 20 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Database Seeding](#database-seeding)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Using the Admin Panel](#using-the-admin-panel)
- [NAICS Code Management](#naics-code-management)
- [Common Workflows](#common-workflows)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)
- [Additional Resources](#additional-resources)

---

## Overview

:::danger
**DEPRECATED:** This section describes the OLD admin panel at `_deprecated/levelith_admin_dashboard_OLD/`.

**NEW LOCATION:** `frontend/src/admin/` (being refactored - see [ADMIN_DASHBOARD_REFACTOR_V2.md](./ADMIN_DASHBOARD_REFACTOR_V2.md))
:::

The Levelith admin panel ~~is~~ **was** a fully functional dashboard that manages users, experiences, and NAICS codes through a backend API connected to PostgreSQL.

**Old Admin Panel Location:** `_deprecated/levelith_admin_dashboard_OLD/` (deprecated)
**New Admin Panel Location:** `frontend/src/admin/` (in refactor - Plan C)

:::info
**Prerequisites:** PostgreSQL database, Python 3.11+, Node.js 18+, FastAPI backend
:::

:::warning
**For Current Development:** Refer to [ADMIN_DASHBOARD_REFACTOR_V2.md](./ADMIN_DASHBOARD_REFACTOR_V2.md) for the new implementation plan. This guide is kept for historical reference only.
:::

---

## Features

### 👥 User Management

- ✅ View all users with search and filtering
- ✅ Create new users with profiles
- ✅ Edit user information
- ✅ Delete users (with confirmation)
- ✅ View user statistics (active, verified, inactive)

### 📚 Experience Management

- ✅ Create/edit/delete all 9 experience types:
  - **Education:** Certificate, Degree, Course
  - **Workplace:** Gig, Part-Time, Full-Time
  - **Skills:** Soft Skill, Hard Skill, Native Skill
- ✅ Assign NAICS codes to experiences
- ✅ Track skills gained and achievements
- ✅ Set date ranges and current status

### 📊 Dashboard Analytics

- ✅ User growth over time
- ✅ Experience distribution by category/type
- ✅ Industry distribution (NAICS-based)
- ✅ Top skills trending
- ✅ Geographic distribution
- ✅ User activity timeline

### 🏢 NAICS Code Management (Full CRUD)

- ✅ Browse all 2222+ industry codes with pagination
- ✅ Search and filter by code/title/description
- ✅ **Edit NAICS codes** with admin-specific fields:
  - Tags (for organization and categorization)
  - Custom Category (admin-defined classification)
  - Admin Notes (internal comments)
- ✅ **Delete NAICS codes** (with confirmation)
- ✅ View industry distribution
- ✅ Server-side pagination (50 items/page)

---

## Quick Start

Follow these 3 steps to get the admin panel running:

### Step 1: Seed the Database with Mock Data

First, populate your PostgreSQL database with test data:

```bash
# From project root
cd backend

# Seed with 25 users (default)
python seed_db.py

# Or customize:
python seed_db.py --users 50 --verbose
```

**What this does:**
- Creates 25 realistic users (or your specified number)
- Generates 2-8 experiences per user (all 9 types)
- Assigns NAICS codes
- Sets realistic dates and profiles

**Expected Output:**
```
==================================================================
DATABASE SEEDING COMPLETE!
==================================================================
📊 Statistics:
   Users created: 25
   Experiences created: 127
   Average experiences per user: 5.1
==================================================================
🎉 You can now use the admin panel to view and manage this data!
```

:::tip
**Pro Tip:** Use `--verbose` flag to see detailed output for each user created. This helps verify data is being generated correctly.
:::

---

### Step 2: Start the Backend API

Start your FastAPI backend server:

```bash
# From project root
cd backend

# Start the API server
uvicorn main:app --reload
```

**Verify it's running:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "development"
}
```

**API Documentation:** http://localhost:8000/docs

:::info
**Note:** The `--reload` flag enables auto-reload during development. Remove it for production.
:::

---

### Step 3: Start the Admin Panel

In a **new terminal**, start the admin dashboard:

```bash
# From project root
cd dev/dev-frontend/levelith_admin_dashboard

# Install dependencies (first time only)
npm install

# Start the admin panel
npm run dev
```

**Access the Admin Panel:** http://localhost:5173

:::success
**Success!** You should now see the admin dashboard with seeded data displayed.
:::

---

## Database Seeding

### Basic Usage

```bash
# Seed with default settings (25 users)
python backend/seed_db.py

# Seed with custom number of users
python backend/seed_db.py --users 100

# Clear existing data and reseed
python backend/seed_db.py --clear --users 50

# Verbose output (show each user created)
python backend/seed_db.py --verbose
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--users N` or `-u N` | Create N users (default: 25) |
| `--clear` or `-c` | Clear all existing data first (WARNING: destroys data!) |
| `--verbose` or `-v` | Show detailed logging |
| `--help` or `-h` | Show help message |

### What Gets Created

**Per User:**
- Unique username and email
- Hashed password: `TestPassword123!`
- Random active/verified status
- Profile data (bio, location, website)
- Created/updated timestamps
- Last login (random recent date)

**Per Experience (2-8 per user):**
- Random type (from all 9 types)
- Appropriate category
- Title and description
- Random NAICS code
- Start date (random past date)
- End date (or current if ongoing)
- Organization (for Education/Workplace)
- Location (for Education/Workplace)
- Skills gained (2-5 random skills)
- Type-specific metadata

:::warning
**Warning:** Using `--clear` flag will permanently delete all existing users and experiences. Use with caution!
:::

---

## Backend Setup

### Connecting Admin Panel to Backend

The admin panel needs to know where your backend API is running.

#### Option 1: Environment Variable (Recommended)

Create `.env` file in `dev/dev-frontend/levelith_admin_dashboard/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Restart the admin panel after creating this file.

#### Option 2: Switch Data Source in UI

1. Open admin panel: http://localhost:5173
2. Look for **"Data Source"** switcher in the header
3. Click to toggle between:
   - **"Local Mock"** - Uses fake data (for testing UI)
   - **"Server API"** - Uses your backend API (real database)

---

## Frontend Setup

### Environment Configuration

**Required Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

### Data Source Modes

**Local Mock Data:**
- Fake data generated in browser
- No backend required
- Perfect for UI testing
- Changes don't persist

**Server API:**
- Real data from PostgreSQL
- Requires backend running
- Changes persist in database
- Full CRUD operations

---

## Using the Admin Panel

### Dashboard (Home)

- Overview statistics
- Charts and graphs
- Quick action links

### Users Page

```
http://localhost:5173/users
```

**Features:**
- Search by username or email
- Filter by status (active/inactive/verified)
- Click "New User" to create
- Click row to view details
- Edit or delete from action buttons

**Creating a User:**
1. Click "New User"
2. Fill in required fields:
   - Username (unique)
   - Email (unique)
   - Password
   - Display name
   - Bio (optional)
   - Location (optional)
3. Click "Create User"

### Experiences Page

```
http://localhost:5173/experiences
```

**Features:**
- Filter by category (Education, Workplace, Skills)
- Filter by type (9 experience types)
- Search by title
- Create new experiences
- Edit or delete existing ones

**Creating an Experience:**
1. Click "New Experience"
2. Select category (Education/Workplace/Skills)
3. Select specific type (Certificate, Degree, etc.)
4. Fill in fields (fields change based on type):
   - Title
   - Description
   - NAICS code
   - Organization
   - Start/End dates
   - Type-specific fields
5. Add skills gained (optional)
6. Click "Create Experience"

**Type-Specific Fields:**

| Type | Extra Fields |
|------|-------------|
| Certificate | Credential ID |
| Degree | Major, Level (Bachelor/Master/PhD) |
| Course | - |
| Gig/Part-Time/Full-Time | Job title, Company |
| Hard Skill | Proficiency level, Years of experience |
| Soft Skill | Proficiency level |
| Native Skill | Fluency level |

---

## NAICS Code Management

### NAICS Codes Page

```
http://localhost:5173/naics
```

**Full CRUD operations for managing NAICS industry codes**

### Features

- Browse all 2222+ NAICS codes with server-side pagination
- Search by code, title, or description
- Filter by category and hierarchical level
- Edit admin-specific fields (tags, category, notes)
- Delete codes (with warning confirmation)

### Viewing NAICS Codes

1. Navigate to NAICS page
2. Use search box to find specific codes
3. Pagination shows 50 codes per page
4. View Tags column for admin-defined tags

### Editing a NAICS Code

1. Click "Edit" button in Actions column
2. Modal opens with admin fields:
   - **Tags**: Comma-separated tags for organization (e.g., "tech, high-demand")
   - **Custom Category**: Your own classification system
   - **Admin Notes**: Internal notes and comments
3. Click "Save Changes"
4. Changes persist immediately

### Deleting a NAICS Code

1. Click "Delete" button in Actions column
2. Confirmation modal warns about permanent deletion
3. Click "Delete" to confirm
4. Code removed from database

:::danger
**Critical:** Official NAICS fields (code, title, description, category) cannot be edited. Only admin-specific fields can be modified.
:::

---

## Common Workflows

### Workflow 1: Add a New User with Experiences

1. **Create User**
   - Go to Users page
   - Click "New User"
   - Fill in details
   - Submit

2. **Add Experiences**
   - Go to Experiences page
   - Click "New Experience"
   - Select user from dropdown
   - Fill in experience details
   - Submit
   - Repeat for multiple experiences

### Workflow 2: Bulk Testing with Seed Data

1. **Clear and Reseed**
   ```bash
   python backend/seed_db.py --clear --users 50
   ```

2. **Restart Backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Refresh Admin Panel**
   - Reload http://localhost:5173
   - Should see all 50 users

### Workflow 3: Export/Import Data

**Export (coming soon):**
- Admin panel will support CSV export
- Backend endpoints already defined

**Import:**
- Use `seed_db.py` for bulk import
- Or use API endpoints directly

---

## API Reference

### User Endpoints

```
GET    /api/v1/users/              # List all users
POST   /api/v1/users/              # Create user
GET    /api/v1/users/{id}          # Get user by ID
PUT    /api/v1/users/{id}          # Update user
DELETE /api/v1/users/{id}          # Delete user
```

### Experience Endpoints

```
GET    /api/v1/experiences/        # List all experiences
POST   /api/v1/experiences/        # Create experience
GET    /api/v1/experiences/{id}    # Get experience by ID
PUT    /api/v1/experiences/{id}    # Update experience
DELETE /api/v1/experiences/{id}    # Delete experience
```

### NAICS Endpoints

```
GET    /api/v1/naics/              # List NAICS codes
GET    /api/v1/naics/paginated     # Paginated search with filters
GET    /api/v1/naics/{code}        # Get specific code
PATCH  /api/v1/naics/{code}        # Update admin fields (tags, category, notes)
DELETE /api/v1/naics/{code}        # Delete code (permanent)
```

**Example - Update NAICS Code:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/naics/541511" \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["technology", "software", "high-demand"],
    "custom_category": "Tech Priority",
    "admin_notes": "Popular code for software development companies"
  }'
```

**Example - Paginated Search:**
```bash
curl "http://localhost:8000/api/v1/naics/paginated?q=computer&page=1&page_size=50"
```

### Health Endpoints

```
GET    /health                     # Basic health check
GET    /health/details             # Detailed health with DB info
```

**Full API Documentation:** http://localhost:8000/docs

---

## Troubleshooting

<details>
<summary><strong>❌ Error: Database connection failed</strong></summary>

**Symptoms:** Cannot connect to PostgreSQL

**Causes:**
1. Database not running
2. Incorrect DATABASE_URL in .env
3. Network/firewall issues

**Solutions:**
```bash
# Check backend/.env has correct DATABASE_URL
# Verify database is running (check Render dashboard)
# Test connection
python backend/init_db.py --check
```

**Explanation:** The backend needs a valid PostgreSQL connection to function.
</details>

<details>
<summary><strong>❌ Error: Module not found</strong></summary>

**Symptoms:** Python import errors

**Solutions:**
```bash
# Install missing dependencies
pip install -r backend/requirements.txt
```

**Additional context:** Ensure you're using Python 3.11+
</details>

<details>
<summary><strong>⚠️ Warning: Admin panel shows "No data"</strong></summary>

**Symptoms:** Dashboard displays empty tables

**Solutions:**
1. Check backend is running: `http://localhost:8000/health`
2. Check admin panel data source setting (toggle in header)
3. Check browser console for CORS errors
4. Verify `.env` file has correct API URL

**Additional context:** Most common cause is backend not running or data source set to LOCAL with no mock data.
</details>

<details>
<summary><strong>❌ Error: CORS errors in browser console</strong></summary>

**Symptoms:** Browser blocks requests to backend

**Solutions:**
Update `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://localhost:5173"]
```

Then restart backend.

**Explanation:** CORS policy prevents frontend from accessing backend on different origin.
</details>

<details>
<summary><strong>❌ Error: Username already exists</strong></summary>

**Symptoms:** Cannot create user with duplicate username

**Solutions:**
- Use unique username/email
- Or clear database: `python backend/seed_db.py --clear`

**Additional context:** Usernames and emails must be unique in the database.
</details>

---

## Production Deployment

### Backend (Render)

Already configured! Just set environment variables:

```env
DATABASE_URL=postgresql://levelith_user:...@dpg-....render.com/levelith
SECRET_KEY=08a4ab222554f29ae4a0eb7d00482fa5a79f46f2617ed9cf6453347dc3a8461f
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://levelith-admin.onrender.com","https://levlith.online"]
```

### Frontend (Render or Vercel)

1. Build command: `npm run build`
2. Environment variable: `VITE_API_URL=https://your-backend.onrender.com/api/v1`
3. Deploy `dev/dev-frontend/levelith_admin_dashboard` directory

### Seed Production Database

```bash
# Set production DATABASE_URL
export DATABASE_URL="postgresql://..."

# Seed production
python backend/seed_db.py --users 10

# Or seed staging first for testing
```

:::warning
**Warning:** Always test on staging environment before seeding production database.
:::

---

## Additional Resources

### Official Documentation

- 📚 [Admin Dashboard Implementation](/docs/dev/ADMIN_DASHBOARD_IMPLEMENTATION.md)
- 🏗️ [API Documentation](/docs/api/API_DOCUMENTATION.md)
- 🧪 [Database Setup](/docs/deployment/DATABASE_SETUP_NOTES.md)

### External Resources

- 🌐 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📖 [React Documentation](https://react.dev/)
- 📊 [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Code Examples

- 💻 [Seed Script](https://github.com/Free-Columns/levelith-2/blob/main/backend/seed_db.py)
- 🎯 [Admin Dashboard](https://github.com/Free-Columns/levelith-2/tree/main/dev/dev-frontend/levelith_admin_dashboard)

---

## Related Documentation

- **Next:** [Admin Dashboard Implementation](/docs/dev/ADMIN_DASHBOARD_IMPLEMENTATION.md)
- **Previous:** [CI/CD Guide](/docs/dev/CI_CD_GUIDE.md)

**Other related documentation:**

- [Project Manifest](/docs/core/MANIFEST.md)
- [Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)
- [Recent Updates](/docs/dev/RECENT_UPDATES.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via the reaction buttons below
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 2.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
