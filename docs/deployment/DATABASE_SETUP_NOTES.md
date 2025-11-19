# Database Setup Notes

---
title: "Database Setup Notes"
description: "Complete database integration notes for Levelith Backend including PostgreSQL setup, initialization scripts, security configuration, and troubleshooting."
category: "reference"
tags: ["database", "postgresql", "setup", "configuration", "migration"]
author: "Semour Media Group"
date: "2025-11-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 15
relatedPages:
  - "/docs/deployment/RENDER_DEPLOYMENT.md"
  - "/docs/deployment/DEPLOYMENT.md"
  - "/docs/api/API_DOCUMENTATION.md"
nextPage: "/docs/api/API_DOCUMENTATION.md"
prevPage: "/docs/deployment/RENDER_DEPLOYMENT.md"
searchKeywords:
  - "database setup"
  - "postgresql"
  - "database migration"
  - "init_db"
  - "database configuration"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Database Setup Notes

> **TL;DR:** Levelith backend is fully configured for PostgreSQL on Render with automated initialization, proper security, and comprehensive database models for all experience types.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 15 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Database Integration Complete](#database-integration-complete)
- [Configuration Files](#configuration-files)
- [Database URL Configuration](#database-url-configuration)
- [Database Initialization](#database-initialization)
- [Database Models](#database-models)
- [Security Configuration](#security-configuration)
- [Testing Database Connection](#testing-database-connection)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## Overview

The Levelith backend is fully integrated with PostgreSQL and ready for deployment on Render. This document covers the database setup, configuration, initialization process, and common issues.

### What's Included

- ✅ **PostgreSQL Integration** - Fully configured and tested
- ✅ **Database Models** - User and 9 experience types
- ✅ **Initialization Script** - Automated table creation
- ✅ **Security** - Secure credentials and password hashing
- ✅ **Environment Configuration** - Local and production configs

:::info
**Note:** All database configuration is complete. You only need to verify the database URL and initialize the tables.
:::

---

## Database Integration Complete

### Implementation Status

1. **Environment Configuration** ✅
   - `.env` file created for local development
   - `.env.render.production` file created with production values
   - Config validator fixed to properly parse CORS origins

2. **Database Initialization Script** ✅
   - `backend/init_db.py` - Comprehensive database initialization tool
   - Features:
     - `--check`: Test database connection
     - `--reset`: Drop and recreate all tables (dev only)
     - Safe to run multiple times

3. **Database Models** ✅
   - User model (`UserDB`) - Ready to use
   - Experience models (9 types) - All configured
   - Relationships properly defined

4. **Security** ✅
   - Generated secure SECRET_KEY for JWT authentication
   - Credentials in .env files (gitignored)
   - Proper password hashing configured

---

## Configuration Files

### Environment Files Created

| File | Purpose | Status |
|------|---------|--------|
| `backend/.env` | Local development configuration | ✅ Created |
| `.env.render.production` | Production reference configuration | ✅ Created |
| `backend/init_db.py` | Database initialization script | ✅ Created |
| `backend/config.py` | Application configuration (updated) | ✅ Fixed |

### Local Development Configuration

Located at `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://levelith_user:password@host/levelith

# Security
SECRET_KEY=generated_secure_key
ENVIRONMENT=development
DEBUG=true

# API Configuration
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
LOG_LEVEL=DEBUG
```

### Production Configuration

Reference configuration in `.env.render.production`:

```env
# Database (update with actual Render URL)
DATABASE_URL=postgresql://levelith_user:password@dpg-xxxxx.oregon-postgres.render.com/levelith

# Security
SECRET_KEY=generated_secure_key
ENVIRONMENT=production
DEBUG=false

# API Configuration
CORS_ORIGINS=["https://levelith-frontend.onrender.com","https://levlith.online"]
LOG_LEVEL=INFO
```

:::warning
**Important:** Never commit `.env` files to Git. These files contain sensitive credentials and should remain local or configured via Render dashboard.
:::

---

## Database URL Configuration

### Render PostgreSQL URL Format

The complete database URL from Render should follow this format:

```
postgresql://user:password@dpg-{id}.{region}-postgres.render.com/database
```

### Example URLs

**Internal URL (Recommended):**
```
postgresql://levelith_user:8AwftjchMM2Y4ID1alOEmde3LUyJz5kM@dpg-d4df71ogjchc73duf8og-a.oregon-postgres.render.com/levelith
```

**External URL (For external access only):**
```
postgresql://levelith_user:8AwftjchMM2Y4ID1alOEmde3LUyJz5kM@dpg-d4df71ogjchc73duf8og-a.oregon-postgres.render.com:5432/levelith
```

### Getting Your Database URL

1. Go to https://dashboard.render.com
2. Click on your PostgreSQL database
3. Find **"Internal Database URL"** (NOT External)
4. Copy the complete URL including:
   - `.oregon-postgres.render.com` (or your region)
   - Full hostname
   - Database name

:::tip
**Pro Tip:** Always use the Internal Database URL for services running on Render. It's faster and more secure since it routes through Render's internal network.
:::

### Updating Configuration

If the database URL needs updating:

1. **Local Development:**
   - Edit `backend/.env`
   - Update `DATABASE_URL` with correct value

2. **Production (Render):**
   - Go to Render Dashboard → Your Web Service
   - Navigate to Environment tab
   - Update `DATABASE_URL` environment variable
   - Save changes (triggers auto-redeploy)

---

## Database Initialization

### Initialization Script

The `backend/init_db.py` script handles all database setup:

#### Features

- ✅ **Connection Testing** - Verify database connectivity
- ✅ **Table Creation** - Create all required tables
- ✅ **Safe Execution** - Only creates tables that don't exist
- ✅ **Reset Option** - Drop and recreate (development only)

#### Usage

**Test Database Connection:**
```bash
cd backend
python init_db.py --check
```

**Initialize Database (Create Tables):**
```bash
cd backend
python init_db.py
```

**Reset Database (WARNING: Destroys Data):**
```bash
cd backend
python init_db.py --reset
```

:::danger
**Critical:** The `--reset` flag drops all tables and data. Only use in development environments. Never use in production!
:::

### What Gets Created

When you run `init_db.py`, it creates the following tables:

1. **users** - User accounts and authentication
2. **education_experiences** - Education history
3. **work_experiences** - Employment history
4. **skill_experiences** - Skills and competencies
5. **certification_experiences** - Certifications and credentials
6. **project_experiences** - Portfolio projects
7. **volunteer_experiences** - Volunteer work
8. **publication_experiences** - Publications and articles
9. **award_experiences** - Awards and recognitions
10. **language_experiences** - Language proficiencies

---

## Database Models

### User Model

```python
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Experience Models

All 9 experience types follow a similar structure:

```python
class EducationExperienceDB(Base):
    __tablename__ = "education_experiences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    institution = Column(String, nullable=False)
    degree = Column(String)
    field_of_study = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("UserDB", back_populates="education_experiences")
```

### Relationships

Each user has relationships to all experience types:

```python
# In UserDB model
education_experiences = relationship("EducationExperienceDB", back_populates="user")
work_experiences = relationship("WorkExperienceDB", back_populates="user")
skill_experiences = relationship("SkillExperienceDB", back_populates="user")
# ... and so on for all 9 types
```

---

## Security Configuration

### SECRET_KEY Generation

A cryptographically secure SECRET_KEY has been generated for JWT authentication:

```bash
# Generated using:
openssl rand -hex 32

# Result (example):
SECRET_KEY=08a4ab222554f29ae4a0eb7d00482fa5a79f46f2617ed9cf6453347dc3a8461f
```

### Password Security

- ✅ **Hashing** - Passwords hashed using bcrypt
- ✅ **Salt** - Unique salt per password
- ✅ **Never Stored** - Plain-text passwords never stored
- ✅ **Validation** - Strong password requirements enforced

### Environment Security

1. **Gitignored Files**
   ```gitignore
   .env
   .env.local
   .env.*.local
   backend/.env
   ```

2. **Secure Credentials**
   - All credentials in environment variables
   - Never hardcoded in source code
   - Separate configs for dev/production

3. **Production Settings**
   ```env
   DEBUG=false
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

:::warning
**Security Best Practice:** Rotate your SECRET_KEY periodically and after any potential security incident. This will invalidate all existing JWT tokens.
:::

---

## Testing Database Connection

### Local Testing

1. **Start PostgreSQL** (if running locally)
   ```bash
   # macOS (Homebrew)
   brew services start postgresql

   # Ubuntu/Debian
   sudo systemctl start postgresql

   # Docker
   docker-compose up -d postgres
   ```

2. **Test Connection**
   ```bash
   cd backend
   python init_db.py --check
   ```

   **Expected Output:**
   ```
   ✅ Database connection successful!
   Database: levelith
   Host: localhost
   Version: PostgreSQL 15.x
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

   **Expected Output:**
   ```
   Creating tables...
   ✅ Table 'users' created successfully
   ✅ Table 'education_experiences' created successfully
   ...
   Database initialization complete!
   ```

### Production Testing

1. **Verify Render Database**
   - Go to Render Dashboard
   - Check database status is "Available"

2. **Test from Web Service**
   ```bash
   curl https://your-service.onrender.com/health/details
   ```

   **Expected Response:**
   ```json
   {
     "status": "healthy",
     "database": {
       "status": "connected",
       "database": "levelith",
       "host": "dpg-xxxxx.oregon-postgres.render.com"
     }
   }
   ```

---

## Troubleshooting

<details>
<summary><strong>❌ Error: "Database connection failed"</strong></summary>

**Symptoms:** Cannot connect to database, connection timeout

**Causes:**
1. Incorrect DATABASE_URL
2. Database not running
3. Network/firewall issues
4. Wrong credentials

**Solutions:**
1. Verify DATABASE_URL format:
   ```
   postgresql://user:password@host:port/database
   ```
2. Check database status in Render dashboard
3. Ensure using Internal URL (not External)
4. Verify database and web service in same region
5. Check for typos in username/password

**Verification:**
```bash
# Test connection
python init_db.py --check

# Check environment variable
echo $DATABASE_URL
```
</details>

<details>
<summary><strong>❌ Error: "Module not found" errors</strong></summary>

**Symptoms:** Import errors when running init_db.py

**Cause:** Missing dependencies

**Solution:**
```bash
# Install all dependencies
cd backend
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(sqlalchemy|psycopg2|pydantic)"
```
</details>

<details>
<summary><strong>⚠️ Warning: CORS errors from frontend</strong></summary>

**Symptoms:** Frontend can't connect to API, CORS policy errors

**Cause:** Frontend URL not in CORS_ORIGINS

**Solution:**
1. Update CORS_ORIGINS in environment variables
2. Use JSON array format:
   ```env
   CORS_ORIGINS=["https://your-frontend.com"]
   ```
3. For multiple origins:
   ```env
   CORS_ORIGINS=["https://app1.com","https://app2.com"]
   ```
4. Restart application after changes
</details>

<details>
<summary><strong>ℹ️ Question: Can I run init_db.py multiple times?</strong></summary>

**Answer:** Yes, it's safe to run multiple times. The script only creates tables that don't exist.

**Example:**
```bash
# First run - creates all tables
python init_db.py
# Output: Created 10 tables

# Second run - no changes
python init_db.py
# Output: All tables already exist
```

**Note:** Use `--reset` flag to drop and recreate (development only).
</details>

<details>
<summary><strong>ℹ️ Question: How do I reset the database?</strong></summary>

**Answer:** Use the `--reset` flag (development only):

```bash
# WARNING: This destroys all data!
cd backend
python init_db.py --reset
```

**Confirmation Required:**
```
⚠️  WARNING: This will drop all tables and data!
Are you sure? (yes/no): yes
```

**Never use in production!**
</details>

---

## Best Practices

### ✅ DO

1. **Use Environment Variables**
   ```python
   # ✅ GOOD - Load from environment
   DATABASE_URL = os.getenv("DATABASE_URL")
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Test Before Deploying**
   ```bash
   # ✅ GOOD - Test connection first
   python init_db.py --check
   python init_db.py
   # Then deploy
   ```

3. **Regular Backups**
   ```bash
   # ✅ GOOD - Schedule regular backups
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   ```

### ❌ DON'T

1. **Don't Hardcode Credentials**
   ```python
   # ❌ BAD - Hardcoded database URL
   DATABASE_URL = "postgresql://user:pass@host/db"

   # ✅ GOOD - Use environment variables
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

2. **Don't Commit Secrets**
   ```bash
   # ❌ BAD - Committing .env file
   git add .env
   git commit -m "Add config"

   # ✅ GOOD - Use .env.example
   git add .env.example
   ```

3. **Don't Use --reset in Production**
   ```bash
   # ❌ BAD - Never in production!
   python init_db.py --reset

   # ✅ GOOD - Use migrations for schema changes
   alembic upgrade head
   ```

---

## Next Steps

### For Local Development

1. ✅ Verify database URL in `backend/.env`
2. ✅ Test connection: `python init_db.py --check`
3. ✅ Initialize database: `python init_db.py`
4. ✅ Start backend: `uvicorn main:app --reload`
5. ✅ Test API: `curl http://localhost:8000/health`

### For Production (Render)

1. ✅ Create PostgreSQL database on Render
2. ✅ Copy Internal Database URL
3. ✅ Add environment variables to web service:
   - `DATABASE_URL` - Your database URL
   - `SECRET_KEY` - Generated secure key
   - `ENVIRONMENT=production`
   - `DEBUG=false`
4. ✅ Deploy web service
5. ✅ Verify: `curl https://your-service.onrender.com/health`

### Available API Endpoints

Once database is initialized:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check |
| `/health/details` | GET | Health check with database info |
| `/api/v1/users/` | POST | Create user |
| `/api/v1/users/{id}` | GET | Get user by ID |
| `/api/v1/experiences/` | POST | Create experience |
| `/api/v1/experiences/{id}` | GET | Get experience by ID |

For complete API reference, see [API Documentation](/docs/api/API_DOCUMENTATION.md).

---

## Files Modified/Created

### Created Files

- ✅ `backend/.env` - Local development environment
- ✅ `.env.render.production` - Production environment reference
- ✅ `backend/init_db.py` - Database initialization script
- ✅ `docs/deployment/DATABASE_SETUP_NOTES.md` - This file

### Modified Files

- ✅ `backend/config.py` - Fixed CORS origins validator
- ✅ `backend/database.py` - Database models and relationships
- ✅ `backend/main.py` - Application startup and configuration

---

## Additional Resources

### Internal Documentation

- 📚 [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)
- 🏗️ [Deployment Guide](/docs/deployment/DEPLOYMENT.md)
- 🧪 [API Documentation](/docs/api/API_DOCUMENTATION.md)

### Database Tools

- 🔧 [pgAdmin](https://www.pgadmin.org/) - PostgreSQL GUI
- 💻 [psql](https://www.postgresql.org/docs/current/app-psql.html) - PostgreSQL CLI
- 📊 [DBeaver](https://dbeaver.io/) - Universal database tool

### External Resources

- 🌐 [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- 📖 [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- 🎯 [Render PostgreSQL Guide](https://render.com/docs/databases)

---

## Related Documentation

- **Previous:** [Render Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)
- **Next:** [API Documentation](/docs/api/API_DOCUMENTATION.md)

**Other related documentation:**

- [Environment Configuration](/docs/guides/ENVIRONMENT_SETUP.md)
- [Architecture Overview](/docs/architecture/ARCHITECTURE.md)
- [Security Best Practices](/docs/guides/SECURITY.md)

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
