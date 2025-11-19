# Levelith Backend API Documentation

**Version:** 1.0
**Last Updated:** 2025-01-17
**Status:** Design Document (Implementation Pending)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
   - [Authentication Endpoints](#authentication-endpoints)
   - [User Endpoints](#user-endpoints)
   - [Experience Endpoints](#experience-endpoints)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Pagination](#pagination)
9. [Filtering and Search](#filtering-and-search)
10. [Security](#security)
11. [Examples](#examples)
12. [Testing](#testing)

---

## Overview

The Levelith Backend API provides RESTful endpoints for managing users and their professional experiences. The API follows REST principles, uses JSON for data exchange, and implements JWT-based authentication.

### Base URL

```
Production:  https://levlith.online/api/v1
Development: http://localhost:8000/api/v1
```

### Core Features

- **User Management**: Registration, authentication, profile management
- **Experience Tracking**: CRUD operations for 9 experience types
- **NAICS Integration**: Industry classification for all experiences
- **Social Features**: User discovery, experience sharing
- **Gamification**: Points, achievements, levels (future)

### Design Principles

- **RESTful**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **JSON**: All request/response bodies use JSON format
- **Stateless**: JWT tokens for authentication
- **Versioned**: API version in URL path (`/api/v1/`)
- **Documented**: OpenAPI/Swagger documentation available

---

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │  ← HTTP Endpoints
│  Controllers handle requests/responses
├─────────────────────────────────────┤
│         Service Layer               │  ← Business Logic
│  UserService, ExperienceService     │
├─────────────────────────────────────┤
│      Repository Layer               │  ← Data Access
│  UserRepository, ExperienceRepository│
├─────────────────────────────────────┤
│         Data Store                  │  ← Persistence
│  PostgreSQL (future), In-memory (current)
└─────────────────────────────────────┘
```

### Technology Stack

- **Framework**: FastAPI (Python 3.11+)
- **Authentication**: JWT tokens
- **Database**: PostgreSQL (planned), In-memory (current)
- **Caching**: Redis (planned)
- **Documentation**: OpenAPI/Swagger (auto-generated)
- **Hosting**: Render.com

### Implemented Components

✅ **Domain Models** (`backend/models/`)
- `User`: User account and profile model
- `Experience`: Base experience model
- 9 Experience subtypes (Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill)

✅ **Repository Layer** (`backend/repositories/`)
- `UserRepository`: User data access operations
- `ExperienceRepository`: Experience data access operations

✅ **Service Layer** (`backend/services/`)
- `UserService`: User business logic and orchestration
- `ExperienceService`: Experience business logic and NAICS validation

🚧 **API Layer** (`backend/api/`) - **TO BE IMPLEMENTED**
- Controllers for all endpoints
- Request/response schemas
- Error handling middleware
- Authentication middleware

---

## Authentication

### JWT Token-Based Authentication

The API uses JSON Web Tokens (JWT) for stateless authentication.

#### Authentication Flow

```
1. User sends credentials to /auth/login
2. Server validates credentials
3. Server generates JWT token (valid for 24 hours)
4. Client stores token
5. Client includes token in Authorization header for subsequent requests
6. Server validates token on each request
```

#### Token Format

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user_id": "user_123abc"
}
```

#### Using Tokens

Include the token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Token Expiration

- **Access tokens**: Valid for 24 hours
- **Refresh tokens**: Valid for 30 days (future implementation)
- Expired tokens return `401 Unauthorized`

---

## API Endpoints

### Authentication Endpoints

#### 1. Register New User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "profile_data": {
    "display_name": "John Doe",
    "bio": "Software engineer and educator",
    "location": "San Francisco, CA"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "user_123abc",
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "is_verified": false,
  "profile_data": {
    "display_name": "John Doe",
    "bio": "Software engineer and educator",
    "location": "San Francisco, CA"
  },
  "created_at": "2025-01-17T10:30:00Z",
  "updated_at": "2025-01-17T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request`: Invalid data (username taken, weak password)
- `422 Unprocessable Entity`: Validation errors

**Business Rules:**
- Username must be 3-50 characters, alphanumeric + underscores/hyphens
- Email must be valid format and unique
- Password must be at least 8 characters
- New users start as unverified but active

---

#### 2. Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "user_123abc",
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials or inactive user
- `422 Unprocessable Entity`: Validation errors

**Business Rules:**
- User must exist with given email
- User must be active (is_active = true)
- Password must match stored hash
- Last login timestamp is updated

---

#### 3. Logout

**POST** `/auth/logout`

Invalidate the current JWT token.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

**Note:** In a stateless JWT system, logout is typically handled client-side by deleting the token. Server-side blacklisting can be implemented with Redis.

---

#### 4. Refresh Token

**POST** `/auth/refresh`

Get a new access token using a refresh token (future implementation).

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

### User Endpoints

#### 5. Get Current User

**GET** `/users/me`

Get the authenticated user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "user_123abc",
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "is_verified": true,
  "profile_data": {
    "display_name": "John Doe",
    "bio": "Software engineer and educator",
    "location": "San Francisco, CA",
    "website": "https://johndoe.com",
    "avatar_url": "https://example.com/avatars/johndoe.jpg"
  },
  "experiences": ["exp_abc123", "exp_def456"],
  "created_at": "2025-01-17T10:30:00Z",
  "updated_at": "2025-01-17T10:35:00Z",
  "last_login": "2025-01-17T15:20:00Z"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token

---

#### 6. Get User by ID

**GET** `/users/{user_id}`

Get a specific user's public profile.

**Parameters:**
- `user_id` (path): User's unique identifier

**Response (200 OK):**
```json
{
  "id": "user_123abc",
  "username": "johndoe",
  "profile_data": {
    "display_name": "John Doe",
    "bio": "Software engineer and educator",
    "location": "San Francisco, CA",
    "website": "https://johndoe.com"
  },
  "created_at": "2025-01-17T10:30:00Z"
}
```

**Errors:**
- `404 Not Found`: User doesn't exist

**Note:** This endpoint returns only public information (no email, password_hash, or sensitive data).

---

#### 7. Update User Profile

**PUT** `/users/me`

Update the authenticated user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "profile_data": {
    "display_name": "John Doe Updated",
    "bio": "Senior software engineer",
    "location": "New York, NY",
    "website": "https://johndoe.dev"
  }
}
```

**Response (200 OK):**
```json
{
  "id": "user_123abc",
  "username": "johndoe",
  "email": "john@example.com",
  "profile_data": {
    "display_name": "John Doe Updated",
    "bio": "Senior software engineer",
    "location": "New York, NY",
    "website": "https://johndoe.dev"
  },
  "updated_at": "2025-01-17T16:45:00Z"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `422 Unprocessable Entity`: Validation errors

---

#### 8. Change Password

**POST** `/users/me/password`

Change the authenticated user's password.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewSecurePass456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password updated successfully"
}
```

**Errors:**
- `401 Unauthorized`: Invalid token or incorrect old password
- `400 Bad Request`: New password doesn't meet requirements

**Business Rules:**
- Old password must be correct
- New password must be at least 8 characters
- New password must be different from old password

---

#### 9. Delete User Account

**DELETE** `/users/me`

Permanently delete the authenticated user's account.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "password": "CurrentPassword123!",
  "confirm": true
}
```

**Response (200 OK):**
```json
{
  "message": "Account deleted successfully"
}
```

**Errors:**
- `401 Unauthorized`: Invalid token or incorrect password
- `400 Bad Request`: Missing confirmation

**Warning:** This action is irreversible and deletes all user data.

---

#### 10. List Users

**GET** `/users`

List all users with optional filtering and pagination.

**Query Parameters:**
- `active_only` (boolean): Filter for active users only
- `verified_only` (boolean): Filter for verified users only
- `search` (string): Search by username
- `limit` (integer): Max number of results (default: 20, max: 100)
- `offset` (integer): Number of results to skip (default: 0)

**Example Request:**
```
GET /users?active_only=true&limit=10&offset=0
```

**Response (200 OK):**
```json
{
  "total": 150,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "id": "user_123abc",
      "username": "johndoe",
      "profile_data": {
        "display_name": "John Doe"
      }
    },
    {
      "id": "user_456def",
      "username": "janedoe",
      "profile_data": {
        "display_name": "Jane Doe"
      }
    }
  ]
}
```

---

### Experience Endpoints

#### 11. Create Experience

**POST** `/experiences`

Create a new experience for the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body (Certificate Example):**
```json
{
  "experience_type": "certificate",
  "title": "AWS Certified Solutions Architect",
  "description": "Professional cloud architecture certification",
  "naics_code": "541511",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": null,
  "organization": "Amazon Web Services",
  "location": "Online",
  "skills_gained": ["AWS", "Cloud Architecture", "DevOps"],
  "achievements": ["Passed exam with 850/1000 score"],
  "metadata": {
    "credential_id": "AWS-12345",
    "verification_url": "https://aws.amazon.com/verify/12345"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "exp_abc123",
  "user_id": "user_123abc",
  "category": "education",
  "experience_type": "certificate",
  "title": "AWS Certified Solutions Architect",
  "description": "Professional cloud architecture certification",
  "naics_code": "541511",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": null,
  "organization": "Amazon Web Services",
  "location": "Online",
  "skills_gained": ["AWS", "Cloud Architecture", "DevOps"],
  "achievements": ["Passed exam with 850/1000 score"],
  "metadata": {
    "credential_id": "AWS-12345",
    "verification_url": "https://aws.amazon.com/verify/12345"
  },
  "created_at": "2025-01-17T10:30:00Z",
  "updated_at": "2025-01-17T10:30:00Z"
}
```

**Experience Types:**

The `experience_type` field must be one of:

**Education:**
- `certificate`: Short-term certifications and credentials
- `degree`: Formal academic degrees
- `course`: Individual courses and workshops

**Workplace:**
- `gig`: Short-term contract work and freelance projects
- `part_time`: Regular part-time employment
- `full_time`: Primary career positions

**Skills:**
- `soft_skill`: Interpersonal abilities and leadership
- `hard_skill`: Technical abilities and competencies
- `native_skill`: Natural talents and language fluencies

**NAICS Code Validation:**
- Must be a valid 6-digit NAICS code
- If invalid or missing, defaults to `"123456"` (GENERAL classification)
- See [NAICS Code Reference](#naics-code-reference) for common codes

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `400 Bad Request`: Invalid experience_type or validation errors
- `422 Unprocessable Entity`: Validation errors

---

#### 12. Get Experience by ID

**GET** `/experiences/{experience_id}`

Get a specific experience by ID.

**Parameters:**
- `experience_id` (path): Experience unique identifier

**Response (200 OK):**
```json
{
  "id": "exp_abc123",
  "user_id": "user_123abc",
  "category": "education",
  "experience_type": "certificate",
  "title": "AWS Certified Solutions Architect",
  "description": "Professional cloud architecture certification",
  "naics_code": "541511",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": null,
  "organization": "Amazon Web Services",
  "location": "Online",
  "skills_gained": ["AWS", "Cloud Architecture", "DevOps"],
  "achievements": ["Passed exam with 850/1000 score"],
  "metadata": {},
  "created_at": "2025-01-17T10:30:00Z",
  "updated_at": "2025-01-17T10:30:00Z"
}
```

**Errors:**
- `404 Not Found`: Experience doesn't exist

---

#### 13. Get User Experiences

**GET** `/users/{user_id}/experiences`

Get all experiences for a specific user.

**Parameters:**
- `user_id` (path): User's unique identifier

**Query Parameters:**
- `category` (string): Filter by category (education, workplace, skills)
- `experience_type` (string): Filter by specific type
- `active_only` (boolean): Only active (ongoing) experiences
- `limit` (integer): Max results (default: 20)
- `offset` (integer): Skip results (default: 0)

**Example Request:**
```
GET /users/user_123abc/experiences?category=education&limit=10
```

**Response (200 OK):**
```json
{
  "user_id": "user_123abc",
  "total": 5,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "id": "exp_abc123",
      "category": "education",
      "experience_type": "certificate",
      "title": "AWS Certified Solutions Architect",
      "start_date": "2024-01-15T00:00:00Z",
      "end_date": null
    },
    {
      "id": "exp_def456",
      "category": "education",
      "experience_type": "degree",
      "title": "Bachelor of Science in Computer Science",
      "start_date": "2020-09-01T00:00:00Z",
      "end_date": "2024-05-15T00:00:00Z"
    }
  ]
}
```

---

#### 14. Update Experience

**PUT** `/experiences/{experience_id}`

Update an existing experience.

**Headers:**
```
Authorization: Bearer <token>
```

**Parameters:**
- `experience_id` (path): Experience unique identifier

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "end_date": "2025-01-17T00:00:00Z",
  "skills_gained": ["Python", "Django", "PostgreSQL"]
}
```

**Response (200 OK):**
```json
{
  "id": "exp_abc123",
  "user_id": "user_123abc",
  "title": "Updated Title",
  "description": "Updated description",
  "end_date": "2025-01-17T00:00:00Z",
  "skills_gained": ["Python", "Django", "PostgreSQL"],
  "updated_at": "2025-01-17T16:50:00Z"
}
```

**Fields that CANNOT be updated:**
- `id`
- `user_id`
- `category`
- `experience_type`

**Errors:**
- `401 Unauthorized`: Invalid token or not the owner
- `404 Not Found`: Experience doesn't exist
- `403 Forbidden`: User is not the owner of this experience

---

#### 15. Delete Experience

**DELETE** `/experiences/{experience_id}`

Delete an experience.

**Headers:**
```
Authorization: Bearer <token>
```

**Parameters:**
- `experience_id` (path): Experience unique identifier

**Response (200 OK):**
```json
{
  "message": "Experience deleted successfully"
}
```

**Errors:**
- `401 Unauthorized`: Invalid token or not the owner
- `404 Not Found`: Experience doesn't exist
- `403 Forbidden`: User is not the owner of this experience

---

#### 16. Search Experiences

**GET** `/experiences/search`

Search experiences by title, skills, or NAICS code.

**Query Parameters:**
- `q` (string): Search query (searches title and skills)
- `naics_code` (string): Filter by NAICS code
- `user_id` (string): Filter by user
- `category` (string): Filter by category
- `experience_type` (string): Filter by type
- `limit` (integer): Max results (default: 20)
- `offset` (integer): Skip results (default: 0)

**Example Request:**
```
GET /experiences/search?q=python&category=workplace&limit=10
```

**Response (200 OK):**
```json
{
  "query": "python",
  "total": 25,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "id": "exp_abc123",
      "user_id": "user_123abc",
      "category": "workplace",
      "experience_type": "full_time",
      "title": "Python Developer",
      "skills_gained": ["Python", "Django", "REST APIs"]
    }
  ]
}
```

---

## Data Models

### User Model

```python
{
  "id": str,                    # Unique user identifier
  "username": str,              # Unique username (3-50 chars)
  "email": str,                 # Unique email address
  "password_hash": str,         # Hashed password (never returned in API)
  "is_active": bool,            # Account active status
  "is_verified": bool,          # Email verification status
  "profile_data": {             # Flexible profile information
    "display_name": str,        # Public display name
    "bio": str,                 # User bio/description
    "location": str,            # Location
    "website": str,             # Personal website
    "avatar_url": str           # Profile picture URL
  },
  "experiences": [str],         # Array of experience IDs
  "created_at": datetime,       # Account creation timestamp
  "updated_at": datetime,       # Last update timestamp
  "last_login": datetime        # Last login timestamp
}
```

### Experience Model

```python
{
  "id": str,                    # Unique experience identifier
  "user_id": str,               # ID of user who owns this experience
  "category": str,              # "education", "workplace", or "skills"
  "experience_type": str,       # Specific type (see below)
  "title": str,                 # Experience title
  "description": str,           # Detailed description
  "naics_code": str,            # REQUIRED: 6-digit NAICS code
  "start_date": datetime,       # When experience started
  "end_date": datetime | null,  # When it ended (null if ongoing)
  "organization": str | null,   # Associated organization
  "location": str | null,       # Geographic location
  "skills_gained": [str],       # Array of skills acquired
  "achievements": [str],        # Array of achievements
  "metadata": dict,             # Additional type-specific data
  "created_at": datetime,       # Record creation timestamp
  "updated_at": datetime        # Last update timestamp
}
```

### Experience Types

**Education (category: "education"):**
- `certificate`: Short-term certifications and credentials
- `degree`: Formal academic degrees
- `course`: Individual courses and workshops

**Workplace (category: "workplace"):**
- `gig`: Short-term contract work and freelance
- `part_time`: Regular part-time employment
- `full_time`: Primary career positions

**Skills (category: "skills"):**
- `soft_skill`: Interpersonal abilities and leadership
- `hard_skill`: Technical abilities and competencies
- `native_skill`: Natural talents and language fluencies

---

## Error Handling

### Error Response Format

All errors follow a consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "username",
      "reason": "Username already taken"
    }
  }
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | User doesn't have permission |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error (should be rare) |

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_CREDENTIALS` | Email or password is incorrect |
| `USER_NOT_FOUND` | User doesn't exist |
| `EXPERIENCE_NOT_FOUND` | Experience doesn't exist |
| `DUPLICATE_USERNAME` | Username already taken |
| `DUPLICATE_EMAIL` | Email already registered |
| `INVALID_TOKEN` | JWT token is invalid or expired |
| `WEAK_PASSWORD` | Password doesn't meet requirements |
| `INVALID_NAICS_CODE` | NAICS code format is invalid |
| `UNAUTHORIZED_ACCESS` | User doesn't own this resource |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

---

## Rate Limiting

### Rate Limit Rules

| Endpoint Pattern | Limit | Window |
|------------------|-------|--------|
| `/auth/login` | 5 requests | 15 minutes |
| `/auth/register` | 3 requests | 1 hour |
| `/users/*` | 100 requests | 1 hour |
| `/experiences/*` | 200 requests | 1 hour |
| All other endpoints | 1000 requests | 1 hour |

### Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642435200
```

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": {
      "retry_after": 3600
    }
  }
}
```

---

## Pagination

### Standard Pagination

List endpoints use offset-based pagination:

**Query Parameters:**
- `limit`: Maximum number of results (default: 20, max: 100)
- `offset`: Number of results to skip (default: 0)

**Example:**
```
GET /experiences?limit=10&offset=20
```

**Response:**
```json
{
  "total": 150,
  "limit": 10,
  "offset": 20,
  "results": [...]
}
```

### Pagination Metadata

All paginated responses include:
- `total`: Total number of results
- `limit`: Number of results per page
- `offset`: Number of results skipped
- `results`: Array of result objects

---

## Filtering and Search

### Query Parameters

Common filtering parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query |
| `category` | string | Filter by category |
| `experience_type` | string | Filter by type |
| `naics_code` | string | Filter by NAICS code |
| `active_only` | boolean | Only active/ongoing items |
| `verified_only` | boolean | Only verified users |
| `user_id` | string | Filter by user |

### Search Behavior

- **Case-insensitive**: Searches ignore case
- **Partial matching**: Searches use substring matching
- **Multiple fields**: Searches can span title, description, and skills

---

## Security

### Security Measures

1. **Password Hashing**
   - Passwords are hashed using PBKDF2-HMAC-SHA256
   - Production will use bcrypt or argon2
   - Never store or return plain text passwords

2. **JWT Tokens**
   - Tokens are signed with secret key
   - Tokens include expiration timestamp
   - Tokens cannot be tampered with

3. **Input Validation**
   - All user input is validated and sanitized
   - Type checking and format validation
   - SQL injection prevention (parameterized queries)

4. **HTTPS Only**
   - Production API requires HTTPS
   - Tokens and credentials encrypted in transit

5. **CORS**
   - Cross-Origin Resource Sharing configured
   - Only allows trusted domains

6. **Rate Limiting**
   - Prevents brute force attacks
   - Protects against DoS

### Security Best Practices

**For Clients:**
- Store tokens securely (HTTPOnly cookies or secure storage)
- Never expose tokens in URLs
- Implement token refresh flow
- Clear tokens on logout
- Use HTTPS for all requests

**For Server:**
- Regular security audits (Bandit, Safety)
- Dependency updates
- Environment variables for secrets
- Audit logging
- Regular backups

---

## NAICS Code Reference

Common NAICS codes for experiences:

| Code | Industry/Classification |
|------|------------------------|
| `123456` | GENERAL (fallback code) |
| `541511` | Custom Computer Programming Services |
| `541512` | Computer Systems Design Services |
| `541513` | Computer Facilities Management |
| `541519` | Other Computer Related Services |
| `541611` | Administrative Management Consulting |
| `541618` | Other Management Consulting Services |
| `611310` | Colleges, Universities, and Professional Schools |
| `611420` | Computer Training |
| `611430` | Professional and Management Development Training |
| `611710` | Educational Support Services |

**Full NAICS Code Database:** https://www.census.gov/naics/

---

## Examples

### Complete User Registration and Login Flow

```bash
# 1. Register new user
curl -X POST https://levlith.online/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "profile_data": {
      "display_name": "John Doe",
      "bio": "Software engineer"
    }
  }'

# Response:
# {
#   "id": "user_123abc",
#   "username": "johndoe",
#   "email": "john@example.com",
#   ...
# }

# 2. Login
curl -X POST https://levlith.online/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'

# Response:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "expires_in": 86400,
#   "user": { ... }
# }

# 3. Get current user (with token)
curl -X GET https://levlith.online/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Response:
# {
#   "id": "user_123abc",
#   "username": "johndoe",
#   "email": "john@example.com",
#   ...
# }
```

### Create Different Experience Types

```bash
# Create Certificate
curl -X POST https://levlith.online/api/v1/experiences \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "experience_type": "certificate",
    "title": "AWS Certified Solutions Architect",
    "description": "Cloud architecture certification",
    "naics_code": "541511",
    "start_date": "2024-01-15T00:00:00Z",
    "organization": "Amazon Web Services",
    "skills_gained": ["AWS", "Cloud Architecture"]
  }'

# Create Full-Time Job
curl -X POST https://levlith.online/api/v1/experiences \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "experience_type": "full_time",
    "title": "Senior Software Engineer",
    "description": "Full-stack development lead",
    "naics_code": "541511",
    "start_date": "2022-01-01T00:00:00Z",
    "end_date": null,
    "organization": "Tech Corp",
    "location": "San Francisco, CA",
    "skills_gained": ["Python", "React", "PostgreSQL"]
  }'

# Create Hard Skill
curl -X POST https://levlith.online/api/v1/experiences \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "experience_type": "hard_skill",
    "title": "Python Programming",
    "description": "5 years of professional Python development",
    "naics_code": "541511",
    "start_date": "2019-01-01T00:00:00Z",
    "skills_gained": ["Python", "Django", "FastAPI", "Testing"]
  }'
```

### Search and Filter

```bash
# Search experiences by keyword
curl -X GET "https://levlith.online/api/v1/experiences/search?q=python&limit=10"

# Filter by category
curl -X GET "https://levlith.online/api/v1/users/user_123abc/experiences?category=education"

# Get active experiences only
curl -X GET "https://levlith.online/api/v1/users/user_123abc/experiences?active_only=true"

# Complex filter
curl -X GET "https://levlith.online/api/v1/experiences/search?naics_code=541511&category=workplace&limit=20"
```

---

## Testing

### Test Coverage Requirements

According to `MANIFEST.md`:
- **Minimum test coverage**: 80%
- **Test-first development**: Tests must be written before implementation
- **Test types**: Unit, integration, and end-to-end tests

### Test Structure

```
tests/
├── unit/
│   ├── test_user_model.py
│   ├── test_experience_model.py
│   ├── test_user_repository.py
│   ├── test_experience_repository.py
│   ├── test_user_service.py
│   └── test_experience_service.py
├── integration/
│   ├── test_user_api.py
│   └── test_experience_api.py
└── e2e/
    └── test_complete_user_flow.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/unit/test_user_service.py

# Run tests matching pattern
pytest -k "test_create_user"
```

### Manual API Testing

Use tools like:
- **curl**: Command-line testing (see examples above)
- **Postman**: GUI-based API testing
- **HTTPie**: User-friendly command-line tool
- **Swagger UI**: Interactive API documentation (when implemented)

**Swagger UI will be available at:**
```
https://levlith.online/docs
```

---

### Statistics Endpoint

#### GET `/stats`

Get aggregated statistics for admin dashboard analytics.

**Purpose**: Provides comprehensive statistics about users, experiences, skills, and geographic distribution for administrative dashboards and analytics.

**Headers**: None required (public endpoint, can be restricted later)

**Response (200 OK):**
```json
{
  "users": {
    "total": 100,
    "active": 85,
    "verified": 60,
    "inactive": 15,
    "growth": [
      {"month": "Jan", "users": 10},
      {"month": "Feb", "users": 25},
      {"month": "Mar", "users": 42}
    ],
    "activity": [
      {"date": "Nov 18", "logins": 42},
      {"date": "Nov 19", "logins": 38}
    ]
  },
  "experiences": {
    "total": 450,
    "byType": {
      "full_time": 120,
      "degree": 80,
      "hard_skill": 100,
      "certificate": 50
    },
    "byCategory": {
      "education": 150,
      "workplace": 180,
      "skills": 120
    },
    "byIndustry": {
      "technology": 200,
      "education": 100,
      "healthcare": 50,
      "finance": 40,
      "general": 60
    }
  },
  "skills": {
    "top": [
      {"skill": "Python", "count": 45},
      {"skill": "JavaScript", "count": 38},
      {"skill": "Communication", "count": 32}
    ],
    "total": 120
  },
  "geography": {
    "locations": [
      {"location": "San Francisco, CA", "count": 25},
      {"location": "New York, NY", "count": 20},
      {"location": "Austin, TX", "count": 15}
    ]
  }
}
```

**Response Fields:**

**users**:
- `total` (integer): Total number of registered users
- `active` (integer): Number of active users (is_active = true)
- `verified` (integer): Number of verified users (is_verified = true)
- `inactive` (integer): Number of inactive users
- `growth` (array): User growth over last 12 months
  - `month` (string): Month abbreviation (Jan, Feb, etc.)
  - `users` (integer): Cumulative user count at end of month
- `activity` (array): User login activity for last 30 days
  - `date` (string): Date string (Mon DD format)
  - `logins` (integer): Number of logins on that date

**experiences**:
- `total` (integer): Total number of experiences
- `byType` (object): Count of experiences by type
  - Keys: Experience type names (full_time, degree, hard_skill, etc.)
  - Values: Count of experiences of that type
- `byCategory` (object): Count of experiences by category
  - Keys: Category names (education, workplace, skills)
  - Values: Count of experiences in that category
- `byIndustry` (object): Count of experiences by industry (NAICS-based)
  - Keys: Industry names (technology, education, healthcare, etc.)
  - Values: Count of experiences in that industry

**skills**:
- `top` (array): Top trending skills (currently returns empty array)
  - `skill` (string): Skill name
  - `count` (integer): Number of users with this skill
- `total` (integer): Total unique skills (currently 0)

**geography**:
- `locations` (array): Top locations by user count (max 8)
  - `location` (string): Location string from user profile
  - `count` (integer): Number of users at that location

**Performance:**
- Response time: < 5 seconds for databases with up to 10,000 users
- Caching recommended for production environments

**Business Rules:**
- All counts are based on current database state
- Growth data shows last 12 months (month by month)
- Activity data shows last 30 days (day by day)
- Industry mapping based on NAICS code classification
- Empty database returns zeros/empty arrays (not errors)

**Usage Example:**
```bash
# Get statistics
curl http://localhost:8000/api/v1/stats

# Use in admin dashboard
fetch('https://levlith.online/api/v1/stats')
  .then(res => res.json())
  .then(stats => {
    console.log(`Total users: ${stats.users.total}`);
    console.log(`Active users: ${stats.users.active}`);
  });
```

**Notes:**
- User activity (logins) is currently estimated; implement login tracking for accurate data
- Skills data requires proper skill extraction from experiences
- Geographic data depends on users having `profile_data.location` set
- Consider adding caching (Redis) for production to reduce database load

---

## Implementation Status

### ✅ Completed

- Domain models (User, Experience, 9 subtypes)
- Repository layer (UserRepository, ExperienceRepository)
- Service layer (UserService, ExperienceService)
- Comprehensive documentation (this file)

### 🚧 In Progress

- API layer (FastAPI controllers)
- Authentication middleware
- Request/response schemas
- Error handling middleware

### 📋 Planned

- Database integration (PostgreSQL)
- Redis caching for sessions
- Refresh token flow
- Email verification workflow
- Profile picture uploads
- Social features (followers, connections)
- Gamification (points, achievements)
- WebSocket support for real-time features

---

## Versioning

The API follows semantic versioning:
- **v1.0**: Current version (in development)
- Future versions will be available at `/api/v2/`, etc.
- Breaking changes will increment the major version
- Backward-compatible changes will increment the minor version

---

## Support

For API issues or questions:
- **Documentation**: This file and inline code docstrings
- **GitHub Issues**: https://github.com/Free-Columns/levelith-2/issues
- **Email**: [contact information]

---

**End of API Documentation**

*This document will be updated as the API is implemented and evolves.*
