# Levelith Complete Deployment Guide

---
title: "Levelith Complete Deployment Guide"
description: "Comprehensive guide for deploying Levelith FastAPI backend to Render with managed PostgreSQL - includes overview, step-by-step setup, troubleshooting, and production best practices."
category: "guides"
tags: ["deployment", "render", "fastapi", "postgresql", "infrastructure", "production"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 35
relatedPages:
  - "/docs/deployment/DATABASE_SETUP_NOTES.md"
  - "/docs/architecture/ARCHITECTURE.md"
  - "/docs/api/API_DOCUMENTATION.md"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Levelith Complete Deployment Guide

> **TL;DR:** Deploy Levelith FastAPI backend to Render using either automated Blueprint (Infrastructure as Code) or manual setup with managed PostgreSQL database. Includes comprehensive configuration, troubleshooting, and production best practices.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25-35 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
- [Option 1: Automated Blueprint Deployment](#option-1-automated-blueprint-deployment)
- [Option 2: Manual Step-by-Step Deployment](#option-2-manual-step-by-step-deployment)
  - [Database Setup](#database-setup)
  - [Web Service Setup](#web-service-setup)
  - [Environment Variables](#environment-variables)
  - [Deploy & Verify](#deploy--verify)
- [Post-Deployment Configuration](#post-deployment-configuration)
- [Database Management](#database-management)
- [Monitoring & Logs](#monitoring--logs)
- [Scaling](#scaling)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)
- [Cost Breakdown](#cost-breakdown)
- [Additional Resources](#additional-resources)

---

## Overview

This comprehensive guide covers deploying the Levelith FastAPI backend to Render Web Service with managed PostgreSQL database. Render provides a fully managed platform with automatic SSL, health monitoring, and easy scaling.

### Key Features

- ✅ **Managed PostgreSQL** - Automatic backups and scaling
- ✅ **Auto-Deploy** - CI/CD integration with GitHub
- ✅ **Health Monitoring** - Automatic restart on failures
- ✅ **SSL/HTTPS** - Free certificates via Let's Encrypt
- ✅ **Custom Domains** - Easy DNS configuration
- ✅ **Environment Variables** - Secure secrets management

:::info
**Note:** This guide combines both Infrastructure as Code (Blueprint) and manual deployment approaches. Choose the method that best fits your needs and experience level.
:::

---

## Architecture

The Levelith backend deployment consists of:

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Platform**: Render Web Service
- **Database**: Render PostgreSQL (Managed)
- **Deployment**: Infrastructure as Code (`render.yaml`) or Manual Setup

```
┌─────────────────────────────────────────┐
│           GitHub Repository              │
│    (levelith-2/main branch)             │
└────────────┬────────────────────────────┘
             │ Auto-deploy on push
             ▼
┌─────────────────────────────────────────┐
│        Render Web Service                │
│  ┌─────────────────────────────────┐   │
│  │   FastAPI Application            │   │
│  │   - Python 3.11                 │   │
│  │   - uvicorn server              │   │
│  │   - Health checks               │   │
│  └──────────┬──────────────────────┘   │
│             │                            │
│             │ Internal connection        │
│             ▼                            │
│  ┌─────────────────────────────────┐   │
│  │   PostgreSQL Database            │   │
│  │   - Managed instance            │   │
│  │   - Automatic backups           │   │
│  │   - Connection pooling          │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
             │
             ▼
    https://your-app.onrender.com
```

---

## Prerequisites

### Required Accounts

1. **Render Account**
   - Sign up at https://render.com
   - Free tier available for testing
   - Credit card required for paid plans

2. **GitHub Account**
   - Repository access to `Free-Columns/levelith-2`
   - Push access to deploy branch

### Required Knowledge

- Basic understanding of REST APIs
- Familiarity with environment variables
- PostgreSQL database basics
- Command line usage

### Repository Files (Already Configured)

The repository includes all necessary configuration:

| File | Purpose |
|------|---------|
| `Procfile` | Defines application start command |
| `backend/requirements.txt` | Python dependencies |
| `backend/main.py` | FastAPI application entry point |
| `render.yaml` | Infrastructure as Code blueprint |
| `.env.render.example` | Environment variable template |

:::tip
**Pro Tip:** Review the repository structure before deployment to understand how files are organized and how the application starts.
:::

---

## Deployment Options

### Comparison

| Feature | Blueprint (IaC) | Manual Setup |
|---------|----------------|--------------|
| **Setup Time** | 5 minutes | 25 minutes |
| **Control** | Limited | Full control |
| **Reproducibility** | High | Medium |
| **Learning Curve** | Low | Medium |
| **Configuration Details** | Automated | Explicit |
| **Best For** | Quick deployment | Learning & custom config |

### Choose Your Method

- **Use Blueprint** if you want fast, automated setup with minimal configuration
- **Use Manual** if you need granular control, want to understand each step, or require custom configuration

---

## Option 1: Automated Blueprint Deployment

Infrastructure as Code deployment using `render.yaml` - the fastest way to deploy.

### Steps

#### 1. Push Code to GitHub

```bash
git add .
git commit -m "feat: Add FastAPI backend for Render deployment"
git push origin main
```

#### 2. Connect to Render

1. Go to https://dashboard.render.com
2. Click **"New +"**
3. Select **"Blueprint"**
4. Connect your GitHub repository
5. Select repository with `render.yaml` (`Free-Columns/levelith-2`)
6. Click **"Apply"**

#### 3. Render Automatically Creates

The Blueprint will automatically provision:

- PostgreSQL database (`levelith-db`)
- Web Service (`levelith-backend`)
- Environment variables
- Internal database connections
- Health check monitoring

Wait 3-5 minutes for complete deployment.

#### 4. Verify Deployment

Visit your service URL: `https://levelith-backend.onrender.com/health`

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T...",
  "version": "2.0.0",
  "environment": "production"
}
```

:::success
**Success:** Blueprint deployment handles all configuration automatically. You can customize settings later through the Render dashboard.
:::

### Blueprint Configuration

The `render.yaml` file defines your infrastructure:

```yaml
services:
  - type: web
    name: levelith-backend
    env: python
    plan: starter
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: levelith-db
          property: connectionString
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false

databases:
  - name: levelith-db
    plan: starter
    databaseName: levelith
    user: levelith_user
```

### After Blueprint Deployment

You can still customize your deployment:

1. **Add Additional Environment Variables**
   - Dashboard → Service → Environment
   - Click "Add Environment Variable"

2. **Upgrade Plans**
   - Dashboard → Service → Settings → Plan
   - Select higher tier for more resources

3. **Configure Custom Domain**
   - Dashboard → Service → Settings → Custom Domains
   - Follow DNS setup instructions

---

## Option 2: Manual Step-by-Step Deployment

Complete manual configuration for full control and understanding of each component.

---

## Database Setup

### Option A: Render PostgreSQL (Recommended)

#### 1. Log in to Render Dashboard

Navigate to https://dashboard.render.com

#### 2. Create New PostgreSQL Database

- Click **"New +"** button
- Select **"PostgreSQL"**

#### 3. Configure Database

| Setting | Value | Notes |
|---------|-------|-------|
| **Name** | `levelith-db` | Database instance name |
| **Database** | `levelith` | Actual database name |
| **User** | `levelith_user` | Database username |
| **Region** | Oregon (US West) | Choose closest to your users |
| **Plan** | Free or Starter | Free for testing, Starter ($7/mo) for production |
| **PostgreSQL Version** | 15 | Latest stable version |

#### 4. Create Database

- Click **"Create Database"**
- Wait for provisioning (~2 minutes)
- Status will change to "Available"

#### 5. Copy Connection String

After creation, go to database dashboard and find **"Internal Database URL"**:

```
postgresql://levelith_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/levelith
```

:::warning
**Important:** Use "Internal Database URL" (not External) for better security and performance within Render's network. Internal connections are faster and don't count against your bandwidth quota.
:::

### Option B: External PostgreSQL

If using external PostgreSQL (AWS RDS, DigitalOcean, Supabase, etc.):

**Requirements:**
- Ensure it's publicly accessible or in same VPC
- SSL connection recommended
- Minimum PostgreSQL 12+

**Connection String Format:**
```
postgresql://user:password@host:port/database
```

**Example:**
```
postgresql://myuser:mypass@postgres.example.com:5432/levelith
```

---

## Web Service Setup

### Create Web Service

#### 1. Go to Render Dashboard

- Click **"New +"** → **"Web Service"**

#### 2. Connect Repository

- Select **"Build and deploy from a Git repository"**
- Click **"Connect GitHub"** (if not already connected)
- Find and select **`Free-Columns/levelith-2`**
- Click **"Connect"**

#### 3. Configure Web Service

Fill in the following settings:

| Setting | Value | Notes |
|---------|-------|-------|
| **Name** | `levelith-backend` | Or your preferred name |
| **Region** | Oregon | **Must match database region** |
| **Branch** | `main` | Or your production branch |
| **Root Directory** | Leave blank | Uses repository root |
| **Runtime** | **Python 3** | Auto-detected |
| **Build Command** | `pip install -r backend/requirements.txt` | Installs dependencies |
| **Start Command** | Leave blank | Uses Procfile |
| **Plan** | Free or Starter | Free for testing, Starter for production |

#### 4. Advanced Settings (Optional)

Click **"Advanced"** to expand:

| Setting | Value | Notes |
|---------|-------|-------|
| **Auto-Deploy** | Yes | Recommended for CI/CD |
| **Health Check Path** | `/health` | Monitors service health |
| **Docker Command** | Leave blank | Not using Docker |

:::tip
**Pro Tip:** Enable Auto-Deploy to automatically redeploy whenever you push to your main branch, ensuring your production environment stays in sync with your codebase.
:::

#### 5. Do NOT Click "Create Web Service" Yet!

⚠️ **Important:** First, configure environment variables in the next step to avoid deployment failures.

---

## Environment Variables

### Required Environment Variables

Before creating the service, scroll down to **"Environment Variables"** section and configure the following:

#### Critical Variables (MUST SET)

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | *(from Database Setup)* | Internal Database URL from Render PostgreSQL |
| `SECRET_KEY` | *(generate)* | Click "Generate Value" or use: `openssl rand -hex 32` |
| `ENVIRONMENT` | `production` | Sets production mode |
| `DEBUG` | `false` | Disables debug mode for security |

#### Recommended Variables

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Ensures correct Python version |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `CORS_ORIGINS` | `https://yourdomain.com` | Your frontend URL (comma-separated if multiple) |
| `API_V1_PREFIX` | `/api/v1` | API prefix (default) |

#### Optional Variables

| Key | Value | Notes |
|-----|-------|-------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token expiry duration |
| `DATABASE_POOL_SIZE` | `10` | Connection pool size |
| `DATABASE_MAX_OVERFLOW` | `20` | Max overflow connections |
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `RATE_LIMIT_REQUESTS` | `100` | Requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Window in seconds |

### How to Add Environment Variables

For each variable:

1. Click **"Add Environment Variable"**
2. Enter **Key** (e.g., `DATABASE_URL`)
3. Enter **Value** (e.g., your database URL)
4. Click **"Add"**

Repeat for all required variables.

### Generate SECRET_KEY

**Option 1: Use Render's Generator**
- In the `SECRET_KEY` value field
- Click **"Generate Value"** button
- Render creates a cryptographically secure key

**Option 2: Generate Locally**

```bash
# On Mac/Linux
openssl rand -hex 32

# On Windows (PowerShell)
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# On Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Link Database (Alternative Method)

If you created a Render PostgreSQL database:

1. Scroll to **"Environment Variables"** section
2. Click **"Add from Database"**
3. Select your `levelith-db` database
4. Variable name: `DATABASE_URL`
5. This automatically adds and maintains the connection string

:::tip
**Pro Tip:** Using "Add from Database" automatically keeps the DATABASE_URL in sync if you ever need to recreate or migrate the database. The URL updates automatically if Render moves your database.
:::

### Environment Variable Template

```env
# Critical
DATABASE_URL=postgresql://levelith_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/levelith
SECRET_KEY=your-generated-secret-key-here
ENVIRONMENT=production
DEBUG=false

# Recommended
PYTHON_VERSION=3.11.0
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
API_V1_PREFIX=/api/v1

# Optional
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_POOL_SIZE=10
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

---

## Deploy & Verify

### Create Web Service

#### 1. Review All Settings

Before deployment, verify:

- ✅ Build Command: `pip install -r backend/requirements.txt`
- ✅ Start Command: (blank - uses Procfile)
- ✅ Environment Variables: All required vars set
- ✅ Health Check Path: `/health`
- ✅ Region: Matches database region

#### 2. Click "Create Web Service"

Render begins the deployment process.

#### 3. Wait for Deployment

Render will:

1. **Clone repository** - Downloads your code
2. **Install dependencies** - Runs build command (~3-5 minutes)
3. **Start service** - Executes start command
4. **Run health checks** - Pings `/health` endpoint
5. **Mark as Live** - Service is ready

Watch the **Logs** tab for real-time progress.

#### 4. Deployment Complete

When successful:
- Status shows: ✅ **"Live"**
- Your service URL: `https://levelith-backend.onrender.com`
- Green indicator on dashboard

### Test Health Endpoint

#### Basic Health Check

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

#### Detailed Health Check

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
    "status": "connected",
    "response_time_ms": 12.5
  }
}
```

### Test API Documentation

Visit interactive API docs:

```
https://levelith-backend.onrender.com/docs
```

You should see:
- FastAPI Swagger UI
- All API endpoints listed
- Try out functionality enabled

:::tip
**Pro Tip:** In production, you may want to disable public API documentation by setting `DOCS_ENABLED=false` in environment variables for security.
:::

### Test Sample Endpoints

```bash
# Test root endpoint
curl https://levelith-backend.onrender.com/

# Test API v1
curl https://levelith-backend.onrender.com/api/v1/

# Test specific endpoint (example)
curl https://levelith-backend.onrender.com/api/v1/users/
```

---

## Post-Deployment Configuration

### Update CORS for Frontend

Once you deploy your frontend:

1. Get frontend URL (e.g., `https://levelith-frontend.onrender.com`)
2. Render Dashboard → Backend Service → Environment
3. Edit `CORS_ORIGINS`:
   ```
   https://levelith-frontend.onrender.com,https://levelith.com
   ```
4. Save changes (triggers automatic redeploy)

**Multiple Origins Example:**
```env
CORS_ORIGINS=https://app.levelith.com,https://www.levelith.com,https://admin.levelith.com
```

:::warning
**Important:** Do not include trailing slashes in CORS origins. Use `https://domain.com` not `https://domain.com/`
:::

### Set Up Custom Domain (Optional)

#### 1. Add Custom Domain

1. Render Dashboard → Your Service → Settings
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `api.levelith.com`

#### 2. Configure DNS

Add the following DNS records at your domain provider:

**For subdomain (api.levelith.com):**
```
Type: CNAME
Name: api
Value: levelith-backend.onrender.com
```

**For root domain (levelith.com):**
```
Type: A
Name: @
Value: [IP provided by Render]
```

#### 3. Wait for SSL Certificate

- Render automatically provisions SSL via Let's Encrypt
- Takes ~5 minutes to complete
- Certificate auto-renews every 90 days

:::tip
**Pro Tip:** Render automatically provisions and renews SSL certificates for custom domains using Let's Encrypt - no manual certificate management required!
:::

### Enable Auto-Deploy

Already enabled if you checked "Auto-Deploy" during setup.

**To verify/enable:**
1. Render Dashboard → Your Service → Settings
2. **Auto-Deploy**: Yes
3. **Branch**: `main`

Now, every push to `main` branch automatically deploys!

**Deployment Flow:**
```
git push → GitHub → Render detects change → Auto build → Auto deploy
```

### Configure Webhooks (Optional)

For deployment notifications:

1. Render Dashboard → Your Service → Settings
2. **Deploy Hooks** section
3. Add webhook URL for Slack, Discord, or custom endpoint

### Monitor Service

**Render Dashboard Metrics:**
- CPU usage over time
- Memory usage trends
- Network bandwidth
- Request rate (requests/second)
- Response times (p50, p95, p99)
- Error rates

**Health Check Monitoring:**
- Render pings `/health` every 60 seconds
- Auto-restarts service if 3 consecutive failures
- Email notifications on health check failures (configurable)

**Log Monitoring:**
- Real-time logs in dashboard
- Filter by severity (INFO, WARNING, ERROR)
- Search functionality
- Download logs for analysis

---

## Database Management

### Access Database

#### Using Render Dashboard

1. Go to your PostgreSQL database in Render Dashboard
2. Click **"Connect"** dropdown
3. **Option A:** Use Web Shell
   - Click "PSQL Command"
   - Opens browser-based terminal
   - No local setup required

4. **Option B:** Get connection details
   - External Database URL
   - Internal Database URL
   - Connection string components

#### Using Local psql Client

**Connect with External URL:**
```bash
# Using connection string
psql "postgresql://levelith_user:xxxxx@dpg-xxxxx-a.oregon-postgres.render.com/levelith"

# Or with separate parameters
psql -h dpg-xxxxx-a.oregon-postgres.render.com \
     -U levelith_user \
     -d levelith
```

**Enter password when prompted.**

#### Using pgAdmin

1. **Get connection details** from Render dashboard
2. **Open pgAdmin** → Create New Server
3. **Configure connection:**
   - Name: `Levelith Production`
   - Host: `dpg-xxxxx-a.oregon-postgres.render.com`
   - Port: `5432`
   - Database: `levelith`
   - Username: `levelith_user`
   - Password: [from dashboard]
4. **Save** and connect

### Run Migrations

If using Alembic for database migrations:

```bash
# From local development with DATABASE_URL set
alembic upgrade head

# Or connect to production database directly
export DATABASE_URL="postgresql://levelith_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/levelith"
alembic upgrade head
```

:::danger
**Critical:** Always test migrations on a staging database before running on production. Have a backup ready in case of issues.
:::

### Database Backups

#### Automatic Backups (Paid Plans)

**Render PostgreSQL (Starter plan and above):**
- Automatic daily backups
- 7-day retention on Starter
- 30-day retention on Standard/Pro
- Point-in-time recovery
- Backup access through dashboard

**To restore from backup:**
1. Render Dashboard → Database → Backups
2. Select backup date
3. Click "Restore"
4. Choose restore target (new database or overwrite)

#### Manual Backups (All Plans)

**Using pg_dump:**
```bash
# Get external connection URL from dashboard
export DB_URL="postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com/levelith"

# Create backup
pg_dump $DB_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
pg_dump $DB_URL | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

**Restore from backup:**
```bash
# Restore from SQL file
psql $DB_URL < backup_20251119_103000.sql

# Restore from compressed file
gunzip -c backup_20251119_103000.sql.gz | psql $DB_URL
```

:::warning
**Warning:** Free tier databases have no automatic backups. Upgrade to Starter plan ($7/month) for production use with automatic backup protection.
:::

### Database Maintenance

**Regular tasks:**

1. **Vacuum Database** (reclaim storage)
   ```sql
   VACUUM ANALYZE;
   ```

2. **Reindex** (improve query performance)
   ```sql
   REINDEX DATABASE levelith;
   ```

3. **Check Database Size**
   ```sql
   SELECT 
       pg_database.datname,
       pg_size_pretty(pg_database_size(pg_database.datname)) AS size
   FROM pg_database
   WHERE datname = 'levelith';
   ```

4. **Monitor Connections**
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   ```

---

## Monitoring & Logs

### View Logs

#### Real-time Logs in Dashboard

1. Go to Render Dashboard
2. Select your web service
3. Click **"Logs"** tab

**Log Types:**
- **All Logs**: Complete log stream
- **Deploy Logs**: Build and deployment process
- **Service Logs**: Application runtime logs

**Log Filters:**
- Filter by severity (INFO, WARNING, ERROR)
- Search by keyword
- Time range selection

#### Tail Logs

Watch logs in real-time:
```bash
# From dashboard, logs auto-scroll
# Or use Render CLI (if installed)
render logs levelith-backend --tail
```

### Metrics

Render provides built-in metrics:

**Performance Metrics:**
- **CPU Usage** - Processor utilization over time
- **Memory Usage** - RAM consumption and trends
- **Disk I/O** - Read/write operations
- **Network** - Inbound/outbound bandwidth

**Application Metrics:**
- **Request Count** - Total API traffic
- **Request Rate** - Requests per second
- **Response Times** - P50, P95, P99 latency
- **Error Rates** - 4xx and 5xx responses

**Database Metrics:**
- **Connection Count** - Active connections
- **Query Performance** - Slow queries
- **Storage Usage** - Database size trends

**Access:** Dashboard → Service → Metrics

### Health Monitoring

Render automatically monitors service health:

**Health Check Configuration:**
- Pings `/health` endpoint every 60 seconds
- Expects 200 status code
- 3 consecutive failures trigger restart
- Email notifications on failures (configurable)

**Custom Health Checks:**

You can customize health check behavior in `render.yaml`:

```yaml
services:
  - type: web
    healthCheckPath: /health
    healthCheckInterval: 60
    healthCheckTimeout: 10
    healthCheckSuccessThreshold: 1
    healthCheckFailureThreshold: 3
```

### Set Up Alerts

**Email Notifications:**
1. Dashboard → Account Settings → Notifications
2. Enable service-related notifications
3. Configure alert preferences

**Webhook Alerts:**
1. Dashboard → Service → Settings → Deploy Hooks
2. Add webhook URL (Slack, Discord, PagerDuty, etc.)
3. Configure event triggers

---

## Scaling

### Vertical Scaling

Upgrade plan for more resources (CPU, RAM):

| Plan | RAM | CPU | Price | Use Case |
|------|-----|-----|-------|----------|
| Free | 512 MB | 0.1 | $0/month | Development, testing |
| Starter | 2 GB | 1 | $7/month | Small production apps |
| Standard | 4 GB | 2 | $25/month | Medium traffic |
| Pro | 8 GB | 4 | $85/month | High traffic |
| Pro Plus | 16 GB | 8 | $185/month | Very high traffic |

**How to Upgrade:**
1. Dashboard → Service → Settings
2. **Instance Type** → Select new plan
3. Click "Save"
4. Service restarts with new resources

### Horizontal Scaling

Add multiple instances for load distribution:

**Requirements:**
- Starter plan or above
- Stateless application design
- Database connection pooling

**How to Scale Horizontally:**
1. Dashboard → Service → Settings
2. **Instance Count** → Increase (2-10 instances)
3. Load balancing handled automatically by Render

**Benefits:**
- Better availability (if one instance fails)
- Handle more concurrent requests
- Zero-downtime deployments

**Considerations:**
- Each instance connects to same database
- Ensure database connection pool can handle load
- Session management must be stateless or use Redis

### Database Scaling

Upgrade database plan for better performance:

| Plan | Storage | Connections | RAM | Price | Use Case |
|------|---------|-------------|-----|-------|----------|
| Free | 256 MB | 20 | 0.25 GB | $0/month | Testing |
| Starter | 1 GB | 50 | 1 GB | $7/month | Small apps |
| Standard | 10 GB | 100 | 4 GB | $25/month | Production |
| Pro | 100 GB | 200 | 8 GB | $90/month | High traffic |
| Pro Plus | 512 GB | 400 | 32 GB | $400/month | Enterprise |

**How to Upgrade:**
1. Dashboard → Database → Settings
2. **Plan** → Select new plan
3. Click "Save"
4. Database upgrades with minimal downtime (~1 minute)

:::info
**Note:** Horizontal scaling requires a Starter plan or above. Free tier is limited to single instance. Always monitor database connection count when scaling horizontally.
:::

### Auto-Scaling (Future)

Render is developing auto-scaling features. For now, manual scaling based on metrics is recommended.

**Current Best Practice:**
1. Monitor CPU/Memory metrics
2. Scale up when consistently >70% utilization
3. Scale down during off-peak hours
4. Use database connection pooling

---

## Security Best Practices

### Environment Security

#### 1. Strong SECRET_KEY

Generate a cryptographically secure key:

```bash
# Generate secure key (32 bytes = 64 hex chars)
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Requirements:**
- Minimum 32 characters
- Use random, unpredictable characters
- Never reuse between environments
- Rotate periodically (every 90 days)

#### 2. Disable Debug in Production

```env
# ❌ BAD - Security risk, exposes sensitive data
DEBUG=true

# ✅ GOOD - Secure production configuration
DEBUG=false
ENVIRONMENT=production
```

**Why this matters:**
- Debug mode exposes stack traces with code
- Shows environment variables in errors
- Reveals internal paths and structure
- Performance impact

#### 3. Restrict CORS Origins

```env
# ❌ BAD - Allows any domain
CORS_ORIGINS=*

# ✅ GOOD - Specific domains only
CORS_ORIGINS=https://levelith.com,https://app.levelith.com
```

**Best Practices:**
- List only your domains
- Use HTTPS (never HTTP in production)
- No trailing slashes
- No wildcards in production

### Database Security

#### 1. Use Internal Database URL

```env
# ❌ BAD - External URL (slower, less secure)
DATABASE_URL=postgresql://user:pass@external-dpg-xxxxx-a.oregon-postgres.render.com:5432/db

# ✅ GOOD - Internal URL (faster, more secure)
DATABASE_URL=postgresql://user:pass@dpg-xxxxx/db
```

**Benefits:**
- Faster connection (internal network)
- More secure (no public exposure)
- No bandwidth charges
- Better availability

#### 2. Strong Database Password

- Auto-generated by Render (65+ characters)
- Never share or commit to Git
- Stored securely in Render's vault
- Rotate if compromised

#### 3. Regular Backups

- Enable automatic backups (Starter+ plan)
- Test restore process monthly
- Store off-site backup copies
- Document recovery procedures

### Application Security

#### 1. HTTPS Only

**Automatic via Render:**
- Free SSL certificates
- Auto-renewal every 90 days
- TLS 1.2+ enforced
- HSTS headers recommended

**Force HTTPS in code:**
```python
# In FastAPI middleware
@app.middleware("http")
async def force_https(request, call_next):
    if request.url.scheme != "https":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url))
    return await call_next(request)
```

#### 2. Rate Limiting

```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # seconds
```

**Protects against:**
- Brute force attacks
- API abuse
- DoS attempts
- Scraping

**Implementation:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/users")
@limiter.limit("100/minute")
async def get_users():
    return users
```

#### 3. Keep Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all (with caution)
pip install --upgrade -r requirements.txt
```

**Regular maintenance schedule:**
- Check monthly for security updates
- Test updates in staging first
- Read changelogs for breaking changes
- Pin critical dependency versions

### Additional Security Measures

#### 4. Input Validation

```python
# ✅ GOOD - Validate and sanitize inputs
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3:
            raise ValueError('Username too short')
        return v
```

#### 5. Authentication & Authorization

```python
# Use JWT tokens
# Implement proper password hashing (bcrypt, argon2)
# Require strong passwords
# Implement 2FA for admin accounts
```

#### 6. Security Headers

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Add security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

:::danger
**Critical:** Never commit `.env` files, API keys, passwords, or secrets to Git. Always use environment variables in Render dashboard for sensitive data. Add `.env` to `.gitignore`.
:::

---

## Troubleshooting

### Common Issues

#### ❌ Error: Build Failed

**Symptoms:**
- Deployment fails during build phase
- Error message: "Build failed"
- Service never reaches "Live" status

**Possible Causes:**
- Missing dependencies in requirements.txt
- Incorrect build command
- Python version mismatch
- Syntax errors in code

**Solutions:**

1. **Verify requirements.txt is complete:**
   ```bash
   # Generate fresh requirements.txt
   pip freeze > requirements.txt
   ```

2. **Check build command:**
   ```bash
   # Should be exactly:
   pip install -r backend/requirements.txt
   ```

3. **Set correct Python version:**
   ```env
   PYTHON_VERSION=3.11.0
   ```

4. **Review build logs:**
   - Dashboard → Service → Logs → Deploy Logs
   - Look for specific error messages

#### ❌ Error: Database Connection Failed

**Symptoms:**
- Service starts but health check fails
- Error: "could not connect to database"
- 500 errors on all endpoints

**Possible Causes:**
- Incorrect DATABASE_URL
- Database not running
- Region mismatch (service and DB in different regions)
- Connection limit reached

**Solutions:**

1. **Use Internal Database URL:**
   ```env
   # ✅ Correct format
   DATABASE_URL=postgresql://user:pass@dpg-xxxxx/dbname
   
   # ❌ Wrong - includes region in hostname
   DATABASE_URL=postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/dbname
   ```

2. **Verify database status:**
   - Dashboard → Database → Check status is "Available"

3. **Ensure same region:**
   - Web Service region must match Database region
   - Both should be in "Oregon" (or same region)

4. **Check connection limit:**
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   ```
   - Free tier: max 20 connections
   - Upgrade plan if needed

#### ❌ Error: Application Crash Loop

**Symptoms:**
- Service repeatedly crashes and restarts
- Logs show: "Application error"
- Status flips between "Live" and "Failed"

**Possible Causes:**
- Missing environment variables
- Uncaught exceptions in startup code
- Port binding issues
- Out of memory

**Solutions:**

1. **Check for missing environment variables:**
   ```python
   # Add validation in code
   import os
   required_vars = ['DATABASE_URL', 'SECRET_KEY', 'ENVIRONMENT']
   for var in required_vars:
       if not os.getenv(var):
           raise ValueError(f"Missing required env var: {var}")
   ```

2. **Review startup logs:**
   - Look for Python tracebacks
   - Check for import errors
   - Verify database migrations ran

3. **Ensure correct port binding:**
   ```python
   # ✅ Correct - use PORT from environment
   port = int(os.getenv("PORT", 8000))
   
   # ❌ Wrong - hardcoded port
   port = 8000
   ```

4. **Monitor memory usage:**
   - Dashboard → Metrics → Memory
   - Upgrade plan if consistently >90%

#### ❌ Error: CORS Errors from Frontend

**Symptoms:**
- Frontend receives CORS policy errors
- Browser console: "Access to fetch... has been blocked by CORS policy"
- API works in Postman but not browser

**Cause:**
- Frontend URL not in `CORS_ORIGINS`
- Incorrect CORS configuration
- Missing protocol (https://)

**Solutions:**

1. **Add frontend URL to CORS_ORIGINS:**
   ```env
   # Format: https://domain (no trailing slash)
   CORS_ORIGINS=https://levelith-frontend.onrender.com
   ```

2. **Multiple origins:**
   ```env
   CORS_ORIGINS=https://app.levelith.com,https://www.levelith.com
   ```

3. **Verify CORS middleware configuration:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

#### ❌ Error: Service Returns 500 Errors

**Symptoms:**
- Service starts but API endpoints return 500 Internal Server Error
- Health endpoint works but others fail
- Intermittent errors

**Causes:**
- Missing environment variables
- Database query errors
- Unhandled exceptions
- Import/dependency errors

**Solutions:**

1. **Check Render logs for detailed error messages:**
   - Dashboard → Logs → Filter by ERROR

2. **Enable debug temporarily:**
   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```

3. **Common issues:**
   - Missing `SECRET_KEY` environment variable
   - Invalid `DATABASE_URL` format
   - Missing dependencies in requirements.txt
   - Database schema mismatch (need migrations)

4. **Test locally with production environment:**
   ```bash
   # Use same DATABASE_URL as production
   export DATABASE_URL="postgresql://..."
   uvicorn main:app --reload
   ```

5. **Remember to disable debug after fixing:**
   ```env
   DEBUG=false
   LOG_LEVEL=INFO
   ```

#### ⚠️ Warning: Slow Response Times

**Symptoms:**
- API responds but takes >1 second
- Timeout errors under load
- Poor user experience

**Possible Causes:**
- Insufficient resources (Free tier)
- Database query optimization needed
- Cold starts (free tier sleeps after 15min)
- Connection pool exhaustion

**Solutions:**

1. **Upgrade to Starter plan:**
   - Eliminates cold starts
   - Better CPU/RAM allocation
   - Dedicated resources

2. **Optimize database queries:**
   ```sql
   -- Add indexes for frequently queried columns
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   
   -- Analyze slow queries
   EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
   ```

3. **Increase connection pool size:**
   ```env
   DATABASE_POOL_SIZE=20
   DATABASE_MAX_OVERFLOW=40
   ```

4. **Add database indexes:**
   ```python
   # In SQLAlchemy models
   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       email = Column(String, index=True)  # ← Add index
   ```

5. **Implement caching:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_user(user_id: int):
       return db.query(User).filter(User.id == user_id).first()
   ```

#### ⚠️ Warning: Free Tier Sleep

**Symptoms:**
- First request after 15 minutes is very slow (>30 seconds)
- Subsequent requests are fast
- Service shows "Sleeping" in dashboard

**Cause:**
- Free tier services sleep after 15 minutes of inactivity

**Solutions:**

1. **Upgrade to Starter plan ($7/month):**
   - No sleep behavior
   - Always ready to serve requests

2. **Keep-alive service (temporary workaround):**
   ```bash
   # External cron job pings your service every 14 minutes
   # Use services like cron-job.org or UptimeRobot
   curl https://levelith-backend.onrender.com/health
   ```

:::tip
**Note:** Keep-alive workarounds are against Render's terms of service for free tier. Upgrade to paid plan for production use.
:::

### Deployment Verification Checklist

After deployment, verify:

- [ ] Health endpoint returns 200 OK
- [ ] Database connection successful
- [ ] API documentation accessible
- [ ] CORS configured for frontend
- [ ] Environment variables set correctly
- [ ] Logs show no errors
- [ ] SSL certificate active (HTTPS)
- [ ] Custom domain (if configured) working
- [ ] Auto-deploy enabled
- [ ] Monitoring alerts configured

---

## Cost Breakdown

### Development Setup (Free Tier)

**Services:**
- **Web Service**: Free (512MB RAM)
  - Sleeps after 15 minutes inactivity
  - Slower cold starts (~30 seconds)
  - Limited to 1 instance

- **PostgreSQL**: Free (256MB storage)
  - No automatic backups
  - 20 concurrent connections max
  - May be deleted after 90 days of inactivity

**Total**: **$0/month**

:::warning
**Warning:** Free tier services sleep after 15 minutes of inactivity and may have slow cold starts. Not recommended for production or public-facing applications.
:::

### Minimal Production Setup

**Services:**
- **Web Service** (Starter): $7/month
  - 2GB RAM, 1 CPU
  - No sleep behavior
  - Always-on
  - SSL included

- **PostgreSQL** (Starter): $7/month
  - 1GB storage
  - Automatic daily backups (7-day retention)
  - 50 concurrent connections

**Total**: **$14/month**

**Best for:**
- Small production applications
- Low to medium traffic (<10K requests/day)
- Startups and side projects

### Recommended Production Setup

**Services:**
- **Web Service** (Standard): $25/month
  - 4GB RAM, 2 CPU
  - Better performance
  - Handle more concurrent requests

- **PostgreSQL** (Standard): $25/month
  - 10GB storage
  - Automatic daily backups (30-day retention)
  - 100 concurrent connections
  - Better query performance

**Total**: **$50/month**

**Best for:**
- Medium traffic applications (10K-100K requests/day)
- Business-critical applications
- Growing startups

### High-Traffic Production Setup

**Services:**
- **Web Service** (Pro): $85/month
  - 8GB RAM, 4 CPU
  - High performance
  - Multiple instances supported

- **PostgreSQL** (Pro): $90/month
  - 100GB storage
  - Automatic backups
  - 200 concurrent connections
  - High-performance queries

**Total**: **$175/month**

**Best for:**
- High traffic applications (>100K requests/day)
- Enterprise applications
- Applications requiring high availability

### Additional Costs

**Optional Services:**
- **Redis** (for caching): $10-$50/month
- **Custom domains**: Free (SSL included)
- **Additional bandwidth**: Included in plan
- **Outbound data transfer**: First 100GB free, then $0.10/GB

---

## Best Practices Summary

### ✅ DO

1. **Use Infrastructure as Code**
   ```yaml
   # ✅ GOOD - Version controlled infrastructure
   # render.yaml defines all resources
   services:
     - type: web
       name: levelith-backend
   ```

2. **Enable Auto-Deploy**
   - Automatic deployments on push to main
   - Ensures production stays in sync
   - Reduces manual deployment errors

3. **Monitor Logs Regularly**
   - Check for errors and warnings daily
   - Set up alerts for critical issues
   - Review performance metrics weekly

4. **Use Internal Database URL**
   - Faster connection
   - More secure
   - No bandwidth charges

5. **Implement Health Checks**
   ```python
   @app.get("/health")
   async def health():
       return {"status": "healthy", "timestamp": datetime.utcnow()}
   ```

6. **Keep Dependencies Updated**
   - Monthly security update reviews
   - Test in staging first
   - Pin critical versions

### ❌ DON'T

1. **Don't Hardcode Secrets**
   ```python
   # ❌ BAD - Hardcoded credentials
   DATABASE_URL = "postgresql://user:pass@host/db"
   SECRET_KEY = "my-secret-key-123"

   # ✅ GOOD - Use environment variables
   DATABASE_URL = os.getenv("DATABASE_URL")
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Don't Use External Database URL Internally**
   ```env
   # ❌ BAD - Slower, less secure
   DATABASE_URL=postgresql://external-host.com:5432/db

   # ✅ GOOD - Internal URL for services on Render
   DATABASE_URL=postgresql://internal-host/db
   ```

3. **Don't Skip Health Checks**
   ```python
   # ❌ BAD - No health monitoring
   # (no /health endpoint)

   # ✅ GOOD - Proper health checks
   @app.get("/health")
   async def health():
       return {"status": "healthy"}
   ```

4. **Don't Commit Secrets**
   ```bash
   # ❌ BAD - Never commit .env files
   git add .env

   # ✅ GOOD - Use .env.example
   git add .env.example
   ```

5. **Don't Leave Debug Enabled**
   ```env
   # ❌ BAD - Security risk
   DEBUG=true

   # ✅ GOOD - Disabled in production
   DEBUG=false
   ```

6. **Don't Use Free Tier for Production**
   - Service sleeps after 15 minutes
   - No backups
   - Limited resources
   - May be deleted after 90 days

---

## Additional Resources

### Official Documentation

- 📚 [Render Documentation](https://render.com/docs)
- 🏗️ [Render Web Services Guide](https://render.com/docs/web-services)
- 🧪 [Render PostgreSQL Guide](https://render.com/docs/databases)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com)
- 🐍 [Python Best Practices](https://docs.python-guide.org)

### Internal Documentation

- 📋 [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)
- 🎯 [API Documentation](/docs/api/API_DOCUMENTATION.md)
- 🏛️ [Architecture Overview](/docs/architecture/ARCHITECTURE.md)
- 🔧 [Environment Configuration](/docs/guides/ENVIRONMENT_SETUP.md)
- 🚀 [CI/CD Pipeline](/docs/guides/CICD.md)

### External Resources

- 🌐 [Render Status Page](https://status.render.com)
- 💻 [Render Community](https://community.render.com)
- 🐛 [GitHub Repository](https://github.com/Free-Columns/levelith-2)
- 📊 [Render Blog](https://render.com/blog)

### Tutorials & Guides

- [FastAPI + PostgreSQL + Render Tutorial](https://testdriven.io/blog/fastapi-render/)
- [Database Migration Strategies](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

### Support Channels

- 💬 [Render Support](https://render.com/support) - Official support
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues) - Bug reports
- ❓ [Discussions](https://github.com/Free-Columns/levelith-2/discussions) - Q&A
- 💡 [Stack Overflow](https://stackoverflow.com/questions/tagged/render) - Community help

---

## Related Documentation

- **Previous:** [Architecture Overview](/docs/architecture/ARCHITECTURE.md)
- **Next:** [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)

**Other related documentation:**

- [Environment Configuration](/docs/guides/ENVIRONMENT_SETUP.md)
- [CI/CD Pipeline](/docs/guides/CICD.md)
- [Testing Guide](/docs/testing/TESTING.md)
- [Contributing Guidelines](/CONTRIBUTING.md)

---

## Quick Reference

### Essential Commands

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Connect to database
psql "postgresql://user:pass@host/db"

# Backup database
pg_dump DATABASE_URL > backup.sql

# Test health endpoint
curl https://your-app.onrender.com/health

# View logs (if using Render CLI)
render logs your-service-name --tail
```

### Environment Variable Template

```env
# Critical
DATABASE_URL=postgresql://user:pass@dpg-xxxxx/db
SECRET_KEY=your-64-char-hex-key
ENVIRONMENT=production
DEBUG=false

# Recommended
PYTHON_VERSION=3.11.0
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
API_V1_PREFIX=/api/v1

# Optional
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_POOL_SIZE=10
RATE_LIMIT_ENABLED=true
```

### Common URLs

```
Service URL:     https://your-app.onrender.com
Health Check:    https://your-app.onrender.com/health
API Docs:        https://your-app.onrender.com/docs
Dashboard:       https://dashboard.render.com
Status Page:     https://status.render.com
```

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Star us on [GitHub](https://github.com/Free-Columns/levelith-2)
- 🐛 **Found a bug?** [Report it](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)
- 📝 **Improve docs?** Submit a pull request

---

**Last Updated:** November 19, 2025 | **Version:** 2.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions or support, visit our [GitHub repository](https://github.com/Free-Columns/levelith-2).*
