# Render Deployment Checklist - XP System Setup

**Last Updated:** 2025-12-08
**Component:** XP System + Dev Interface
**Branch:** `claude/mvp-backend-setup-01YafZDPCREi254gDQqVbktE`

---

## 🎯 Overview

This guide will help you deploy the new XP system to your Render setup:
- **Backend:** Web Service (already running)
- **Database:** PostgreSQL (already created)
- **Dev Interface:** Static site

---

## ✅ Pre-Deployment Checklist

### 1. Code Deployed
- [x] Code pushed to GitHub branch: `claude/mvp-backend-setup-01YafZDPCREi254gDQqVbktE`
- [ ] Merge to `main` branch (or configure Render to deploy from this branch)

### 2. Environment Variables Ready
- [ ] OpenAI API key (already in Render dashboard)
- [ ] Pinecone API key (already in Render dashboard)
- [ ] Pinecone index populated (confirmed by user)

---

## 🗄️ Database Migration

### Step 1: Access Render Shell

**Option A: Via Render Dashboard**
1. Go to https://dashboard.render.com
2. Select your **backend web service**
3. Click **"Shell"** tab
4. You'll get a terminal in your running container

**Option B: Via Render CLI**
```bash
# Install Render CLI (if not installed)
npm install -g @render/cli

# Login
render login

# Connect to shell
render shell <your-service-id>
```

### Step 2: Run Migration

In the Render shell:

```bash
# Navigate to backend directory
cd backend

# Run the migration
python -m alembic upgrade head

# Verify migration
python -m alembic current
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade 41518377be8d -> add_xp_fields, add xp fields to users
```

### Step 3: Verify Database Schema

```bash
# Connect to PostgreSQL (in Render shell)
python -c "
from backend.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
columns = inspector.get_columns('users')
xp_fields = [c['name'] for c in columns if 'xp' in c['name'] or c['name'] == 'level']
print('XP Fields:', xp_fields)
"
```

**Expected Output:**
```
XP Fields: ['professional_xp', 'education_xp', 'skills_xp', 'vocational_xp', 'total_xp', 'level']
```

---

## ⚙️ Environment Variables

### Required Variables (Already Set)

These should already be in your Render dashboard:

| Variable | Status | Notes |
|----------|--------|-------|
| `DATABASE_URL` | ✅ Set | Internal PostgreSQL URL |
| `SECRET_KEY` | ✅ Set | JWT secret |
| `OPENAI_API_KEY` | ✅ Set | For Neural Hive |
| `PINECONE_API_KEY` | ✅ Set | For job correlation |
| `PINECONE_INDEX_NAME` | ✅ Set | industry-classifier |
| `PINECONE_ENV` | ✅ Set | us-east-1 (or your region) |

### Optional Variables (Recommended)

If not already set, add these:

| Variable | Value | Purpose |
|----------|-------|---------|
| `NAMESPACE_NAICS` | `naics-codes` | Pinecone namespace |
| `NAMESPACE_ONET` | `onet-codes` | Pinecone namespace |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `ENVIRONMENT` | `production` | Environment mode |
| `DEBUG` | `false` | Disable debug mode |

### How to Verify Environment Variables

1. Go to Render Dashboard
2. Select your backend web service
3. Click **"Environment"** tab
4. Verify all variables are present

---

## 🚀 Deployment

### Option A: Auto-Deploy (Recommended)

If you have auto-deploy enabled on `main` branch:

1. **Merge your branch to main:**
   ```bash
   git checkout main
   git merge claude/mvp-backend-setup-01YafZDPCREi254gDQqVbktE
   git push origin main
   ```

2. **Watch Render deploy automatically:**
   - Go to Render Dashboard → Your Service
   - Click **"Events"** tab
   - Watch deployment progress (~3-5 minutes)

### Option B: Manual Deploy

If auto-deploy is NOT enabled:

1. Go to Render Dashboard → Your Service
2. Click **"Manual Deploy"** dropdown
3. Select **"Deploy latest commit"** or select your branch
4. Click **"Deploy"**

### Option C: Configure Branch Deploy

To deploy from feature branch without merging:

1. Render Dashboard → Your Service → **Settings**
2. **Branch:** Change from `main` to `claude/mvp-backend-setup-01YafZDPCREi254gDQqVbktE`
3. Click **"Save Changes"**
4. Render will redeploy automatically

---

## 🧪 Post-Deployment Testing

### 1. Test Health Endpoint

```bash
curl https://your-service.onrender.com/health
```

**Expected:** `{"status": "healthy", ...}`

### 2. Test XP Endpoints

```bash
# Get API docs (if DEBUG=true)
curl https://your-service.onrender.com/docs

# Check new XP endpoints are available
curl https://your-service.onrender.com/api/v1/leaderboard

# Should return empty leaderboard initially
```

### 3. Test User Creation with XP

```bash
# Create a test user
curl -X POST https://your-service.onrender.com/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "xptest",
    "email": "xptest@example.com",
    "password": "testpass123"
  }'

# Login to get token
TOKEN=$(curl -X POST https://your-service.onrender.com/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xptest", "password": "testpass123"}' \
  | jq -r '.access_token')

# Get user profile (should show XP fields with zeros)
curl https://your-service.onrender.com/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "id": "...",
  "username": "xptest",
  "email": "xptest@example.com",
  "professional_xp": 0.0,
  "education_xp": 0.0,
  "skills_xp": 0.0,
  "vocational_xp": 0.0,
  "total_xp": 0.0,
  "level": 0,
  ...
}
```

