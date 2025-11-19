# Levelith Backend Deployment Guide

---
title: "Levelith Backend Deployment Guide"
description: "General deployment guide for Levelith FastAPI backend covering Render Web Service, infrastructure as code, and production best practices."
category: "guides"
tags: ["deployment", "render", "fastapi", "infrastructure", "production"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 20
relatedPages:
  - "/docs/deployment/RENDER_DEPLOYMENT.md"
  - "/docs/deployment/DATABASE_SETUP_NOTES.md"
  - "/docs/architecture/ARCHITECTURE.md"
nextPage: "/docs/deployment/RENDER_DEPLOYMENT.md"
prevPage: "/docs/architecture/ARCHITECTURE.md"
searchKeywords:
  - "deployment"
  - "render"
  - "infrastructure as code"
  - "blueprint"
  - "production deployment"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Levelith Backend Deployment Guide

> **TL;DR:** Deploy Levelith FastAPI backend to Render using either automated Blueprint (Infrastructure as Code) or manual web service setup with managed PostgreSQL database.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 20 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
- [Option 1: Automated Blueprint Deployment](#option-1-automated-blueprint-deployment)
- [Option 2: Manual Deployment](#option-2-manual-deployment)
- [Post-Deployment Verification](#post-deployment-verification)
- [Database Management](#database-management)
- [Monitoring & Logs](#monitoring--logs)
- [Scaling](#scaling)
- [Security Best Practices](#security-best-practices)
- [Additional Resources](#additional-resources)

---

## Overview

This guide covers deploying the Levelith FastAPI backend to Render Web Service with managed PostgreSQL database. Render provides a fully managed platform with automatic SSL, health monitoring, and easy scaling.

### Key Features

- ✅ **Managed PostgreSQL** - Automatic backups and scaling
- ✅ **Auto-Deploy** - CI/CD integration with GitHub
- ✅ **Health Monitoring** - Automatic restart on failures
- ✅ **SSL/HTTPS** - Free certificates via Let's Encrypt
- ✅ **Custom Domains** - Easy DNS configuration
- ✅ **Environment Variables** - Secure secrets management

:::info
**Note:** This guide covers general deployment concepts. For detailed step-by-step instructions, see the [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md).
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

2. **GitHub Account**
   - Repository access to `Free-Columns/levelith-2`
   - Push access to deploy branch

### Required Knowledge

- Basic understanding of REST APIs
- Familiarity with environment variables
- PostgreSQL database basics
- Command line usage

### Repository Files

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
| **Setup Time** | 5 minutes | 15 minutes |
| **Control** | Limited | Full control |
| **Reproducibility** | High | Medium |
| **Learning Curve** | Low | Medium |
| **Best For** | Quick deployment | Custom configuration |

### Choose Your Method

- **Use Blueprint** if you want fast, automated setup
- **Use Manual** if you need granular control or learning

---

## Option 1: Automated Blueprint Deployment

Infrastructure as Code deployment using `render.yaml`.

### Steps

1. **Push Code to GitHub**

   ```bash
   git add .
   git commit -m "feat: Add FastAPI backend for Render deployment"
   git push origin main
   ```

2. **Connect to Render**

   - Go to https://dashboard.render.com
   - Click **"New +"**
   - Select **"Blueprint"**
   - Connect your GitHub repository
   - Select repository with `render.yaml`
   - Click **"Apply"**

3. **Render Automatically Creates:**

   - PostgreSQL database (`levelith-db`)
   - Web Service (`levelith-backend`)
   - Environment variables
   - Deploys the application

4. **Verify Deployment**

   Visit your service URL: `https://levelith-backend.onrender.com/health`

   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-11-19T...",
     "version": "2.0.0"
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

databases:
  - name: levelith-db
    plan: starter
    databaseName: levelith
    user: levelith_user
```

---

## Option 2: Manual Deployment

Step-by-step manual configuration through Render dashboard.

### Step 1: Create PostgreSQL Database

1. **Go to Render Dashboard**

   Navigate to https://dashboard.render.com

2. **Create Database**

   - Click **"New +"** → **"PostgreSQL"**
   - Configure settings:

   | Setting | Value |
   |---------|-------|
   | Name | `levelith-db` |
   | Database | `levelith` |
   | User | `levelith_user` |
   | Region | Oregon (US West) |
   | Plan | Starter ($7/month) |

3. **Save Connection String**

   Copy the **Internal Database URL** for later use

### Step 2: Create Web Service

1. **Create Service**

   - Click **"New +"** → **"Web Service"**
   - Connect GitHub repository
   - Select `Free-Columns/levelith-2`

2. **Configure Service**

   | Setting | Value |
   |---------|-------|
   | Name | `levelith-backend` |
   | Region | Oregon (same as database) |
   | Branch | `main` |
   | Runtime | Python 3 |
   | Build Command | `pip install -r backend/requirements.txt` |
   | Start Command | Leave blank (uses Procfile) |

3. **Add Environment Variables**

   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | Your Internal Database URL |
   | `SECRET_KEY` | Generate with: `openssl rand -hex 32` |
   | `ENVIRONMENT` | `production` |
   | `DEBUG` | `false` |
   | `LOG_LEVEL` | `INFO` |

4. **Create Web Service**

   Click **"Create Web Service"** and wait for deployment

:::warning
**Important:** Always use the Internal Database URL for better security and performance. External URLs should only be used for connections from outside Render's network.
:::

### Step 3: Verify Deployment

Test the health endpoint:

```bash
curl https://levelith-backend.onrender.com/health
```

For detailed manual setup instructions, see [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md).

---

## Post-Deployment Verification

### Health Checks

**Basic Health Check:**
```bash
curl https://your-service.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T10:30:00.000000",
  "service": "Levelith API",
  "version": "2.0.0"
}
```

**Database Health Check:**
```bash
curl https://your-service.onrender.com/health/ready
```

Expected response:
```json
{
  "status": "ready",
  "checks": {
    "database": true
  }
}
```

### API Documentation

:::danger
**Critical:** API documentation is disabled in production by default for security. Only enable temporarily for testing.
:::

To access API docs (development only):
1. Set `DEBUG=true` temporarily
2. Visit: `https://your-service.onrender.com/docs`
3. **Remember to set `DEBUG=false` after testing**

### Test API Endpoints

**Create a User:**
```bash
curl -X POST https://your-service.onrender.com/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

**Get User:**
```bash
curl https://your-service.onrender.com/api/v1/users/1
```

---

## Database Management

### Access Database

1. Go to Render Dashboard → Your Database
2. Click **"Connect"** → Copy connection string
3. Use with any PostgreSQL client:

   ```bash
   psql <connection-string>
   ```

### Database Migrations

Migrations run automatically on deployment via database initialization in `main.py`.

For manual migration:
```bash
# Via Render shell (paid plans only)
python -c "from backend.database import init_db; init_db()"
```

### Backup Database

**Automatic Backups** (Starter plan and above):
- Daily backups
- 7-day retention (Starter)
- Continuous backups (Standard)

**Manual Backup:**
```bash
pg_dump <connection-string> > backup.sql
```

**Restore from Backup:**
```bash
psql <connection-string> < backup.sql
```

:::tip
**Pro Tip:** Set up a scheduled backup script using GitHub Actions or Render Cron Jobs to ensure regular backups even on free tier.
:::

---

## Monitoring & Logs

### View Logs

**Via Render Dashboard:**
1. Go to Render Dashboard → Your Service
2. Click **"Logs"** tab
3. Real-time log streaming

**Log Filters:**
- **All Logs** - Complete output
- **Deploy Logs** - Build and deployment
- **Service Logs** - Application runtime

### Metrics

Render provides built-in metrics:
- **CPU Usage** - Processor utilization
- **Memory Usage** - RAM consumption
- **Request Count** - API traffic
- **Response Times** - Performance metrics

Access: Dashboard → Service → Metrics

### Health Monitoring

Render automatically monitors service health:
- Pings `/health` endpoint every 60 seconds
- Auto-restarts service if health check fails
- Email notifications on failures (configurable)

---

## Scaling

### Vertical Scaling

Upgrade plan for more resources:

| Plan | RAM | CPU | Price |
|------|-----|-----|-------|
| Free | 512 MB | 0.1 | $0/month |
| Starter | 2 GB | 1 | $7/month |
| Standard | 4 GB | 2 | $25/month |
| Pro | 8 GB | 4 | $85/month |

### Horizontal Scaling

Add multiple instances:
1. Dashboard → Service → Settings
2. **Instance Count** → Increase
3. Load balancing handled automatically

### Database Scaling

Upgrade database plan for better performance:

| Plan | Storage | Connections | Price |
|------|---------|-------------|-------|
| Free | 256 MB | 20 | $0/month |
| Starter | 1 GB | 50 | $7/month |
| Standard | 10 GB | 100 | $25/month |
| Pro | 100 GB | 200 | $90/month |

:::info
**Note:** Horizontal scaling requires a Starter plan or above. Free tier is limited to single instance.
:::

---

## Security Best Practices

### Environment Security

1. **Strong SECRET_KEY**
   ```bash
   # Generate secure key
   openssl rand -hex 32
   ```

2. **Disable Debug in Production**
   ```env
   DEBUG=false
   ENVIRONMENT=production
   ```

3. **Restrict CORS Origins**
   ```env
   # Specific domains only
   CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
   ```

### Database Security

1. **Use Internal Database URL**
   - Faster connection
   - More secure (internal network)
   - No public exposure

2. **Strong Database Password**
   - Auto-generated by Render
   - Never share or commit to Git

3. **Regular Backups**
   - Enable automatic backups (Starter+)
   - Test restore process regularly

### Application Security

1. **HTTPS Only**
   - Automatic via Render
   - Free SSL certificates
   - Auto-renewal

2. **Rate Limiting**
   ```env
   RATE_LIMIT_ENABLED=true
   RATE_LIMIT_REQUESTS=100
   RATE_LIMIT_WINDOW=60
   ```

3. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

:::danger
**Critical:** Never commit `.env` files or secrets to Git. Always use environment variables in Render dashboard for sensitive data.
:::

---

## Best Practices

### ✅ DO

1. **Use Infrastructure as Code**
   ```yaml
   # ✅ GOOD - Version controlled infrastructure
   # render.yaml defines all resources
   ```

2. **Enable Auto-Deploy**
   - Automatic deployments on push to main
   - Ensures production stays in sync

3. **Monitor Logs Regularly**
   - Check for errors and warnings
   - Set up alerts for critical issues

### ❌ DON'T

1. **Don't Hardcode Secrets**
   ```python
   # ❌ BAD - Hardcoded credentials
   DATABASE_URL = "postgresql://user:pass@host/db"

   # ✅ GOOD - Use environment variables
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

2. **Don't Use External Database URL Internally**
   ```env
   # ❌ BAD - Slower, less secure
   DATABASE_URL=postgresql://external-host:5432/db

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

---

## Troubleshooting

### Common Issues

<details>
<summary><strong>❌ Error: Build Failed</strong></summary>

**Possible Causes:**
- Missing dependencies in requirements.txt
- Incorrect build command
- Python version mismatch

**Solutions:**
1. Verify `requirements.txt` is complete
2. Check build command: `pip install -r backend/requirements.txt`
3. Set `PYTHON_VERSION=3.11.0` in environment variables
</details>

<details>
<summary><strong>❌ Error: Database Connection Failed</strong></summary>

**Possible Causes:**
- Incorrect DATABASE_URL
- Database not running
- Region mismatch

**Solutions:**
1. Use Internal Database URL
2. Verify database status in dashboard
3. Ensure database and service in same region
</details>

<details>
<summary><strong>⚠️ Warning: Slow Response Times</strong></summary>

**Possible Causes:**
- Insufficient resources
- Database query optimization needed
- Cold starts (free tier)

**Solutions:**
1. Upgrade to Starter plan (no cold starts)
2. Optimize database queries
3. Increase connection pool size
4. Add database indexes
</details>

---

## Cost Breakdown

### Development Setup (Free)
- **Web Service**: Free (with limitations)
- **PostgreSQL**: Free (256MB)
- **Total**: $0/month

:::warning
**Warning:** Free tier services sleep after 15 minutes of inactivity and may have slow cold starts.
:::

### Production Setup (Minimal)
- **Web Service** (Starter): $7/month
- **PostgreSQL** (Starter): $7/month
- **Total**: $14/month

### Production Setup (Recommended)
- **Web Service** (Standard): $25/month
- **PostgreSQL** (Standard): $25/month
- **Total**: $50/month

---

## Additional Resources

### Official Documentation

- 📚 [Render Documentation](https://render.com/docs)
- 🏗️ [Render Web Services](https://render.com/docs/web-services)
- 🧪 [Render PostgreSQL](https://render.com/docs/databases)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com)

### Internal Documentation

- 📋 [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)
- 🔧 [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)
- 🎯 [API Documentation](/docs/api/API_DOCUMENTATION.md)
- 🏛️ [Architecture Overview](/docs/architecture/ARCHITECTURE.md)

### External Resources

- 🌐 [Render Status Page](https://status.render.com)
- 💻 [Render Community](https://community.render.com)
- 🐛 [GitHub Repository](https://github.com/Free-Columns/levelith-2)

### Support

- 💬 [Render Support](https://render.com/support)
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues)
- ❓ [Discussions](https://github.com/Free-Columns/levelith-2/discussions)

---

## Related Documentation

- **Previous:** [Architecture Overview](/docs/architecture/ARCHITECTURE.md)
- **Next:** [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)

**Other related documentation:**

- [Database Setup Notes](/docs/deployment/DATABASE_SETUP_NOTES.md)
- [Environment Configuration](/docs/guides/ENVIRONMENT_SETUP.md)
- [CI/CD Pipeline](/docs/guides/CICD.md)

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
