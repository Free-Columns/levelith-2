// ============================================================================
// AdminDashboardRefactorv2: MIGRATE - Phase 2 (Users Feature)
// ============================================================================
// What: Migrate Users.jsx → features/users/ folder structure with TypeScript
// Why: Feature-based organization, React Query integration, type safety
// Risk: HIGH - core functionality, affects user management
// Phase: 2 (Users Feature)
// Complexity: High (242 lines, complex state management)
// Depends: Phase 1 (React Query setup, base components)
//
// CURRENT PROBLEMS:
// 1. Manual state management (useState for users, loading, errors)
// 2. Manual API calls via useDataSource hook
// 3. No caching - refetches on every mount
// 4. No optimistic updates
// 5. Inline styles instead of Tailwind
// 6. No TypeScript type safety
// 7. Form validation is manual
// 8. Modal component not accessible
//
// NEW STRUCTURE (Phase 2):
// features/users/
//   ├── Users.tsx                    (Main page component)
//   ├── api/
//   │   ├── users.queries.ts         (React Query hooks: useUsers, useUser)
//   │   └── users.mutations.ts       (useMutations: useCreateUser, useUpdateUser, useDeleteUser, useSeedUsers)
//   ├── components/
//   │   ├── UsersTable.tsx           (TanStack Table with sorting/filtering)
//   │   ├── UserForm.tsx             (React Hook Form + Zod validation)
//   │   ├── UserFilters.tsx          (Search + filter dropdowns)
//   │   ├── UserStats.tsx            (Stats cards)
//   │   └── UserActions.tsx          (Action dropdown menu)
//   ├── schemas/
//   │   └── user.schema.ts           (Zod validation schemas)
//   ├── types/
//   │   └── user.types.ts            (TypeScript interfaces)
//   └── hooks/
//       └── useUsers.ts              (Custom hook combining queries)
//
// MIGRATION TASKS (25 total - see ADMIN_DASHBOARD_REFACTOR_V2.md Phase 2):
// ☐ Create user.types.ts with User, CreateUserInput, UpdateUserInput interfaces
// ☐ Create user.schema.ts with Zod schemas for validation
// ☐ Create users.queries.ts with useUsers, useUser hooks
// ☐ Create users.mutations.ts with useCreateUser, useUpdateUser, useDeleteUser
// ☐ Build UsersTable with TanStack Table (search, filter, pagination, sorting)
// ☐ Build UserForm with React Hook Form + Zod
// ☐ Build UserFilters component
// ☐ Build CreateUserDialog using shadcn/ui Dialog
// ☐ Build EditUserDialog
// ☐ Build DeleteUserDialog with confirmation
// ☐ Add loading states (skeleton)
// ☐ Add error handling (toast notifications)
// ☐ Add optimistic updates
// ☐ Migrate inline styles to Tailwind CSS
// ☐ Test all CRUD operations
//
// REPLACE THIS ENTIRE FILE after migration complete
// ============================================================================

/**
 * Users Page - Comprehensive CRUD Interface
 *
 * Features:
 * - User list with search and filtering
 * - Create new user form
 * - Edit existing user
 * - Delete user with confirmation
 * - Statistics and analytics
 */

import React, { useState, useEffect } from "react";
// AdminDashboardRefactorv2: REPLACE - Remove useDataSource, use React Query hooks
// OLD: const { getUsers, createUser } = useDataSource();
// NEW: const { data: users, isLoading } = useUsers(filters);
//      const { mutate: createUser } = useCreateUser();
import { useDataSource } from "../context/DataSourceContext";
// AdminDashboardRefactorv2: REPLACE - Use shadcn/ui Dialog instead
import Modal from "../components/Modal";
// AdminDashboardRefactorv2: REPLACE - Use shadcn/ui form components
import FormInput from "../components/forms/FormInput";
import FormTextarea from "../components/forms/FormTextarea";
import Button from "../components/forms/Button";
// AdminDashboardRefactorv2: REPLACE - Use Tailwind classes instead
import ONETRUTH, { getStatusColor } from "../config/theme";

