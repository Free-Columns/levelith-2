# Levelith Backend - Render Deployment Guide

## Overview

This guide covers deploying the Levelith FastAPI backend to Render Web Service with managed PostgreSQL.

## Architecture

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Platform**: Render Web Service
- **Database**: Render PostgreSQL (Managed)
- **Deployment**: Infrastructure as Code (render.yaml)

## Prerequisites

1. Render account: https://render.com
2. GitHub repository connected to Render
3. This codebase pushed to your repository

## Deployment Options

### Option 1: Automated Deployment (Recommended)

Use the `render.yaml` Infrastructure as Code configuration.

#### Steps:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "feat: Add FastAPI backend for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +"
   - Select "Blueprint"
   - Connect your GitHub repository
   - Select the repository with `render.yaml`
   - Click "Apply"

3. **Render will automatically:**
   - Create PostgreSQL database (`levelith-db`)
   - Create Web Service (`levelith-backend`)
   - Set environment variables
   - Deploy the application

4. **Verify deployment**
   - Visit your service URL: `https://levelith-backend.onrender.com/health`
   - Should return: `{"status": "healthy", ...}`

### Option 2: Manual Deployment

If you prefer manual setup through the Render Dashboard:

#### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configuration:
   - **Name**: levelith-db
   - **Database**: levelith
   - **User**: levelith_user
   - **Region**: Oregon (or your preference)
   - **Plan**: Starter ($7/month)
4. Click "Create Database"
5. Save the **Internal Database URL** (starts with `postgresql://`)

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configuration:
   - **Name**: levelith-backend
   - **Region**: Oregon (same as database)
   - **Branch**: main
   - **Root Directory**: Leave blank
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Starter ($7/month)

4. **Environment Variables**:
   Click "Add Environment Variable" for each:

   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.11.0` |
   | `ENVIRONMENT` | `production` |
   | `DEBUG` | `false` |
   | `DATABASE_URL` | Paste Internal Database URL from Step 1 |
   | `SECRET_KEY` | Generate with: `openssl rand -hex 32` |
   | `CORS_ORIGINS` | `https://your-frontend-url.onrender.com` |
   | `LOG_LEVEL` | `INFO` |

5. Click "Create Web Service"

## Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | Secret key for JWT/sessions | Random 64-char hex string |
| `ENVIRONMENT` | Deployment environment | `production` |
| `DEBUG` | Enable debug mode | `false` |
| `CORS_ORIGINS` | Allowed CORS origins | Comma-separated URLs |
| `LOG_LEVEL` | Logging verbosity | `INFO`, `DEBUG`, `WARNING` |

## Health Checks

Render monitors your service health using these endpoints:

- **Health**: `/health` - Basic health check
- **Readiness**: `/health/ready` - Database connectivity check
- **Liveness**: `/health/live` - Service alive check

## Post-Deployment Verification

### 1. Check Service Health

```bash
curl https://your-service.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-17T...",
  "service": "Levelith API",
  "version": "2.0.0"
}
```

### 2. Check Database Connection

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

### 3. Access API Documentation

Visit: `https://your-service.onrender.com/docs`

Note: API docs are disabled in production by default for security.

### 4. Test API Endpoints

Create a user:
```bash
curl -X POST https://your-service.onrender.com/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

## Database Management

### Access Database

1. Go to Render Dashboard → Your Database
2. Click "Connect" → Copy connection string
3. Use with any PostgreSQL client:
   ```bash
   psql <connection-string>
   ```

### Run Migrations

Migrations run automatically on deployment via the database initialization in `main.py`.

For manual migration:
```bash
# SSH into Render shell (available on paid plans)
python -c "from backend.database import init_db; init_db()"
```

### Backup Database

Render automatically backs up your database:
- **Starter Plan**: Daily backups, 7-day retention
- **Standard Plan**: Continuous backups

Manual backup:
```bash
pg_dump <connection-string> > backup.sql
```

## Monitoring & Logs

### View Logs

1. Go to Render Dashboard → Your Service
2. Click "Logs" tab
3. Real-time log streaming

### Metrics

Render provides:
- CPU usage
- Memory usage
- Request count
- Response times

Access: Dashboard → Service → Metrics

## Scaling

### Vertical Scaling

Upgrade your plan for more resources:
- **Starter**: 512 MB RAM, 0.5 CPU
- **Standard**: 2 GB RAM, 1 CPU
- **Pro**: 4 GB RAM, 2 CPU

### Horizontal Scaling

Add multiple instances:
1. Dashboard → Service → Settings
2. "Instance Count" → Increase
3. Load balancing handled automatically

## Custom Domain

### Add Custom Domain

1. Dashboard → Service → Settings
2. "Custom Domain" → Add domain
3. Add DNS records:
   ```
   CNAME www your-service.onrender.com
   A     @   <Render IP>
   ```

### SSL Certificate

Render provides free SSL certificates automatically via Let's Encrypt.

## Troubleshooting

### Service Won't Start

**Check logs for errors:**
```
Dashboard → Service → Logs
```

**Common issues:**
- Missing environment variables
- Database connection failure
- Port binding issues

### Database Connection Errors

1. Verify `DATABASE_URL` is correct
2. Check database is running: Dashboard → Database
3. Ensure database and service in same region

### Health Check Failures

Test locally:
```bash
cd backend
python main.py
curl http://localhost:8000/health
```

### Import Errors

Ensure all dependencies in `requirements.txt`:
```bash
cd backend
pip freeze > requirements.txt
```

## Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Use strong SECRET_KEY**: Generate with `openssl rand -hex 32`
3. **Enable HTTPS**: Render provides this automatically
4. **Restrict CORS**: Set specific origins, not `*`
5. **Disable debug in production**: `DEBUG=false`
6. **Regular updates**: Keep dependencies updated

## Cost Breakdown

### Minimal Setup (Development)
- Web Service (Starter): $7/month
- PostgreSQL (Starter): $7/month
- **Total**: $14/month

### Production Setup
- Web Service (Standard): $25/month
- PostgreSQL (Standard): $25/month
- **Total**: $50/month

### Free Tier
Render offers free tier for testing:
- Web Service: Free (sleeps after inactivity)
- PostgreSQL: Free tier available (limited storage)

## CI/CD Integration

Render automatically deploys on:
- Push to main branch (default)
- Pull request merges
- Manual triggers

### Customize Deployment

Edit `render.yaml`:
```yaml
services:
  - type: web
    name: levelith-backend
    autoDeploy: true  # Auto-deploy on push
    branch: main      # Deploy from this branch
```

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Render Support**: support@render.com
- **Community**: https://community.render.com

## Next Steps

1. ✅ Deploy backend to Render
2. Deploy frontend to Render Static Site
3. Connect frontend to backend API
4. Set up monitoring and alerts
5. Configure custom domain
6. Set up staging environment

---

**Deployed Successfully?** Access your API at: `https://your-service.onrender.com/docs`
