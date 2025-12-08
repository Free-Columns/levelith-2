# Backend Connectivity & CRUD Operations Test Guide

**Date:** November 20, 2025
**Purpose:** Manual testing checklist for Users feature with backend API

---

## Prerequisites

### 1. Backend Server Running
```bash
cd backend
uvicorn main:app --reload
```

**Verify:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### 2. Frontend Development Server Running
```bash
cd frontend
npm run dev
```

**Access:** http://localhost:5173/admin/users

---

## Test Checklist

### ✅ 1. Transformation Layer

**Test snake_case → camelCase conversion**

Open browser DevTools Network tab and verify:

**Request to `/api/v1/users`:**
- Query params transformed: `pageSize` → `page_size`
- Request body transformed if POSTing data

**Response from `/api/v1/users`:**
- Backend sends: `is_active`, `created_at`, `last_login`
- Frontend receives: `isActive`, `createdAt`, `lastLoginAt`

**How to verify:**
1. Open Network tab in DevTools
2. Navigate to `/admin/users`
3. Click on the `/users` request
4. Check "Response" tab - should show snake_case
5. Check console logs - should show camelCase

---

### ✅ 2. Users List Page

**URL:** `http://localhost:5173/admin/users`

**Tests:**

- [ ] **Page loads without errors**
  - No console errors
  - No blank page
  - Header displays "User Management"

- [ ] **Data fetching works**
  - Loading spinner appears
  - Users table populates with data
  - Pagination shows correct page numbers

- [ ] **Search functionality**
  - Type in search box
  - Results filter in real-time (or after debounce)
  - Shows "X users" count

- [ ] **Filter dropdowns**
  - Active/Inactive filter works
  - Verified/Unverified filter works
  - Filters can be combined

- [ ] **Table displays correctly**
  - Columns: Username, Email, Status, Verified, Experiences, Joined, Actions
  - Data displays in correct format
  - Dates formatted properly

- [ ] **Pagination controls**
  - Page numbers display
  - Next/Previous buttons work
  - Can change page size (if implemented)
  - Total pages calculated correctly

- [ ] **Row selection (if enabled)**
  - Checkboxes work
  - "Select all" works
  - Selected count displays

---

### ✅ 3. User Detail Page

**URL:** `http://localhost:5173/admin/users/:id`

**Tests:**

- [ ] **Page loads**
  - Click username in table
  - Navigates to `/admin/users/:id`
  - Shows user details

- [ ] **Displays user information**
  - Username and email in header
  - Account status badges (Active/Inactive, Verified/Unverified)
  - Member since date
  - Last login date (if exists)

- [ ] **Profile information (if exists)**
  - Display name
  - Bio
  - Location
  - Website/LinkedIn/GitHub links

- [ ] **Quick stats sidebar**
  - Experience count
  - Account age in days

- [ ] **Breadcrumb navigation**
  - Shows: Admin / Users / {username}
  - Links work correctly

- [ ] **Action buttons**
  - "Edit User" button works
  - "Back to List" button works
  - "View Experiences" button (if implemented)

---

### ✅ 4. CRUD Operations

#### Create User

**Test:**
1. Click "Create New User" button
2. Should navigate to `/admin/users/new` (if form exists)
3. Or open create modal
4. Fill in form:
   - Username: testuser123
   - Email: test@example.com
   - Password: TestPass123!
5. Submit

**Expected:**
- Success message or toast
- Redirects to user list or detail page
- New user appears in list

**API Call:**
```http
POST /api/v1/users
{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "TestPass123!"
}
```

#### Update User

**Test:**
1. Click "Edit" button on a user
2. Should navigate to `/admin/users/:id/edit` or open edit modal
3. Modify email: newemail@example.com
4. Change status: Toggle Active/Inactive
5. Submit

**Expected:**
- Success message
- User list updates immediately (optimistic)
- Backend confirms update

**API Call:**
```http
PATCH /api/v1/users/:id
{
  "email": "newemail@example.com",
  "isActive": false
}
```

#### Delete User (Single)

**Test:**
1. Click "Delete" button on a user
2. Confirmation dialog appears
3. Click "Delete" to confirm

**Expected:**
- Success message
- User removed from list immediately (optimistic)
- If delete fails, user reappears (rollback)

**API Call:**
```http
DELETE /api/v1/users/:id
```

#### Delete Users (Bulk)

**Test:**
1. Select 2-3 users using checkboxes
2. Click "Delete Selected" button
3. Confirmation dialog shows count
4. Click "Delete" to confirm

**Expected:**
- Success message: "Deleted X users"
- Users removed from list
- Selection cleared

**API Call:**
```http
POST /api/v1/users/bulk-delete
{
  "ids": ["id1", "id2", "id3"]
}
```

#### Toggle User Status

**Test:**
1. Click on "Active" or "Inactive" badge in Status column
2. Badge changes immediately
3. API request sends

**Expected:**
- Badge toggles: Active ↔ Inactive
- Background color changes
- Update persists after page refresh

**API Call:**
```http
PATCH /api/v1/users/:id
{
  "isActive": true
}
```

