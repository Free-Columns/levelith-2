// ============================================================================
// AdminDashboardRefactorv2: MIGRATE - Phase 3 (Experiences Feature)
// ============================================================================
// What: Migrate to features/experiences/ with TypeScript + polymorphic types
// Why: Handle all 9 experience types with type safety
// Risk: HIGH - complex polymorphic forms, multiple experience types
// Phase: 3 (Experiences Feature)
// Complexity: VERY HIGH (1017 lines! Needs decomposition)
// Depends: Phase 1 (infrastructure), Phase 2 (pattern established from Users)
//
// CURRENT PROBLEMS:
// 1. Massive 1000+ line file - needs decomposition
// 2. No type safety for 9 different experience types
// 3. Complex conditional rendering in forms
// 4. Manual state management
// 5. No proper validation per experience type
//
// NEW STRUCTURE (Phase 3):
// features/experiences/
//   ├── Experiences.tsx
//   ├── api/experiences.queries.ts
//   ├── api/experiences.mutations.ts
//   ├── components/
//   │   ├── ExperiencesTable.tsx
//   │   ├── ExperienceForm.tsx (polymorphic form handler)
//   │   ├── ExperienceFilters.tsx
//   │   ├── ExperienceTypeSelector.tsx
//   │   └── forms/ (9 type-specific forms)
//   │       ├── CertificateForm.tsx
//   │       ├── DegreeForm.tsx
//   │       ├── CourseForm.tsx
//   │       ├── GigForm.tsx
//   │       ├── PartTimeForm.tsx
//   │       ├── FullTimeForm.tsx
//   │       ├── SoftSkillForm.tsx
//   │       ├── HardSkillForm.tsx
//   │       └── NativeSkillForm.tsx
//   ├── schemas/ (Zod discriminated unions)
//   ├── types/experience.types.ts (polymorphic types)
//
// MIGRATION TASKS (30 total - see ADMIN_DASHBOARD_REFACTOR_V2.md Phase 3)
//
// REPLACE THIS ENTIRE FILE after migration
// ============================================================================

/**
 * Experiences Page - Complete CRUD for all 9 experience types
 *
 * Features:
 * - Hybrid form with common + type-specific fields
 * - Category filtering and search
 * - Create, Edit, Delete operations
 * - NAICS code integration
 */

import React, { useState, useEffect } from "react";
// AdminDashboardRefactorv2: REPLACE - Use React Query hooks
import { useDataSource } from "../context/DataSourceContext";
import Modal from "../components/Modal";
import FormInput from "../components/forms/FormInput";
import FormSelect from "../components/forms/FormSelect";
import FormTextarea from "../components/forms/FormTextarea";
import TagInput from "../components/forms/TagInput";
import Button from "../components/forms/Button";
import ONETRUTH, { getCategoryColor } from "../config/theme";

// Experience types by category
const EXPERIENCE_TYPES = {
  education: [
    { value: "certificate", label: "Certificate" },
    { value: "degree", label: "Degree" },
    { value: "course", label: "Course" },
  ],
  workplace: [
    { value: "gig", label: "Gig" },
    { value: "part_time", label: "Part-Time" },
    { value: "full_time", label: "Full-Time" },
  ],
  skills: [
    { value: "soft_skill", label: "Soft Skill" },
    { value: "hard_skill", label: "Hard Skill" },
    { value: "native_skill", label: "Native Skill" },
  ],
};

