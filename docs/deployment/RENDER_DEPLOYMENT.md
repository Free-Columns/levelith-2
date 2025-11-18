# Render Web Service Deployment Guide

**Complete guide for deploying Levelith Backend to Render Web Service (without Blueprints)**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Web Service Setup](#web-service-setup)
4. [Environment Variables](#environment-variables)
5. [Deploy & Verify](#deploy--verify)
6. [Troubleshooting](#troubleshooting)
7. [Post-Deployment](#post-deployment)

---

## Prerequisites

### Required Accounts
- ✅ GitHub account with this repository pushed
- ✅ Render account (free tier available at https://render.com)

### Required Files (Already Configured)
- ✅ `Procfile` - Defines start command
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/main.py` - FastAPI application
- ✅ `.env.render.example` - Environment variable reference

---

## Step 1: Database Setup

### Option A: Render PostgreSQL (Recommended)

1. **Log in to Render Dashboard**
   - Go to https://dashboard.render.com

2. **Create New PostgreSQL Database**
   - Click **"New +"** button
   - Select **"PostgreSQL"**

3. **Configure Database**
   ```
   Name:           levelith-db
   Database:       levelith
   User:           levelith_user
   Region:         Oregon (US West)
   Plan:           Free (or Starter $7/month for production)
   PostgreSQL Ver: 15
   ```

4. **Create Database**
   - Click **"Create Database"**
   - Wait for provisioning (~2 minutes)

5. **Copy Connection String**
   - After creation, go to database dashboard
   - Find **"Internal Database URL"**
   - Copy the full URL (looks like):
     ```
     postgresql://levelith_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/levelith
     ```
   - ⚠️ **IMPORTANT**: Use "Internal Database URL" (not External)

### Option B: External PostgreSQL

If using external PostgreSQL (AWS RDS, DigitalOcean, etc.):
- Ensure it's publicly accessible or in same VPC
- Get connection string in format:
  ```
  postgresql://user:password@host:port/database
  ```

---

## Step 2: Web Service Setup

### Create Web Service

1. **Go to Render Dashboard**
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository**
   - Select **"Build and deploy from a Git repository"**
   - Click **"Connect GitHub"** (if not already connected)
   - Find and select **`Free-Columns/levelith-2`**
   - Click **"Connect"**

3. **Configure Web Service**

   Fill in the following settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `levelith-backend` (or your preferred name) |
   | **Region** | Oregon (same as database) |
   | **Branch** | `main` (or your production branch) |
   | **Root Directory** | Leave blank (will use repository root) |
   | **Runtime** | **Python 3** |
   | **Build Command** | `pip install -r backend/requirements.txt` |
   | **Start Command** | Leave blank (will use Procfile) |
   | **Plan** | Free (or Starter $7/month) |

4. **Advanced Settings (Optional)**

   Click **"Advanced"** to expand:

   - **Auto-Deploy**: `Yes` (recommended)
   - **Health Check Path**: `/health`
   - **Docker Command**: Leave blank (not using Docker)

5. **Do NOT Click "Create Web Service" Yet!**

   ⚠️ First, configure environment variables (next step)

---

## Step 3: Environment Variables

### Required Environment Variables

Before creating the service, scroll down to **"Environment Variables"** section and add:

#### Critical Variables (MUST SET)

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | *(from Step 1)* | Internal Database URL from Render PostgreSQL |
| `SECRET_KEY` | *(generate)* | Click "Generate Value" or use: `openssl rand -hex 32` |
| `ENVIRONMENT` | `production` | Sets production mode |
| `DEBUG` | `false` | Disables debug mode |

#### Recommended Variables

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `LOG_LEVEL` | `INFO` | Logging level |
| `CORS_ORIGINS` | `https://yourdomain.com` | Your frontend URL (comma-separated if multiple) |
| `API_V1_PREFIX` | `/api/v1` | API prefix (default) |

#### Optional Variables

| Key | Value | Notes |
|-----|-------|-------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token expiry |
| `DATABASE_POOL_SIZE` | `10` | Connection pool size |
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `RATE_LIMIT_REQUESTS` | `100` | Requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Window in seconds |

### How to Add Environment Variables

For each variable:
1. Click **"Add Environment Variable"**
2. Enter **Key** (e.g., `DATABASE_URL`)
3. Enter **Value** (e.g., your database URL)
4. Click **"Add"**

### Generate SECRET_KEY

**Option 1**: Use Render's Generator
- In the `SECRET_KEY` value field
- Click **"Generate Value"**

**Option 2**: Generate Locally
```bash
# On Mac/Linux
openssl rand -hex 32

# On Windows (PowerShell)
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

### Link Database (Alternative Method)

If you created a Render PostgreSQL database:
1. Scroll to **"Environment Variables"**
2. Click **"Add from Database"**
3. Select your `levelith-db` database
4. This automatically adds `DATABASE_URL`

---

## Step 4: Create Web Service

1. **Review All Settings**
   - ✅ Build Command: `pip install -r backend/requirements.txt`
   - ✅ Start Command: (blank - uses Procfile)
   - ✅ Environment Variables: All required vars set
   - ✅ Health Check Path: `/health`

2. **Click "Create Web Service"**

3. **Wait for Deployment**
   - Render will:
     1. Clone your repository
     2. Install dependencies (~3-5 minutes)
     3. Run health checks
     4. Start the service

   - Watch the **Logs** tab for progress

4. **Deployment Complete**
   - You'll see: ✅ **"Live"** status
   - Your service URL: `https://levelith-backend.onrender.com`

---

## Step 5: Verify Deployment

### Test Health Endpoint

```bash
# Replace with your actual Render URL
curl https://levelith-backend.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "version": "2.0.0",
  "environment": "production"
}
```

### Test Database Connection

```bash
curl https://levelith-backend.onrender.com/health/details
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "version": "2.0.0",
  "environment": "production",
  "database": {
    "status": "healthy",
    "database": "dpg-xxxxx.oregon-postgres.render.com/levelith",
    "version": "PostgreSQL 15.x",
    "pool_size": 10
  }
}
```

### Test API Documentation

⚠️ **Note**: In production, API docs are disabled by default.

To temporarily enable for testing:
1. Go to Render Dashboard → Your Service
2. Environment → Edit `DEBUG` to `true`
3. Save (triggers redeploy)
4. Visit: `https://levelith-backend.onrender.com/docs`
5. **Remember to set `DEBUG=false` after testing!**

### Test API Endpoints

```bash
# Create a user
curl -X POST https://levelith-backend.onrender.com/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Get user
curl https://levelith-backend.onrender.com/api/v1/users/1
```

---

## Step 6: Troubleshooting

### Common Issues

#### 1. **Build Failed: "No module named 'backend'"**

**Cause**: Incorrect build/start commands

**Solution**:
- Ensure `Procfile` exists in repository root
- Start command should be blank (uses Procfile)
- Build command: `pip install -r backend/requirements.txt`

#### 2. **Database Connection Error**

**Cause**: Incorrect `DATABASE_URL` or database not running

**Solution**:
- Verify database is **"Available"** in Render dashboard
- Use **"Internal Database URL"** (not External)
- Check database and web service are in **same region**
- Format: `postgresql://user:pass@host/db` (no spaces)

#### 3. **Health Check Failing**

**Cause**: App not starting or wrong health check path

**Solution**:
- Check logs: Render Dashboard → Logs
- Verify health check path: `/health` (no trailing slash)
- Check if port is correctly set (Render sets `$PORT` automatically)

#### 4. **"Your service has exceeded the memory limit"**

**Cause**: Free tier has 512MB limit

**Solutions**:
- Reduce `DATABASE_POOL_SIZE` to `5`
- Upgrade to Starter plan ($7/month, 512MB → 2GB)
- Check for memory leaks in logs

#### 5. **CORS Errors from Frontend**

**Cause**: Frontend URL not in `CORS_ORIGINS`

**Solution**:
- Add your frontend URL to `CORS_ORIGINS` environment variable
- Format: `https://frontend.onrender.com` (no trailing slash)
- Multiple origins: `https://app1.com,https://app2.com`

#### 6. **Service Starts But Returns 500 Errors**

**Cause**: Application error

**Solution**:
1. Check Render logs for error messages
2. Common issues:
   - Missing environment variables
   - Database migration needed
   - Import errors
3. Enable debug temporarily:
   - Set `DEBUG=true`
   - Set `LOG_LEVEL=DEBUG`
   - Check detailed logs
   - **Remember to disable after fixing!**

### View Logs

1. Go to Render Dashboard
2. Select your web service
3. Click **"Logs"** tab
4. Use filters:
   - **All Logs**: Shows everything
   - **Deploy Logs**: Build and deploy process
   - **Service Logs**: Application runtime logs

### Manual Restart

If needed:
1. Render Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

---

## Step 7: Post-Deployment

### Update CORS for Frontend

Once you deploy your frontend:
1. Get frontend URL (e.g., `https://levelith-frontend.onrender.com`)
2. Render Dashboard → Backend Service → Environment
3. Edit `CORS_ORIGINS`:
   ```
   https://levelith-frontend.onrender.com,https://levelith.com
   ```
4. Save (auto-redeploys)

### Set Up Custom Domain (Optional)

1. Render Dashboard → Your Service → Settings
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `api.levelith.com`
5. Add DNS records as instructed
6. Wait for SSL certificate provisioning (~5 min)

### Enable Auto-Deploy

Already enabled if you checked "Auto-Deploy" during setup.

To verify/enable:
1. Render Dashboard → Your Service → Settings
2. **Auto-Deploy**: Yes
3. **Branch**: `main`

Now, every push to `main` branch auto-deploys!

### Monitor Service

**Render Dashboard Metrics:**
- CPU usage
- Memory usage
- Bandwidth
- Request rate
- Response times

**Health Check Monitoring:**
- Render pings `/health` every 60 seconds
- Auto-restarts if health check fails

### Database Backups

**Render PostgreSQL** (Paid plans only):
- Automatic daily backups
- Point-in-time recovery

**Free Tier**:
- No automatic backups
- Manual backup:
  ```bash
  # Get external connection URL
  pg_dump <EXTERNAL_DATABASE_URL> > backup.sql
  ```

### Scale Up (When Ready)

**Upgrade Web Service:**
- Free → Starter ($7/month)
  - 512MB RAM → 2GB RAM
  - Better performance
  - No cold starts

**Upgrade Database:**
- Free → Starter ($7/month)
  - Automatic backups
  - Better performance
  - More connections

---

## Environment-Specific Configuration

### Production (Current Setup)
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### Staging (If Needed)
Create a second web service:
- Name: `levelith-backend-staging`
- Branch: `staging`
- Environment:
  ```env
  ENVIRONMENT=staging
  DEBUG=true
  LOG_LEVEL=DEBUG
  ```

---

## Quick Reference

### Service URLs

| Environment | URL |
|-------------|-----|
| Production | `https://levelith-backend.onrender.com` |
| Health Check | `https://levelith-backend.onrender.com/health` |
| API Docs (dev) | `https://levelith-backend.onrender.com/docs` |

### Key Commands

```bash
# Test health endpoint
curl https://levelith-backend.onrender.com/health

# Test with details
curl https://levelith-backend.onrender.com/health/details

# View logs (via Render CLI - optional)
render logs levelith-backend

# Manual deploy (via Render CLI)
render deploy levelith-backend
```

### Important Files

| File | Purpose |
|------|---------|
| `Procfile` | Start command |
| `backend/requirements.txt` | Dependencies |
| `backend/main.py` | Application entry |
| `.env.render.example` | Env var reference |

---

## Differences from Blueprint Deployment

This guide uses **Manual Web Service** creation instead of `render.yaml` Blueprint.

**Why?**
- More control over configuration
- Easier to understand for beginners
- Can modify without changing code
- Easier troubleshooting

**Blueprint Equivalent:**
The `render.yaml` file in this repo can still be used for Infrastructure as Code deployment. This guide provides the manual alternative.

---

## Security Checklist

Before going live:

- [ ] `SECRET_KEY` is strong and unique (not default)
- [ ] `DEBUG=false` in production
- [ ] `DATABASE_URL` uses Internal URL (secure)
- [ ] `CORS_ORIGINS` only includes your domains
- [ ] Database has strong password
- [ ] Environment variables not committed to Git
- [ ] HTTPS enabled (automatic on Render)
- [ ] Health checks configured

---

## Cost Estimate

### Free Tier (Development)
- **Web Service**: Free (512MB RAM, sleeps after 15min inactivity)
- **PostgreSQL**: Free (256MB storage, no backups)
- **Total**: $0/month

### Starter Tier (Production)
- **Web Service**: $7/month (2GB RAM, no sleep)
- **PostgreSQL**: $7/month (1GB storage, automatic backups)
- **Total**: $14/month

---

## Support & Resources

- **Render Documentation**: https://render.com/docs
- **Render Status**: https://status.render.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Levelith Backend Issues**: https://github.com/Free-Columns/levelith-2/issues

---

## Next Steps

1. ✅ Deploy backend (you are here!)
2. 🔄 Deploy frontend to Render
3. 🔄 Update `CORS_ORIGINS` with frontend URL
4. 🔄 Test end-to-end integration
5. 🔄 Set up custom domain (optional)
6. 🔄 Enable monitoring/alerts
7. 🔄 Plan for production scaling

---

**Congratulations!** Your Levelith backend is now live on Render! 🎉
