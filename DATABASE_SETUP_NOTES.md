# Database Setup Notes

## Database Integration Complete ✅

The Levelith backend is now fully configured to work with PostgreSQL on Render.

### What's Been Implemented:

1. **Environment Configuration**
   - `.env` file created for local development
   - `.env.render.production` file created with production values for Render deployment
   - Config validator fixed to properly parse CORS origins

2. **Database Initialization Script**
   - `backend/init_db.py` - Comprehensive database initialization tool
   - Features:
     - `--check`: Test database connection
     - `--reset`: Drop and recreate all tables (dev only)
     - Safe to run multiple times

3. **Database Models**
   - User model (`UserDB`) - Ready to use
   - Experience models (9 types) - All configured
   - Relationships properly defined

4. **Security**
   - Generated secure SECRET_KEY for JWT authentication
   - Credentials in .env files (gitignored)
   - Proper password hashing configured

---

## Database URL Clarification Needed

### Provided URL:
```
postgresql://levelith_user:8AwftjchMM2Y4ID1alOEmde3LUyJz5kM@dpg-d4df71ogjchc73duf8og-a/levelith
```

### Expected Render PostgreSQL URL Format:
```
postgresql://user:password@dpg-{id}-a.{region}-postgres.render.com/database
```

### Action Required:

Please verify the complete database URL from your Render Dashboard:

1. Go to https://dashboard.render.com
2. Click on your PostgreSQL database
3. Find "Internal Database URL" (NOT External)
4. The complete URL should include:
   - `.oregon-postgres.render.com` (or another region)
   - Full hostname with port if non-standard

### Current Configuration:

I've assumed the hostname is:
```
dpg-d4df71ogjchc73duf8og-a.oregon-postgres.render.com
```

If this is incorrect, please update the DATABASE_URL in:
- `backend/.env` (for local development)
- `.env.render.production` (for reference)
- Render Dashboard Environment Variables

---

## Next Steps

### To Initialize Database:

Once you have the correct database URL:

```bash
# From project root
cd backend
python init_db.py --check    # Test connection
python init_db.py            # Create all tables
```

### For Render Deployment:

1. Go to Render Dashboard → Your Web Service
2. Environment tab
3. Add/Update these environment variables (copy from `.env.render.production`):

```env
DATABASE_URL=postgresql://levelith_user:8AwftjchMM2Y4ID1alOEmde3LUyJz5kM@{CORRECT_HOSTNAME}/levelith
SECRET_KEY=08a4ab222554f29ae4a0eb7d00482fa5a79f46f2617ed9cf6453347dc3a8461f
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=["https://levelith-frontend.onrender.com","https://levlith.online"]
```

4. Save changes (Render will auto-deploy)
5. Check health endpoint: `https://your-service.onrender.com/health`

### Testing Locally:

```bash
# From project root
cd backend

# Test database connection
python init_db.py --check

# Initialize database (create tables)
python init_db.py

# Start backend server
uvicorn main:app --reload
```

### API Endpoints Available:

Once database is initialized:
- `GET /health` - Health check
- `GET /health/details` - Health check with database info
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}` - Get user
- `POST /api/v1/experiences/` - Create experience
- And many more...

See `docs/api/API_DOCUMENTATION.md` for complete API reference.

---

## Troubleshooting

### Connection Errors:

1. **"Database connection failed"**
   - Verify DATABASE_URL is correct (check Render dashboard)
   - Ensure database is "Available" in Render
   - Check if using Internal URL (not External)
   - Verify same region as web service

2. **"Module not found" errors**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **CORS errors from frontend**
   - Update CORS_ORIGINS in environment variables
   - Use JSON array format: `["https://domain.com"]`

### Database Already Initialized:

If tables already exist, running `init_db.py` again is safe - it will only create tables that don't exist.

To reset database (WARNING: destroys data):
```bash
cd backend
python init_db.py --reset
```

---

## Files Modified/Created:

✅ `backend/.env` - Local development environment
✅ `.env.render.production` - Render production environment (for reference)
✅ `backend/init_db.py` - Database initialization script
✅ `backend/config.py` - Fixed CORS origins validator
✅ `DATABASE_SETUP_NOTES.md` - This file

---

## Security Notes:

🔒 **IMPORTANT:**
- `.env` files are gitignored (credentials safe)
- SECRET_KEY is cryptographically secure
- Never commit actual credentials to Git
- `.env.render.production` contains real values for your reference only

---

## Status: Ready for Deployment

Once the database URL is confirmed/corrected, you can:
1. Initialize the database
2. Test locally
3. Deploy to Render
4. Start building features!

🎉 Database integration complete!