export default function Experiences() {
  const { getExperiences, createExperience, updateExperience, deleteExperience, getNAICSCodes } = useDataSource();

  const [experiences, setExperiences] = useState([]);
  const [naicsCodes, setNaicsCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedExperience, setSelectedExperience] = useState(null);

  // Form state - initialized with default values
  const [formData, setFormData] = useState({
    category: "education",
    experience_type: "certificate",
    title: "",
    description: "",
    naics_code: "123456",
    start_date: "",
    end_date: "",
    organization: "",
    location: "",
    skills_gained: [],
    achievements: [],
    metadata: {},
  });

  const [formErrors, setFormErrors] = useState({});

  // Load experiences
  const loadExperiences = async () => {
    setLoading(true);
    try {
      const filters = {
        category: categoryFilter !== "all" ? categoryFilter : undefined,
        experience_type: typeFilter !== "all" ? typeFilter : undefined,
        search: searchTerm || undefined,
        limit: 100,
      };
      const response = await getExperiences(filters);
      setExperiences(response.results);
    } catch (error) {
      console.error("Error loading experiences:", error);
    } finally {
      setLoading(false);
    }
  };

  // Load NAICS codes
  const loadNAICSCodes = async () => {
    try {
      const codes = await getNAICSCodes();
      setNaicsCodes(codes);
    } catch (error) {
      console.error("Error loading NAICS codes:", error);
    }
  };

  useEffect(() => {
    loadExperiences();
  }, [categoryFilter, typeFilter, searchTerm]);

  useEffect(() => {
    loadNAICSCodes();
  }, []);

  // Form handlers
  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Handle category change - update experience_type to match category
    if (name === "category") {
      const firstTypeForCategory = EXPERIENCE_TYPES[value][0].value;
      setFormData({
        ...formData,
        category: value,
        experience_type: firstTypeForCategory,
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleTagChange = (name, tags) => {
    setFormData({
      ...formData,
      [name]: tags,
    });
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.title || formData.title.length < 1) {
      errors.title = "Title is required";
    }
    if (!formData.category) {
      errors.category = "Category is required";
    }
    if (!formData.experience_type) {
      errors.experience_type = "Experience type is required";
    }
    if (!formData.naics_code) {
      errors.naics_code = "NAICS code is required";
    }
    if (formData.start_date && formData.end_date) {
      if (new Date(formData.end_date) < new Date(formData.start_date)) {
        errors.end_date = "End date must be after start date";
      }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleCreateExperience = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      // For demo purposes, assign to first user
      // In production, this would be the logged-in user
      const demoUserId = "user_demo_001";

      await createExperience({
        ...formData,
        user_id: demoUserId,
      });

      setShowCreateModal(false);
      resetForm();
      loadExperiences();
    } catch (error) {
      console.error("Error creating experience:", error);
    }
  };

  const handleEditExperience = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const updates = {
        title: formData.title,
        description: formData.description,
        naics_code: formData.naics_code,
        start_date: formData.start_date,
        end_date: formData.end_date,
        organization: formData.organization,
        location: formData.location,
        skills_gained: formData.skills_gained,
        achievements: formData.achievements,
        metadata: formData.metadata,
      };

      await updateExperience(selectedExperience.id, updates);
      setShowEditModal(false);
      resetForm();
      loadExperiences();
    } catch (error) {
      console.error("Error updating experience:", error);
    }
  };

  const handleDeleteExperience = async () => {
    try {
      await deleteExperience(selectedExperience.id);
      setShowDeleteModal(false);
      setSelectedExperience(null);
      loadExperiences();
    } catch (error) {
      console.error("Error deleting experience:", error);
    }
  };

  const resetForm = () => {
    setFormData({
      category: "education",
      experience_type: "certificate",
      title: "",
      description: "",
      naics_code: "123456",
      start_date: "",
      end_date: "",
      organization: "",
      location: "",
      skills_gained: [],
      achievements: [],
      metadata: {},
    });
    setFormErrors({});
    setSelectedExperience(null);
  };

  const openEditModal = (experience) => {
    setSelectedExperience(experience);
    setFormData({
      category: experience.category,
      experience_type: experience.experience_type,
      title: experience.title,
      description: experience.description || "",
      naics_code: experience.naics_code,
      start_date: experience.start_date ? experience.start_date.split("T")[0] : "",
      end_date: experience.end_date ? experience.end_date.split("T")[0] : "",
      organization: experience.organization || "",
      location: experience.location || "",
      skills_gained: experience.skills_gained || [],
      achievements: experience.achievements || [],
      metadata: experience.metadata || {},
    });
    setShowEditModal(true);
  };

  const openDeleteModal = (experience) => {
    setSelectedExperience(experience);
    setShowDeleteModal(true);
  };

  // Category counts
  const categoryCounts = {
    all: experiences.length,
    education: experiences.filter((e) => e.category === "education").length,
    workplace: experiences.filter((e) => e.category === "workplace").length,
    skills: experiences.filter((e) => e.category === "skills").length,
  };

  // Render type-specific fields based on selected experience type
  const renderTypeSpecificFields = () => {
    const { category, experience_type } = formData;

    // Common fields for all education types
    if (category === "education") {
      return (
        <>
          <FormInput
            label="Organization/Institution"
            name="organization"
            value={formData.organization}
            onChange={handleInputChange}
            placeholder="e.g., Harvard University, Udemy, AWS"
          />
          {experience_type === "certificate" && (
            <FormInput
              label="Credential ID (Optional)"
              name="metadata.credential_id"
              value={formData.metadata.credential_id || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  metadata: { ...formData.metadata, credential_id: e.target.value },
                })
              }
              placeholder="e.g., AWS-12345"
            />
          )}
          {experience_type === "degree" && (
            <>
              <FormInput
                label="Major/Field of Study"
                name="metadata.major"
                value={formData.metadata.major || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    metadata: { ...formData.metadata, major: e.target.value },
                  })
                }
                placeholder="e.g., Computer Science"
              />
              <FormSelect
                label="Degree Level"
                name="metadata.degree_level"
                value={formData.metadata.degree_level || "bachelors"}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    metadata: { ...formData.metadata, degree_level: e.target.value },
                  })
                }
                options={[
                  { value: "associates", label: "Associate's" },
                  { value: "bachelors", label: "Bachelor's" },
                  { value: "masters", label: "Master's" },
                  { value: "doctorate", label: "Doctorate" },
                ]}
              />
            </>
          )}
        </>
      );
    }

    // Common fields for all workplace types
    if (category === "workplace") {
      return (
        <>
          <FormInput
            label="Company/Organization"
            name="organization"
            value={formData.organization}
            onChange={handleInputChange}
            required
            placeholder="e.g., Google, Freelance, Local Business"
          />
          <FormInput
            label="Location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="e.g., San Francisco, CA or Remote"
          />
          {experience_type === "gig" && (
            <FormInput
              label="Project Duration (Optional)"
              name="metadata.project_duration"
              value={formData.metadata.project_duration || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  metadata: { ...formData.metadata, project_duration: e.target.value },
                })
              }
              placeholder="e.g., 3 months"
            />
          )}
          {(experience_type === "part_time" || experience_type === "full_time") && (
            <FormInput
              label="Job Title"
              name="metadata.job_title"
              value={formData.metadata.job_title || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  metadata: { ...formData.metadata, job_title: e.target.value },
                })
              }
              placeholder="e.g., Senior Software Engineer"
            />
          )}
        </>
      );
    }

    // Fields for skills
    if (category === "skills") {
      return (
        <>
          {experience_type === "soft_skill" && (
            <FormSelect
              label="Proficiency Level"
              name="metadata.proficiency_level"
              value={formData.metadata.proficiency_level || "intermediate"}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  metadata: { ...formData.metadata, proficiency_level: e.target.value },
                })
              }
              options={[
                { value: "beginner", label: "Beginner" },
                { value: "intermediate", label: "Intermediate" },
                { value: "advanced", label: "Advanced" },
                { value: "expert", label: "Expert" },
              ]}
            />
          )}
          {experience_type === "hard_skill" && (
            <>
              <FormSelect
                label="Skill Level"
                name="metadata.skill_level"
                value={formData.metadata.skill_level || "intermediate"}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    metadata: { ...formData.metadata, skill_level: e.target.value },
                  })
                }
                options={[
                  { value: "beginner", label: "Beginner" },
                  { value: "intermediate", label: "Intermediate" },
                  { value: "advanced", label: "Advanced" },
                  { value: "expert", label: "Expert" },
                ]}
              />
              <FormInput
                label="Years of Experience"
                name="metadata.years_experience"
                type="number"
                value={formData.metadata.years_experience || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    metadata: { ...formData.metadata, years_experience: e.target.value },
                  })
                }
                placeholder="e.g., 5"
              />
            </>
          )}
          {experience_type === "native_skill" && (
            <FormInput
              label="Fluency Level (for languages)"
              name="metadata.fluency_level"
              value={formData.metadata.fluency_level || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  metadata: { ...formData.metadata, fluency_level: e.target.value },
                })
              }
              placeholder="e.g., Native, Fluent, Conversational"
            />
          )}
        </>
      );
    }

    return null;
  };

  return (
    <div className="space-y-6">
      {/* Category Filter Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {Object.entries(categoryCounts).map(([category, count]) => (
          <div
            key={category}
            className="p-6 rounded-lg shadow cursor-pointer transition-all hover:shadow-lg"
            style={{
              backgroundColor: ONETRUTH.colors.surface,
              borderLeft:
                categoryFilter === category ? `4px solid ${getCategoryColor(category)}` : "none",
            }}
            onClick={() => setCategoryFilter(category)}
          >
            <p
              className="text-sm font-medium capitalize mb-1"
              style={{ color: getCategoryColor(category) }}
            >
              {category}
            </p>
            <p className="text-3xl font-bold">{count}</p>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div className="p-4 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <div className="flex flex-col md:flex-row gap-4 items-center">
          <div className="flex-1 w-full md:w-auto">
            <input
              type="text"
              placeholder="Search experiences by title or description..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
              style={{
                borderColor: ONETRUTH.colors.border,
                fontFamily: ONETRUTH.fonts.body,
              }}
            />
          </div>

          <div>
            <select
              value={categoryFilter}
              onChange={(e) => {
                setCategoryFilter(e.target.value);
                setTypeFilter("all"); // Reset type filter when category changes
              }}
              className="px-4 py-2 border rounded-lg"
              style={{
                borderColor: ONETRUTH.colors.border,
                fontFamily: ONETRUTH.fonts.body,
                minWidth: '150px'
              }}
            >
              <option value="all">All Categories</option>
              <option value="education">Education</option>
              <option value="workplace">Workplace</option>
              <option value="skills">Skills</option>
            </select>
          </div>

          <div>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="px-4 py-2 border rounded-lg"
              style={{
                borderColor: ONETRUTH.colors.border,
                fontFamily: ONETRUTH.fonts.body,
                minWidth: '150px'
              }}
            >
              <option value="all">All Types</option>
              {categoryFilter === "all" ? (
                <>
                  <optgroup label="Education">
                    {EXPERIENCE_TYPES.education.map(type => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </optgroup>
                  <optgroup label="Workplace">
                    {EXPERIENCE_TYPES.workplace.map(type => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </optgroup>
                  <optgroup label="Skills">
                    {EXPERIENCE_TYPES.skills.map(type => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </optgroup>
                </>
              ) : (
                EXPERIENCE_TYPES[categoryFilter]?.map(type => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))
              )}
            </select>
          </div>

          <Button
            variant="primary"
            onClick={() => setShowCreateModal(true)}
            icon={
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
            }
          >
            Add Experience
          </Button>
        </div>
      </div>

      {/* Experiences Table */}
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
                <th className="px-6 py-3 text-left text-xs font-medium uppercase">Title</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase">Organization</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase">Date</th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y" style={{ borderColor: ONETRUTH.colors.border }}>
              {loading ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center">
                    Loading experiences...
                  </td>
                </tr>
              ) : experiences.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center">
                    No experiences found. Create your first experience!
                  </td>
                </tr>
              ) : (
                experiences.map((exp) => (
                  <tr key={exp.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium">{exp.title}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-xs font-semibold capitalize">
                        {exp.experience_type.replace("_", " ")}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className="px-2 py-1 rounded text-xs font-semibold capitalize"
                        style={{
                          backgroundColor: getCategoryColor(exp.category) + "20",
                          color: getCategoryColor(exp.category),
                        }}
                      >
                        {exp.category}
                      </span>
                    </td>
                    <td className="px-6 py-4">{exp.organization || "—"}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {exp.start_date ? new Date(exp.start_date).toLocaleDateString() : "—"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => openEditModal(exp)}
                        className="mr-3 hover:opacity-75"
                        style={{ color: ONETRUTH.colors.primary }}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => openDeleteModal(exp)}
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

      {/* Create Experience Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => {
          setShowCreateModal(false);
          resetForm();
        }}
        title="Add New Experience"
        size="xl"
      >
        <form onSubmit={handleCreateExperience}>
          <div className="space-y-4">
            {/* Category & Type Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormSelect
                label="Category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                error={formErrors.category}
                required
                options={[
                  { value: "education", label: "Education" },
                  { value: "workplace", label: "Workplace" },
                  { value: "skills", label: "Skills" },
                ]}
              />
              <FormSelect
                label="Experience Type"
                name="experience_type"
                value={formData.experience_type}
                onChange={handleInputChange}
                error={formErrors.experience_type}
                required
                options={EXPERIENCE_TYPES[formData.category]}
              />
            </div>

            {/* Common Fields */}
            <FormInput
              label="Title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              error={formErrors.title}
              required
              placeholder="e.g., AWS Certified Solutions Architect"
            />

            <FormTextarea
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              placeholder="Describe this experience, what you learned, and your achievements..."
            />

            {/* NAICS Code */}
            <FormSelect
              label="NAICS Code (Industry Classification)"
              name="naics_code"
              value={formData.naics_code}
              onChange={handleInputChange}
              error={formErrors.naics_code}
              required
              options={[
                { value: "123456", label: "123456 - GENERAL" },
                ...naicsCodes.map((code) => ({
                  value: code.code,
                  label: `${code.code} - ${code.title}`,
                })),
              ]}
            />

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormInput
                label="Start Date"
                name="start_date"
                type="date"
                value={formData.start_date}
                onChange={handleInputChange}
              />
              <FormInput
                label="End Date (leave blank if ongoing)"
                name="end_date"
                type="date"
                value={formData.end_date}
                onChange={handleInputChange}
                error={formErrors.end_date}
              />
            </div>

            {/* Type-Specific Fields */}
            <div className="border-t pt-4" style={{ borderColor: ONETRUTH.colors.border }}>
              <h4 className="text-sm font-semibold mb-3" style={{ color: ONETRUTH.colors.textDark }}>
                {formData.category.charAt(0).toUpperCase() + formData.category.slice(1)}-Specific Details
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {renderTypeSpecificFields()}
              </div>
            </div>

            {/* Skills & Achievements */}
            <TagInput
              label="Skills Gained"
              value={formData.skills_gained}
              onChange={(tags) => handleTagChange("skills_gained", tags)}
              placeholder="Add a skill and press Enter"
            />

            <TagInput
              label="Achievements"
              value={formData.achievements}
              onChange={(tags) => handleTagChange("achievements", tags)}
              placeholder="Add an achievement and press Enter"
            />
          </div>

          <div className="flex gap-3 justify-end mt-6">
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
              Create Experience
            </Button>
          </div>
        </form>
      </Modal>

      {/* Edit Experience Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          resetForm();
        }}
        title="Edit Experience"
        size="xl"
      >
        <form onSubmit={handleEditExperience}>
          <div className="space-y-4">
            {/* Show category & type as read-only */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Category</label>
                <div className="px-4 py-2 bg-gray-100 rounded-lg capitalize">
                  {formData.category}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Experience Type</label>
                <div className="px-4 py-2 bg-gray-100 rounded-lg capitalize">
                  {formData.experience_type.replace("_", " ")}
                </div>
              </div>
            </div>

            {/* Common Fields */}
            <FormInput
              label="Title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              error={formErrors.title}
              required
            />

            <FormTextarea
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
            />

            {/* NAICS Code */}
            <FormSelect
              label="NAICS Code (Industry Classification)"
              name="naics_code"
              value={formData.naics_code}
              onChange={handleInputChange}
              error={formErrors.naics_code}
              required
              options={[
                { value: "123456", label: "123456 - GENERAL" },
                ...naicsCodes.map((code) => ({
                  value: code.code,
                  label: `${code.code} - ${code.title}`,
                })),
              ]}
            />

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormInput
                label="Start Date"
                name="start_date"
                type="date"
                value={formData.start_date}
                onChange={handleInputChange}
              />
              <FormInput
                label="End Date (leave blank if ongoing)"
                name="end_date"
                type="date"
                value={formData.end_date}
                onChange={handleInputChange}
                error={formErrors.end_date}
              />
            </div>

            {/* Type-Specific Fields */}
            <div className="border-t pt-4" style={{ borderColor: ONETRUTH.colors.border }}>
              <h4 className="text-sm font-semibold mb-3" style={{ color: ONETRUTH.colors.textDark }}>
                {formData.category.charAt(0).toUpperCase() + formData.category.slice(1)}-Specific Details
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {renderTypeSpecificFields()}
              </div>
            </div>

            {/* Skills & Achievements */}
            <TagInput
              label="Skills Gained"
              value={formData.skills_gained}
              onChange={(tags) => handleTagChange("skills_gained", tags)}
              placeholder="Add a skill and press Enter"
            />

            <TagInput
              label="Achievements"
              value={formData.achievements}
              onChange={(tags) => handleTagChange("achievements", tags)}
              placeholder="Add an achievement and press Enter"
            />
          </div>

          <div className="flex gap-3 justify-end mt-6">
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
          setSelectedExperience(null);
        }}
        title="Delete Experience"
        size="sm"
      >
        <div className="space-y-4">
          <p style={{ color: ONETRUTH.colors.text }}>
            Are you sure you want to delete the experience{" "}
            <strong>{selectedExperience?.title}</strong>? This action cannot be undone.
          </p>
          <div className="flex gap-3 justify-end">
            <Button
              variant="ghost"
              onClick={() => {
                setShowDeleteModal(false);
                setSelectedExperience(null);
              }}
            >
              Cancel
            </Button>
            <Button variant="danger" onClick={handleDeleteExperience}>
              Delete Experience
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