export default function Users() {
  const { getUsers, createUser, updateUser, deleteUser, seedUsers } = useDataSource();

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeFilter, setActiveFilter] = useState("all");

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  // Seed states
  const [seeding, setSeeding] = useState(false);
  const [seedMessage, setSeedMessage] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    profile_data: {
      display_name: "",
      bio: "",
      location: "",
      website: "",
    },
    is_active: true,
    is_verified: false,
  });

  const [formErrors, setFormErrors] = useState({});

  // Load users
  const loadUsers = async () => {
    setLoading(true);
    try {
      const filters = {
        search: searchTerm || undefined,
        active_only: activeFilter === "active" || undefined,
        verified_only: activeFilter === "verified" || undefined,
        limit: 100,
      };
      const response = await getUsers(filters);
      setUsers(response.results);
    } catch (error) {
      console.error("Error loading users:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, [searchTerm, activeFilter]);

  // Form handlers
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name.startsWith("profile_")) {
      const fieldName = name.replace("profile_", "");
      setFormData({
        ...formData,
        profile_data: {
          ...formData.profile_data,
          [fieldName]: value,
        },
      });
    } else {
      setFormData({
        ...formData,
        [name]: type === "checkbox" ? checked : value,
      });
    }
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.username || formData.username.length < 3) {
      errors.username = "Username must be at least 3 characters";
    }
    if (!formData.email || !/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = "Valid email is required";
    }
    if (!selectedUser && (!formData.password || formData.password.length < 8)) {
      errors.password = "Password must be at least 8 characters";
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      await createUser(formData);
      setShowCreateModal(false);
      resetForm();
      loadUsers();
    } catch (error) {
      console.error("Error creating user:", error);
    }
  };

  const handleEditUser = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const updates = {
        username: formData.username,
        email: formData.email,
        profile_data: formData.profile_data,
        is_active: formData.is_active,
        is_verified: formData.is_verified,
      };
      await updateUser(selectedUser.id, updates);
      setShowEditModal(false);
      resetForm();
      loadUsers();
    } catch (error) {
      console.error("Error updating user:", error);
    }
  };

  const handleDeleteUser = async () => {
    try {
      await deleteUser(selectedUser.id);
      setShowDeleteModal(false);
      setSelectedUser(null);
      loadUsers();
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  const resetForm = () => {
    setFormData({
      username: "",
      email: "",
      password: "",
      profile_data: {
        display_name: "",
        bio: "",
        location: "",
        website: "",
      },
      is_active: true,
      is_verified: false,
    });
    setFormErrors({});
    setSelectedUser(null);
  };

  const openEditModal = (user) => {
    setSelectedUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      password: "",
      profile_data: user.profile_data,
      is_active: user.is_active,
      is_verified: user.is_verified,
    });
    setShowEditModal(true);
  };

  const openDeleteModal = (user) => {
    setSelectedUser(user);
    setShowDeleteModal(true);
  };

  // Seed database handler
  const handleSeedDatabase = async () => {
    if (!window.confirm("Seed database with 50 new users? This will ADD new users to the existing ones.")) {
      return;
    }

    setSeeding(true);
    setSeedMessage(null);

    try {
      const result = await seedUsers(50);
      setSeedMessage({
        type: "success",
        text: result.message,
        stats: result.statistics
      });
      // Reload users to show the new data
      loadUsers();
    } catch (error) {
      console.error("Error seeding database:", error);
      setSeedMessage({
        type: "error",
        text: error.response?.data?.detail || "Failed to seed database"
      });
    } finally {
      setSeeding(false);
      // Clear message after 5 seconds
      setTimeout(() => setSeedMessage(null), 5000);
    }
  };

  // Statistics
  const stats = {
    total: users.length,
    active: users.filter((u) => u.is_active).length,
    verified: users.filter((u) => u.is_verified).length,
    inactive: users.filter((u) => !u.is_active).length,
  };

  return (
    <div className="space-y-6">
      {/* Header with stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: "Total Users", value: stats.total, color: ONETRUTH.colors.info },
          { label: "Active", value: stats.active, color: ONETRUTH.colors.success },
          { label: "Verified", value: stats.verified, color: ONETRUTH.colors.secondary },
          { label: "Inactive", value: stats.inactive, color: ONETRUTH.colors.error },
        ].map((stat) => (
          <div
            key={stat.label}
            className="p-6 rounded-lg shadow"
            style={{ backgroundColor: ONETRUTH.colors.surface }}
          >
            <p
              className="text-sm font-medium mb-1"
              style={{ color: ONETRUTH.colors.textLight }}
            >
              {stat.label}
            </p>
            <p
              className="text-3xl font-bold"
              style={{ color: stat.color }}
            >
              {stat.value}
            </p>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div
        className="p-4 rounded-lg shadow"
        style={{ backgroundColor: ONETRUTH.colors.surface }}
      >
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="flex-1 w-full md:w-auto">
            <input
              type="text"
              placeholder="Search users by name, email, or username..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
              style={{
                borderColor: ONETRUTH.colors.border,
                fontFamily: ONETRUTH.fonts.body,
              }}
            />
          </div>

          <div className="flex gap-2">
            {["all", "active", "verified", "inactive"].map((filter) => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                className="px-4 py-2 rounded-lg font-medium capitalize transition-all"
                style={{
                  backgroundColor:
                    activeFilter === filter
                      ? ONETRUTH.colors.primary
                      : ONETRUTH.colors.backgroundDark,
                  color:
                    activeFilter === filter
                      ? ONETRUTH.colors.textInverse
                      : ONETRUTH.colors.textLight,
                }}
              >
                {filter}
              </button>
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              variant="secondary"
              onClick={handleSeedDatabase}
              disabled={seeding}
              icon={
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              }
            >
              {seeding ? "Seeding..." : "Seed Database (50)"}
            </Button>

            <Button
              variant="primary"
              onClick={() => setShowCreateModal(true)}
              icon={
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
            }
          >
            Create User
          </Button>
          </div>
        </div>
      </div>

      {/* Seed Message */}
      {seedMessage && (
        <div
          className="p-4 rounded-lg shadow"
          style={{
            backgroundColor: seedMessage.type === "success"
              ? ONETRUTH.colors.success + "20"
              : ONETRUTH.colors.error + "20",
            borderLeft: `4px solid ${seedMessage.type === "success"
              ? ONETRUTH.colors.success
              : ONETRUTH.colors.error}`,
          }}
        >
          <p
            className="font-medium"
            style={{
              color: seedMessage.type === "success"
                ? ONETRUTH.colors.success
                : ONETRUTH.colors.error,
            }}
          >
            {seedMessage.text}
          </p>
          {seedMessage.stats && (
            <p className="text-sm mt-2" style={{ color: ONETRUTH.colors.text }}>
              Users: {seedMessage.stats.users_created} | Experiences: {seedMessage.stats.experiences_created} |
              Avg: {seedMessage.stats.average_experiences_per_user} per user
            </p>
          )}
        </div>
      )}

      {/* Users Table */}
      <div
        className="rounded-lg shadow overflow-hidden"
        style={{ backgroundColor: ONETRUTH.colors.surface }}
      >
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead
              style={{
                backgroundColor: ONETRUTH.colors.backgroundDark,
                color: ONETRUTH.colors.textInverse,
              }}
            >
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                  Experiences
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y" style={{ borderColor: ONETRUTH.colors.border }}>
              {loading ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center">
                    Loading users...
                  </td>
                </tr>
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center">
                    No users found
                  </td>
                </tr>
              ) : (
                users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div
                            className="h-10 w-10 rounded-full flex items-center justify-center text-white font-semibold"
                            style={{ backgroundColor: ONETRUTH.colors.primary }}
                          >
                            {user.username.charAt(0).toUpperCase()}
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium">{user.profile_data.display_name}</div>
                          <div className="text-sm" style={{ color: ONETRUTH.colors.textLight }}>
                            @{user.username}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">{user.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">{user.profile_data.location || "—"}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex gap-2">
                        <span
                          className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                          style={{
                            backgroundColor: user.is_active
                              ? ONETRUTH.colors.success + "20"
                              : ONETRUTH.colors.error + "20",
                            color: user.is_active ? ONETRUTH.colors.success : ONETRUTH.colors.error,
                          }}
                        >
                          {user.is_active ? "Active" : "Inactive"}
                        </span>
                        {user.is_verified && (
                          <span
                            className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                            style={{
                              backgroundColor: ONETRUTH.colors.secondary + "20",
                              color: ONETRUTH.colors.secondary,
                            }}
                          >
                            Verified
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">{user.experiences.length}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => openEditModal(user)}
                        className="mr-3 hover:opacity-75"
                        style={{ color: ONETRUTH.colors.primary }}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => openDeleteModal(user)}
                        className="hover:opacity-75"
                        style={{ color: ONETRUTH.colors.error }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create User Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => {
          setShowCreateModal(false);
          resetForm();
        }}
        title="Create New User"
        size="lg"
      >
        <form onSubmit={handleCreateUser}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormInput
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              error={formErrors.username}
              required
            />
            <FormInput
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleInputChange}
              error={formErrors.email}
              required
            />
            <FormInput
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleInputChange}
              error={formErrors.password}
              required
              helpText="Minimum 8 characters"
            />
            <FormInput
              label="Display Name"
              name="profile_display_name"
              value={formData.profile_data.display_name}
              onChange={handleInputChange}
              required
            />
            <FormInput
              label="Location"
              name="profile_location"
              value={formData.profile_data.location}
              onChange={handleInputChange}
            />
            <FormInput
              label="Website"
              name="profile_website"
              type="url"
              value={formData.profile_data.website}
              onChange={handleInputChange}
            />
          </div>

          <FormTextarea
            label="Bio"
            name="profile_bio"
            value={formData.profile_data.bio}
            onChange={handleInputChange}
            rows={3}
          />

          <div className="flex gap-4 mb-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleInputChange}
              />
              <span className="text-sm font-medium">Active</span>
            </label>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="is_verified"
                checked={formData.is_verified}
                onChange={handleInputChange}
              />
              <span className="text-sm font-medium">Verified</span>
            </label>
          </div>

          <div className="flex gap-3 justify-end">
            <Button
              variant="ghost"
              onClick={() => {
                setShowCreateModal(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Create User
            </Button>
          </div>
        </form>
      </Modal>

      {/* Edit User Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          resetForm();
        }}
        title="Edit User"
        size="lg"
      >
        <form onSubmit={handleEditUser}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormInput
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              error={formErrors.username}
              required
            />
            <FormInput
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleInputChange}
              error={formErrors.email}
              required
            />
            <FormInput
              label="Display Name"
              name="profile_display_name"
              value={formData.profile_data.display_name}
              onChange={handleInputChange}
              required
            />
            <FormInput
              label="Location"
              name="profile_location"
              value={formData.profile_data.location}
              onChange={handleInputChange}
            />
            <FormInput
              label="Website"
              name="profile_website"
              type="url"
              value={formData.profile_data.website}
              onChange={handleInputChange}
            />
          </div>

          <FormTextarea
            label="Bio"
            name="profile_bio"
            value={formData.profile_data.bio}
            onChange={handleInputChange}
            rows={3}
          />

          <div className="flex gap-4 mb-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleInputChange}
              />
              <span className="text-sm font-medium">Active</span>
            </label>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="is_verified"
                checked={formData.is_verified}
                onChange={handleInputChange}
              />
              <span className="text-sm font-medium">Verified</span>
            </label>
          </div>

          <div className="flex gap-3 justify-end">
            <Button
              variant="ghost"
              onClick={() => {
                setShowEditModal(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Save Changes
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => {
          setShowDeleteModal(false);
          setSelectedUser(null);
        }}
        title="Delete User"
        size="sm"
      >
        <div className="space-y-4">
          <p style={{ color: ONETRUTH.colors.text }}>
            Are you sure you want to delete user{" "}
            <strong>{selectedUser?.username}</strong>? This action cannot be undone and will also
            delete all of their experiences.
          </p>
          <div className="flex gap-3 justify-end">
            <Button
              variant="ghost"
              onClick={() => {
                setShowDeleteModal(false);
                setSelectedUser(null);
              }}
            >
              Cancel
            </Button>
            <Button variant="danger" onClick={handleDeleteUser}>
              Delete User
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}