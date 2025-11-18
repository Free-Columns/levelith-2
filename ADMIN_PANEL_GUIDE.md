# Levelith Admin Panel Integration Guide

**Complete guide for using the admin dashboard with your PostgreSQL database**

---

## 🎯 Overview

You have a **fully functional admin panel** that can manage users and experiences through your backend API! This guide shows you how to set everything up.

**Admin Panel Location:** `dev/dev-frontend/levelith_admin_dashboard/`

---

## ✨ What Can You Do With the Admin Panel?

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

### 🏢 NAICS Code Browser
- ✅ Browse all industry codes
- ✅ Search and filter by industry
- ✅ View industry distribution

---

## 🚀 Quick Start (3 Steps)

### Step 1: Seed the Database with Mock Data

First, let's populate your PostgreSQL database with test data:

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

---

## 🔌 Connecting Admin Panel to Backend

The admin panel needs to know where your backend API is running.

### Option 1: Environment Variable (Recommended)

Create `.env` file in `dev/dev-frontend/levelith_admin_dashboard/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Restart the admin panel after creating this file.

### Option 2: Switch Data Source in UI

1. Open admin panel: http://localhost:5173
2. Look for **"Data Source"** switcher in the header
3. Click to toggle between:
   - **"Local Mock"** - Uses fake data (for testing UI)
   - **"Server API"** - Uses your backend API (real database)

---

## 📖 Using the Admin Panel

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

### NAICS Codes Page
```
http://localhost:5173/naics
```

Browse all NAICS industry codes, search, and filter by industry category.

---

## 🛠️ Database Seeding Reference

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

### Generated Data Examples

**Users:**
- `johnsmith0` / `john.smith0@example.com`
- `sarahjohnson1` / `sarah.johnson1@example.com`
- Password for all: `TestPassword123!`

**Experiences:**
- "AWS Certified Solutions Architect" (Certificate)
- "Senior Software Engineer at Tech Corp" (Full-Time)
- "Python" (Hard Skill)
- "Master of Science in Data Science" (Degree)

---

## 🔐 Testing Login

All seeded users have the same password for easy testing:

**Password:** `TestPassword123!`

**Login via API:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johnsmith0",
    "password": "TestPassword123!"
  }'
```

---

## 📊 Verification Steps

### 1. Verify Database Seeding
```bash
# Check database
cd backend
python init_db.py --check

# Count users
python -c "from database import get_db_context; from models.db_models import UserDB; \
           with get_db_context() as db: print(f'Users: {db.query(UserDB).count()}')"
```

### 2. Verify Backend API
```bash
# Health check
curl http://localhost:8000/health

# Get users
curl http://localhost:8000/api/v1/users/

# Get experiences
curl http://localhost:8000/api/v1/experiences/
```

### 3. Verify Admin Panel
1. Open http://localhost:5173
2. Check Dashboard shows statistics
3. Navigate to Users page - should see all seeded users
4. Navigate to Experiences page - should see all experiences
5. Try creating a new user
6. Try editing an existing user

---

## 🐛 Troubleshooting

### "Database connection failed"
**Problem:** Cannot connect to PostgreSQL

**Solutions:**
1. Check `backend/.env` has correct DATABASE_URL
2. Verify database is running (check Render dashboard)
3. Test connection: `python backend/init_db.py --check`

### "Module not found" errors
**Problem:** Missing Python dependencies

**Solution:**
```bash
pip install -r backend/requirements.txt
```

### Admin panel shows "No data"
**Problem:** Not connected to backend or backend not running

**Solutions:**
1. Check backend is running: `http://localhost:8000/health`
2. Check admin panel data source setting (toggle in header)
3. Check browser console for CORS errors
4. Verify `.env` file has correct API URL

### CORS errors in browser console
**Problem:** Backend rejecting frontend requests

**Solution:**
Update `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://localhost:5173"]
```

Then restart backend.

### "Username already exists"
**Problem:** Trying to create duplicate user

**Solution:**
- Use unique username/email
- Or clear database: `python backend/seed_db.py --clear`

---

## 🎨 Admin Panel Features Reference

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

### Available Pages

| Page | Route | Features |
|------|-------|----------|
| Dashboard | `/` | Statistics, charts, quick actions |
| Users | `/users` | User CRUD, search, filter |
| Experiences | `/experiences` | Experience CRUD, type-specific forms |
| NAICS Codes | `/naics` | Browse industry codes |
| Settings | `/settings` | Configuration (stub) |

---

## 🔄 Common Workflows

### Workflow 1: Add a New User with Experiences

1. **Create User**
   - Go to Users page
   - Click "New User"
   - Fill in details
   - Submit

2. **Add Experiences**
   - Go to Experiences page
   - Click "New Experience"
   - Select user from dropdown (or it auto-selects if you just created one)
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

## 📝 API Endpoints Reference

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
GET    /api/v1/naics/{code}        # Get specific code
```

### Health Endpoints
```
GET    /health                     # Basic health check
GET    /health/details             # Detailed health with DB info
```

**Full API Documentation:** http://localhost:8000/docs

---

## 🚀 Production Deployment

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

---

## 🎉 You're Ready!

**Complete Flow:**

1. ✅ Database configured (PostgreSQL on Render)
2. ✅ Seeding script created (`backend/seed_db.py`)
3. ✅ Admin panel exists (`dev/dev-frontend/levelith_admin_dashboard/`)
4. ✅ Backend API ready (`backend/main.py`)

**Next Steps:**

```bash
# 1. Seed the database
python backend/seed_db.py

# 2. Start backend
cd backend && uvicorn main:app --reload

# 3. Start admin panel (new terminal)
cd dev/dev-frontend/levelith_admin_dashboard && npm run dev

# 4. Open browser
# http://localhost:5173
```

**Now you can:**
- View all seeded users and experiences
- Create new users through the UI
- Add experiences to users
- Edit and delete data
- See real-time statistics and analytics

---

## 📚 Additional Resources

- **API Documentation:** [docs/api/API_DOCUMENTATION.md](docs/api/API_DOCUMENTATION.md)
- **Database Setup:** [DATABASE_SETUP_NOTES.md](DATABASE_SETUP_NOTES.md)
- **Project Manifest:** [docs/core/MANIFEST.md](docs/core/MANIFEST.md)
- **Deployment Guide:** [docs/deployment/RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md)

---

**Questions or issues?** Check the troubleshooting section or review the logs from the backend/frontend consoles.

**Happy Testing! 🚀**
