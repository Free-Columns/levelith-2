# Render Web Service Deployment Guide

---
title: "Render Web Service Deployment Guide"
description: "Complete step-by-step guide for deploying Levelith Backend to Render Web Service with managed PostgreSQL database."
category: "guides"
tags: ["deployment", "render", "postgresql", "backend", "production"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 25
relatedPages:
  - "/docs/deployment/DEPLOYMENT.md"
  - "/docs/deployment/DATABASE_SETUP_NOTES.md"
  - "/docs/api/API_DOCUMENTATION.md"
nextPage: "/docs/deployment/DATABASE_SETUP_NOTES.md"
prevPage: "/docs/deployment/DEPLOYMENT.md"
searchKeywords:
  - "render deployment"
  - "postgresql setup"
  - "production deployment"
  - "web service"
  - "environment variables"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Render Web Service Deployment Guide

> **TL;DR:** Deploy Levelith FastAPI backend to Render Web Service with PostgreSQL - no Docker required, fully managed infrastructure with automatic SSL and health monitoring.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Database Setup](#database-setup)
- [Web Service Setup](#web-service-setup)
- [Environment Variables](#environment-variables)
- [Deploy & Verify](#deploy--verify)
- [Troubleshooting](#troubleshooting)
- [Post-Deployment](#post-deployment)
- [Security Checklist](#security-checklist)
- [Additional Resources](#additional-resources)

---

## Prerequisites

### Required Accounts

- ✅ **GitHub account** with this repository pushed
- ✅ **Render account** (free tier available at https://render.com)

### Required Files (Already Configured)

- ✅ `Procfile` - Defines start command
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/main.py` - FastAPI application
- ✅ `.env.render.example` - Environment variable reference

:::info
**Note:** All required configuration files are already included in the repository. You only need to set up environment variables on Render.
:::

---

## Database Setup

### Option A: Render PostgreSQL (Recommended)

1. **Log in to Render Dashboard**

   Navigate to https://dashboard.render.com

2. **Create New PostgreSQL Database**

   - Click **"New +"** button
   - Select **"PostgreSQL"**

3. **Configure Database**

   | Setting | Value |
   |---------|-------|
   | **Name** | `levelith-db` |
   | **Database** | `levelith` |
   | **User** | `levelith_user` |
   | **Region** | Oregon (US West) |
   | **Plan** | Free (or Starter $7/month for production) |
   | **PostgreSQL Ver** | 15 |

4. **Create Database**

   - Click **"Create Database"**
   - Wait for provisioning (~2 minutes)

5. **Copy Connection String**

   After creation, go to database dashboard and find **"Internal Database URL"**:

   ```
   postgresql://levelith_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/levelith
   ```

:::warning
**Important:** Use "Internal Database URL" (not External) for better security and performance within Render's network.
:::

### Option B: External PostgreSQL

If using external PostgreSQL (AWS RDS, DigitalOcean, etc.):
- Ensure it's publicly accessible or in same VPC
- Get connection string in format:
  ```
  postgresql://user:password@host:port/database
  ```

---

## Web Service Setup

### Create Web Service

1. **Go to Render Dashboard**

   Click **"New +"** → **"Web Service"**

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

:::tip
**Pro Tip:** Enable Auto-Deploy to automatically redeploy whenever you push to your main branch, ensuring your production environment stays in sync with your codebase.
:::

5. **Do NOT Click "Create Web Service" Yet!**

   ⚠️ First, configure environment variables (next step)

---

## Environment Variables

### Required Environment Variables

Before creating the service, scroll down to **"Environment Variables"** section and add:

#### Critical Variables (MUST SET)

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | *(from Database Setup)* | Internal Database URL from Render PostgreSQL |
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

**Option 1: Use Render's Generator**
- In the `SECRET_KEY` value field
- Click **"Generate Value"**

**Option 2: Generate Locally**

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

:::tip
**Pro Tip:** Using "Add from Database" automatically keeps the DATABASE_URL in sync if you ever need to recreate or migrate the database.
:::

---

## Deploy & Verify

### Create Web Service

1. **Review All Settings**

   - ✅ Build Command: `pip install -r backend/requirements.txt`
   - ✅ Start Command: (blank - uses Procfile)
   - ✅ Environment Variables: All required vars set
   - ✅ Health Check Path: `/health`

2. **Click "Create Web Service"**

3. **Wait for Deployment**

   Render will:
   1. Clone your repository
   2. Install dependencies (~3-5 minutes)
   3. Run health checks
   4. Start the service

   Watch the **Logs** tab for progress

4. **Deployment Complete**

   - You'll see: ✅ **"Live"** status
   - Your service URL: `https://levelith-backend.onrender.com`

### Test Health Endpoint

```bash
# Replace with your actual Render URL
curl https://levelith-backend.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T10:30:00.000000",
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
  "timestamp": "2025-11-19T10:30:00.000000",
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

:::warning
**Warning:** In production, API docs are disabled by default for security. Only enable temporarily for testing.
:::

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

## Troubleshooting

<details>
<summary><strong>❌ Error: "No module named 'backend'"</strong></summary>

**Symptoms:** Build fails with import errors related to backend module

**Causes:**
1. Incorrect build/start commands
2. Missing Procfile
3. Wrong working directory

**Solutions:**
```bash
# Ensure Procfile exists in repository root
cat Procfile
# Should contain: web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT

# Verify build command in Render dashboard:
# pip install -r backend/requirements.txt

# Start command should be blank (uses Procfile)
```

**Explanation:** Render needs to install dependencies from the correct path and start the application from the backend directory.
</details>

<details>
<summary><strong>❌ Error: Database Connection Failed</strong></summary>

**Symptoms:** Service starts but health checks fail with database connection errors

**Causes:**
1. Incorrect `DATABASE_URL`
2. Database not running
3. Using External URL instead of Internal
4. Database and web service in different regions

**Solutions:**
1. Verify database is **"Available"** in Render dashboard
2. Use **"Internal Database URL"** (not External)
3. Check database and web service are in **same region**
4. Verify format: `postgresql://user:pass@host/db` (no spaces)

**Example of correct Internal URL:**
```
postgresql://levelith_user:password@dpg-xxxxx.oregon-postgres.render.com/levelith
```
</details>

<details>
<summary><strong>⚠️ Warning: Health Check Failing</strong></summary>

**Symptoms:** Service shows as "Unhealthy" or fails to start

**Solutions:**
1. Check logs: Render Dashboard → Logs
2. Verify health check path: `/health` (no trailing slash)
3. Check if port is correctly set (Render sets `$PORT` automatically)
4. Ensure application starts on `0.0.0.0` not `localhost`

**Debug steps:**
```bash
# Check if health endpoint exists
curl https://your-service.onrender.com/health -v

# Review application logs for startup errors
# Render Dashboard → Service → Logs tab
```
</details>

<details>
<summary><strong>⚠️ Warning: "Service has exceeded memory limit"</strong></summary>

**Symptoms:** Service crashes or restarts frequently, memory usage at 100%

**Causes:** Free tier has 512MB limit, application using too much memory

**Solutions:**
1. Reduce `DATABASE_POOL_SIZE` to `5`
   ```env
   DATABASE_POOL_SIZE=5
   ```
2. Upgrade to Starter plan ($7/month, 512MB → 2GB)
3. Check for memory leaks in logs
4. Review application code for memory-intensive operations
</details>

<details>
<summary><strong>❌ Error: CORS Errors from Frontend</strong></summary>

**Symptoms:** Frontend receives CORS policy errors when calling API

**Cause:** Frontend URL not in `CORS_ORIGINS`

**Solution:**
Add your frontend URL to `CORS_ORIGINS` environment variable:
- Format: `https://frontend.onrender.com` (no trailing slash)
- Multiple origins: `https://app1.com,https://app2.com`

**Example:**
```env
CORS_ORIGINS=https://levelith-frontend.onrender.com,https://levelith.com
```
</details>

<details>
<summary><strong>❌ Error: Service Returns 500 Errors</strong></summary>

**Symptoms:** Service starts but API endpoints return 500 Internal Server Error

**Causes:**
1. Missing environment variables
2. Database migration needed
3. Import/dependency errors

**Solutions:**
1. Check Render logs for detailed error messages
2. Enable debug temporarily:
   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```
3. Common issues:
   - Missing `SECRET_KEY`
   - Invalid `DATABASE_URL` format
   - Missing dependencies in requirements.txt
4. **Remember to disable debug after fixing:**
   ```env
   DEBUG=false
   LOG_LEVEL=INFO
   ```
</details>

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

## Post-Deployment

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

:::tip
**Pro Tip:** Render automatically provisions and renews SSL certificates for custom domains using Let's Encrypt - no manual certificate management required!
:::

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

**Render PostgreSQL (Paid plans only):**
- Automatic daily backups
- Point-in-time recovery

**Free Tier:**
- No automatic backups
- Manual backup:
  ```bash
  # Get external connection URL from dashboard
  pg_dump <EXTERNAL_DATABASE_URL> > backup.sql
  ```

:::warning
**Warning:** Free tier databases have no automatic backups. Upgrade to Starter plan ($7/month) for production use with automatic backup protection.
:::

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

## Best Practices

### ✅ DO

1. **Use Internal Database URL**
   ```env
   # ✅ GOOD - Internal URL (faster, more secure)
   DATABASE_URL=postgresql://user:pass@dpg-xxx.oregon-postgres.render.com/db
   ```

2. **Enable Auto-Deploy for main branch**
   - Ensures production stays in sync with repository
   - Automatic deployments on every push

3. **Set up health check monitoring**
   ```python
   # ✅ GOOD - Include database check in health endpoint
   @app.get("/health/details")
   async def health_details():
       return {
           "status": "healthy",
           "database": await check_database()
       }
   ```

### ❌ DON'T

1. **Use External Database URL**
   ```env
   # ❌ BAD - External URL (slower, less secure)
   DATABASE_URL=postgresql://user:pass@external-host.com:5432/db
   ```

2. **Commit secrets to repository**
   ```bash
   # ❌ BAD - Never commit .env files
   git add .env

   # ✅ GOOD - Use .env.example instead
   git add .env.example
   ```

3. **Leave DEBUG=true in production**
   ```env
   # ❌ BAD - Security risk, performance impact
   DEBUG=true

   # ✅ GOOD - Disable debug in production
   DEBUG=false
   ```

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
- [ ] API documentation disabled in production
- [ ] Rate limiting enabled

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

### Standard Tier (High Traffic)
- **Web Service**: $25/month (4GB RAM, dedicated)
- **PostgreSQL**: $25/month (10GB storage, high performance)
- **Total**: $50/month

---

## Additional Resources

### Official Documentation

- 📚 [Render Documentation](https://render.com/docs)
- 🏗️ [Render PostgreSQL Guide](https://render.com/docs/databases)
- 🧪 [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

### Internal Documentation

- 📖 [Deployment Guide](/docs/deployment/DEPLOYMENT.md)
- 📋 [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)
- 🎯 [API Documentation](/docs/api/API_DOCUMENTATION.md)

### External Resources

- 🌐 [Render Status Page](https://status.render.com)
- 📊 [Render Community](https://community.render.com)
- 💻 [GitHub Repository](https://github.com/Free-Columns/levelith-2)

### Support

- 💬 [Render Support](https://render.com/support)
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues)
- ❓ [Levelith Documentation](https://github.com/Free-Columns/levelith-2/tree/main/docs)

---

## Related Documentation

- **Previous:** [General Deployment Guide](/docs/deployment/DEPLOYMENT.md)
- **Next:** [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)

**Other related documentation:**

- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Environment Configuration](/docs/guides/ENVIRONMENT_SETUP.md)
- [Architecture Overview](/docs/architecture/ARCHITECTURE.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Star us on GitHub
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 2.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, visit our [GitHub repository](https://github.com/Free-Columns/levelith-2).*