---

### ✅ 5. Error Handling

**Test error scenarios:**

- [ ] **Network error**
  - Stop backend server
  - Try to load `/admin/users`
  - Should show error message: "Error loading users"
  - Should not show blank page

- [ ] **404 - User not found**
  - Navigate to `/admin/users/invalid-id-12345`
  - Should show error: "User not found"
  - "Back to Users" button works

- [ ] **Validation error**
  - Try to create user with invalid email
  - Should show validation error
  - Form should not submit

- [ ] **Duplicate username/email**
  - Try to create user with existing username
  - Should show error: "Username already exists"
  - API returns 409 Conflict

- [ ] **Delete failure**
  - Mock backend failure (if possible)
  - User should reappear in list (rollback)
  - Error message displayed

---

### ✅ 6. Loading States

- [ ] **Initial load**
  - Loading spinner displays
  - Table shows "Loading users..." message

- [ ] **Pagination load**
  - Loading indicator when changing pages
  - Previous data remains visible (or skeleton)

- [ ] **Mutation loading**
  - Create button shows "Creating..."
  - Delete button shows "Deleting..."
  - Buttons disabled during operation

---

### ✅ 7. Empty States

- [ ] **No users found**
  - Search for non-existent user
  - Shows: "No users found"
  - Shows: "Try adjusting your search or filters"

- [ ] **No data at all**
  - If database is empty
  - Shows helpful message
  - Suggests creating first user

---

### ✅ 8. Cache & Optimistic Updates

**Test React Query caching:**

- [ ] **Navigate away and back**
  1. Load `/admin/users`
  2. Navigate to `/admin/experiences`
  3. Navigate back to `/admin/users`
  4. Data loads instantly from cache (stale-while-revalidate)
  5. Background refetch occurs

- [ ] **Optimistic update**
  1. Toggle user status Active → Inactive
  2. UI updates immediately (before API responds)
  3. If API fails, reverts to Active (rollback)

- [ ] **Cache invalidation**
  1. Create new user
  2. User list refetches automatically
  3. New user appears in list

---

### ✅ 9. Accessibility

- [ ] **Keyboard navigation**
  - Tab through table
  - Can navigate with keyboard only
  - Focus indicators visible

- [ ] **Screen reader**
  - Button labels clear
  - Table headers announced
  - Status changes announced

- [ ] **ARIA labels**
  - Checkboxes have labels
  - Buttons have descriptions

---

### ✅ 10. Performance

- [ ] **Large dataset (100+ users)**
  - Seed database: `POST /api/v1/users/seed?user_count=100`
  - Table renders smoothly
  - Pagination works correctly
  - No lag when scrolling

- [ ] **Search performance**
  - Type in search box
  - Debounced (doesn't fire on every keystroke)
  - Results update within 1 second

---

## Common Issues & Solutions

### Issue: "CORS Error"
**Solution:**
```bash
# In backend/.env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8000"]
```
Restart backend server.

### Issue: "Field names don't match"
**Solution:**
Check transformation layer is working:
```javascript
// In browser console
console.log(user)
// Should show: { userName: 'john', isActive: true, createdAt: '...' }
// NOT: { user_name: 'john', is_active: true, created_at: '...' }
```

### Issue: "Pagination not working"
**Solution:**
Check backend response format:
```json
// Backend should return:
{
  "items": [...],  // or "data": [...]
  "total": 100,
  "page": 1,
  "page_size": 50,
  "total_pages": 2
}
```

### Issue: "Mutations not updating cache"
**Solution:**
Check `userKeys` query key factory:
```typescript
// All queries should use userKeys
useQuery({ queryKey: userKeys.list(params) })
// Mutations should invalidate
queryClient.invalidateQueries({ queryKey: userKeys.lists() })
```

---

## Backend API Endpoints to Test

```bash
# List users
curl "http://localhost:8000/api/v1/users?skip=0&limit=50"

# Get single user
curl "http://localhost:8000/api/v1/users/{user_id}"

# Create user
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123!"}'

# Update user
curl -X PATCH "http://localhost:8000/api/v1/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{"is_active":false}'

# Delete user
curl -X DELETE "http://localhost:8000/api/v1/users/{user_id}"

# Seed database
curl -X POST "http://localhost:8000/api/v1/users/seed?user_count=50"
```

---

## Test Results

**Date Tested:** _____________

**Tester:** _____________

**Backend Status:** ☐ Running ☐ Not Running

**Frontend Status:** ☐ Running ☐ Not Running

**Overall Result:** ☐ PASS ☐ FAIL

**Issues Found:**
1. _______________________________
2. _______________________________
3. _______________________________

**Notes:**
_________________________________
_________________________________
_________________________________

---

## Next Steps After Testing

- [ ] Document any bugs found
- [ ] Create GitHub issues for bugs
- [ ] Update documentation if needed
- [ ] Add missing features to backlog
- [ ] Deploy to staging environment
- [ ] Run E2E tests with Playwright

---

**Conclusion:** Manual testing completed. Ready for automated E2E tests and staging deployment.
