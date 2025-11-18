# Admin Panel Quick Start Guide

## ✅ Fixed: Dashboard Loading Issue

**Problem:** Dashboard was showing white screen with "Cannot read properties of undefined" error.

**Solution:** Fixed async data loading in Dashboard component. The dashboard now properly waits for statistics to load before rendering.

---

## 🚀 How to Access the Admin Panel

### No Login Required for Development!

The admin panel works **without authentication** when using local mock data. Just:

1. **Navigate to:** http://localhost:5173
2. **See the Dashboard immediately** - no login needed!

The login page exists but is a stub for future development.

---

## 📊 Using the Admin Panel

### Navigation

Click the sidebar links:

- **📊 Dashboard** - Home page with analytics
- **👥 Users** - Manage users
- **📚 Experiences** - Manage experiences
- **🏢 NAICS** - Browse industry codes
- **⚙️ Settings** - Configuration

### Data Source Toggle

Look at the **top right corner** of the navigation bar:

- **"Local Mock"** - Uses fake data (no backend needed)
- **"Server API"** - Uses your PostgreSQL database (requires backend running)

**Default:** Local Mock

---

## 🎯 Quick Actions

### View Dashboard (Current Page)
- See user statistics
- View charts and graphs
- Check experience distribution
- Monitor user activity

### Manage Users
1. Click **"Users"** in sidebar
2. Click **"New User"** button to create
3. Click any row to view details
4. Use **Edit** or **Delete** buttons

### Manage Experiences
1. Click **"Experiences"** in sidebar
2. Click **"New Experience"** button
3. Select category and type
4. Fill in the form
5. Click **"Create"**

### Browse NAICS Codes
1. Click **"NAICS"** in sidebar
2. Search or filter by industry
3. View code details

---

## 🔌 Connecting to Your Database

### Step 1: Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### Step 2: Switch Data Source
1. Look at top right of admin panel
2. Click the toggle switch
3. Change from **"Local Mock"** to **"Server API"**

### Step 3: Verify Connection
- Dashboard should load with database statistics
- Users page should show database users
- If you see errors, check that backend is running

---

## 🐛 Troubleshooting

### White Screen / Loading Forever
**FIXED!** The Dashboard async issue has been resolved.

### "Loading dashboard..." Never Finishes
**Cause:** Data source is set to "Server API" but backend is not running

**Solution:**
1. Start backend: `uvicorn main:app --reload` (in backend/ directory)
2. OR switch to "Local Mock" mode

### CORS Errors in Console
**Cause:** Backend rejecting requests from frontend

**Solution:** Update `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://localhost:5173"]
```

Restart backend after changing.

### No Data Showing
**In Local Mock Mode:**
- Should always show mock data (25 users)
- If not, there may be a JavaScript error (check console)

**In Server API Mode:**
- Backend must be running
- Database must be seeded: `python backend/seed_db.py`
- Check browser console for API errors

---

## 🎨 Features You Can Use Now

### ✅ Working Features (Local Mock)
- View dashboard with charts
- Browse mock users (25 users)
- Browse mock experiences
- View NAICS codes
- Create/edit/delete users (in memory only)
- Create/edit/delete experiences (in memory only)

### ✅ Working Features (Server API - with backend)
- All above features PLUS:
- Changes persist to database
- Real user data from PostgreSQL
- Real experience data
- Authentication (future)

---

## 📝 Test Users (Local Mock)

When using Local Mock mode, you'll see users like:
- johnsmith0@example.com
- sarahjohnson1@example.com
- michaelwilliams2@example.com

**Note:** These are fake users for testing the UI.

---

## 🔐 Test Users (Server API - after seeding)

After running `python backend/seed_db.py`, you'll have:
- 25 real users in database
- Username format: `firstnamelastnameN`
- Password for all: `TestPassword123!`

Examples:
- Username: `johnsmith0`
- Password: `TestPassword123!`

---

## ✨ What Was Fixed

### Before (Broken):
```javascript
// ❌ Wrong - not awaiting async function
useEffect(() => {
  const data = getStats();  // Returns a Promise, not data!
  setStats(data);
}, []);
```

### After (Fixed):
```javascript
// ✅ Correct - properly awaiting async function
useEffect(() => {
  const loadStats = async () => {
    const data = await getStats();  // Wait for data
    setStats(data);
  };
  loadStats();
}, [getStats]);
```

---

## 🎯 Next Steps

1. **Try it now:** Refresh http://localhost:5173
2. **Explore:** Click around the dashboard
3. **Create a user:** Go to Users → New User
4. **Add experience:** Go to Experiences → New Experience
5. **Connect backend:** When ready, switch to Server API mode

---

## 📚 Full Documentation

For complete details, see:
- **[ADMIN_PANEL_GUIDE.md](../../../docs/dev/ADMIN_PANEL_GUIDE.md)** - Comprehensive guide
- **[DATABASE_SETUP_NOTES.md](../../../docs/deployment/DATABASE_SETUP_NOTES.md)** - Database setup
- **[API_DOCUMENTATION.md](../../../docs/api/API_DOCUMENTATION.md)** - API reference

---

**The admin panel is now working! 🎉**

Refresh your browser at http://localhost:5173 and you should see the dashboard load properly.