### 4. Test Experience Creation + XP Calculation

```bash
# Create an experience
curl -X POST "https://your-service.onrender.com/api/v1/experiences/?user_id=<USER_ID>" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "workplace",
    "experience_type": "full_time",
    "title": "Software Engineer",
    "description": "Test job",
    "naics_code": "541511",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-04-01T00:00:00",
    "type_specific_data": {"hours_per_week": 40}
  }'

# Check XP recalculated
curl https://your-service.onrender.com/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:**
- `professional_xp` should be ~5200 (3 months × 4 weeks × 40 hrs × 10 XP)
- `level` should be 7

---

## 🌐 Deploy Dev Interface (Static Site)

### Option 1: Render Static Site

1. **Create New Static Site:**
   - Render Dashboard → **"New +"** → **"Static Site"**
   - Connect GitHub repository
   - **Name:** `levelith-dev-interface`
   - **Branch:** `claude/mvp-backend-setup-01YafZDPCREi254gDQqVbktE` (or main after merge)
   - **Root Directory:** Leave blank
   - **Build Command:** Leave blank (no build needed)
   - **Publish Directory:** `.` (root directory)

2. **Configure:**
   - No environment variables needed (uses API at localhost:8000 by default)
   - Static site will be at: `https://levelith-dev-interface.onrender.com`

3. **Update dev_interface.html:**

   You'll need to update the API URL in the dev interface:

   ```javascript
   // Change this line in dev_interface.html
   const API_BASE = 'https://your-backend.onrender.com/api/v1';
   ```

### Option 2: Keep Local Only

The dev interface works great locally:

```bash
# From project root
python -m http.server 8080

# Visit: http://localhost:8080/dev_interface.html
```

---

## 🔍 Troubleshooting

### Migration Fails

**Error:** `"table users has no column named professional_xp"`

**Solution:**
```bash
# Check current migration
alembic current

# If behind, run upgrade
alembic upgrade head

# If migration file missing, check:
ls backend/alembic/versions/
# Should see: 20251208_add_xp_fields_to_users.py
```

### XP Not Calculating

**Symptoms:** Experience created but XP stays at 0

**Causes:**
1. Migration didn't run (XP fields don't exist)
2. Experience creation endpoint not calling XP service

**Solution:**
```bash
# Check logs in Render Dashboard
# Look for errors like "column professional_xp does not exist"

# Verify migration ran:
curl https://your-service.onrender.com/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" | jq .professional_xp

# If null instead of 0.0, migration didn't run
```

### Pinecone Errors

**Error:** `"Pinecone index not found"`

**Cause:** Pinecone index name mismatch

**Solution:**
1. Check Pinecone dashboard for actual index name
2. Update `PINECONE_INDEX_NAME` in Render environment variables
3. Redeploy

### CORS Errors in Dev Interface

**Error:** `"CORS policy: No 'Access-Control-Allow-Origin' header"`

**Solution:**
1. Render Dashboard → Backend Service → Environment
2. Update `CORS_ORIGINS`:
   ```
   https://levelith-dev-interface.onrender.com,http://localhost:8080,http://localhost:8000
   ```
3. Save (triggers redeploy)

---

## 📋 Deployment Verification Checklist

After deployment, verify:

- [ ] Backend service shows "Live" status
- [ ] Migration completed successfully
- [ ] Health endpoint returns healthy
- [ ] XP endpoints accessible (`/api/v1/leaderboard`, `/api/v1/users/{id}/xp`)
- [ ] User creation includes XP fields (all zeros)
- [ ] Experience creation triggers XP recalculation
- [ ] XP calculates correctly (10 XP per hour)
- [ ] Level calculates correctly (exponential formula)
- [ ] Neural Hive endpoint works (if testing)
- [ ] CORS allows dev interface domain
- [ ] API docs accessible (if DEBUG=true)

---

## 🎯 Quick Commands Reference

```bash
# SSH into Render service
render shell <service-id>

# Run migration
cd backend && alembic upgrade head

# Check migration status
alembic current

# View logs
# (Do this in Render Dashboard → Logs tab)

# Test health
curl https://your-service.onrender.com/health

# Test XP endpoint
curl https://your-service.onrender.com/api/v1/leaderboard

# Deploy from branch
# (Render Dashboard → Settings → Branch → Save)

# Manual deploy
# (Render Dashboard → Manual Deploy → Deploy latest commit)
```

---

## 📞 Need Help?

**Common Issues:**
1. **Migration fails** → Check database connection in Render logs
2. **XP not calculating** → Verify migration ran with `alembic current`
3. **CORS errors** → Update `CORS_ORIGINS` environment variable
4. **Pinecone errors** → Verify API key and index name in environment

**Where to Check:**
- **Logs:** Render Dashboard → Your Service → Logs
- **Database:** Render Dashboard → Your Database → Connections
- **Environment:** Render Dashboard → Your Service → Environment
- **Deployment:** Render Dashboard → Your Service → Events

---

**Next Steps:**
1. ✅ Run database migration
2. ✅ Verify deployment successful
3. ✅ Test XP calculation
4. ✅ Deploy dev interface (optional)
5. ✅ Start creating experiences and earning XP!
