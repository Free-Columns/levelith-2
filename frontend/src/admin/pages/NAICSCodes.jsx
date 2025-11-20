// ============================================================================
// AdminDashboardRefactorv2: MIGRATE - Phase 4 (NAICS Feature)
// ============================================================================
// What: Migrate to features/naics/ with tag/category editing
// Phase: 4 (NAICS Feature)
// Complexity: High (600+ lines, pagination, editing)
// Depends: Phase 1 (infrastructure)
//
// MIGRATION TASKS (20 total - see ADMIN_DASHBOARD_REFACTOR_V2.md Phase 4):
// ☐ Build NAICSTable with server-side pagination
// ☐ Build NAICSEditDialog for tags/category/notes editing
// ☐ Add NAICSFilters (search, category, level)
// ☐ Integrate with React Query
//
// REPLACE THIS FILE after migration
// ============================================================================

/**
 * NAICS Codes Management Page
 *
 * Comprehensive NAICS code browser with industry filtering, visualization,
 * and full CRUD operations for admin-specific fields.
 */

import React, { useState, useEffect } from "react";
// AdminDashboardRefactorv2: REPLACE - Use React Query
import { useDataSource } from "../context/DataSourceContext";
import apiService from "../services/apiService";
import ONETRUTH, { getNAICSColor } from "../config/theme";
import Modal from "../components/Modal";
import FormInput from "../components/forms/FormInput";
import FormTextarea from "../components/forms/FormTextarea";
import FormButton from "../components/forms/FormButton";
import TagInput from "../components/forms/TagInput";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function NAICSCodes() {
  const { dataSource } = useDataSource();
  const [codes, setCodes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [industryFilter, setIndustryFilter] = useState("all");
  const [levelFilter, setLevelFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  // Pagination state
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 50,
    total: 0,
    total_pages: 0,
  });

  // Modal state
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedCode, setSelectedCode] = useState(null);
  const [formData, setFormData] = useState({
    tags: [],
    custom_category: "",
    admin_notes: "",
  });

  useEffect(() => {
    loadCodes();
  }, [searchTerm, industryFilter, levelFilter, pagination.page, dataSource]);

  const loadCodes = async () => {
    setLoading(true);
    try {
      if (dataSource === "server") {
        // Use server-side pagination
        const results = await apiService.getNAICSCodesPaginated({
          query: searchTerm || undefined,
          category: industryFilter !== "all" ? industryFilter : undefined,
          level: levelFilter !== "all" ? parseInt(levelFilter) : undefined,
          page: pagination.page,
          page_size: pagination.page_size,
        });

        setCodes(results.items || []);
        setPagination({
          page: results.page,
          page_size: results.page_size,
          total: results.total,
          total_pages: results.total_pages,
        });
      } else {
        // Use local data source (DataSourceContext)
        const { getNAICSCodes } = await import("../context/DataSourceContext").then(
          (m) => m.useDataSource()
        );
        const filters = {
          search: searchTerm || undefined,
          industry: industryFilter !== "all" ? industryFilter : undefined,
          level: levelFilter !== "all" ? parseInt(levelFilter) : undefined,
        };
        const results = await getNAICSCodes(filters);
        setCodes(results);
      }
    } catch (error) {
      console.error("Error loading NAICS codes:", error);
      alert("Failed to load NAICS codes. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (code) => {
    setSelectedCode(code);
    setFormData({
      tags: code.tags || [],
      custom_category: code.custom_category || "",
      admin_notes: code.admin_notes || "",
    });
    setShowEditModal(true);
  };

  const handleUpdateCode = async () => {
    if (!selectedCode) return;

    try {
      const updated = await apiService.updateNAICSCode(selectedCode.code, formData);

      // Update local state
      setCodes((prevCodes) =>
        prevCodes.map((c) => (c.code === updated.code ? updated : c))
      );

      setShowEditModal(false);
      alert("NAICS code updated successfully");
    } catch (error) {
      console.error("Error updating NAICS code:", error);
      alert("Failed to update NAICS code. Check console for details.");
    }
  };

  const handleDelete = (code) => {
    setSelectedCode(code);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedCode) return;

    try {
      await apiService.deleteNAICSCode(selectedCode.code);

      // Remove from local state
      setCodes((prevCodes) => prevCodes.filter((c) => c.code !== selectedCode.code));

      setShowDeleteModal(false);
      setSelectedCode(null);
      alert("NAICS code deleted successfully");
    } catch (error) {
      console.error("Error deleting NAICS code:", error);
      alert("Failed to delete NAICS code. Check console for details.");
    }
  };

  const handlePageChange = (newPage) => {
    setPagination((prev) => ({ ...prev, page: newPage }));
  };

  const industries = ["all", "general", "technology", "education", "healthcare", "finance", "retail", "manufacturing", "services"];
  const levels = [
    { value: "all", label: "All Levels" },
    { value: "2", label: "Sector (2-digit)" },
    { value: "3", label: "Subsector (3-digit)" },
    { value: "4", label: "Industry Group (4-digit)" },
    { value: "6", label: "National Industry (6-digit)" },
  ];

  const industryStats = codes.reduce((acc, code) => {
    const category = code.category || code.industry || "general";
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {});

  const levelStats = codes.reduce((acc, code) => {
    const level = code.code?.length || 0;
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {});

  // Prepare chart data
  const industryChartData = Object.entries(industryStats).map(([industry, count]) => ({
    name: industry.charAt(0).toUpperCase() + industry.slice(1),
    count,
    color: getNAICSColor(industry),
  }));

  const levelChartData = Object.entries(levelStats)
    .sort(([a], [b]) => parseInt(a) - parseInt(b))
    .map(([level, count]) => {
      const levelNames = { "2": "Sector", "3": "Subsector", "4": "Industry Group", "6": "National Industry" };
      return {
        name: levelNames[level] || `${level}-digit`,
        count,
      };
    });

  return (
    <div className="space-y-6">
      {/* Overview Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Total NAICS Codes
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.primary }}>
            {dataSource === "server" ? pagination.total : codes.length}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Industries
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.secondary }}>
            {Object.keys(industryStats).length}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Current Page
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.info }}>
            {pagination.page} / {pagination.total_pages || 1}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Items Per Page
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.success }}>
            {pagination.page_size}
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Industry Distribution Bar Chart */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4">Industry Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={industryChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill={ONETRUTH.colors.primary}>
                {industryChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Level Distribution Pie Chart */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4">Level Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={levelChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.count}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {levelChartData.map((entry, index) => {
                  const colors = [ONETRUTH.colors.primary, ONETRUTH.colors.secondary, ONETRUTH.colors.info, ONETRUTH.colors.success];
                  return <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />;
                })}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Search and Filter Controls */}
      <div className="p-4 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <div className="flex flex-col md:flex-row gap-4">
          <input
            type="text"
            placeholder="Search NAICS codes..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPagination((prev) => ({ ...prev, page: 1 })); // Reset to page 1 on search
            }}
            className="flex-1 px-4 py-2 border rounded-lg"
            style={{ borderColor: ONETRUTH.colors.border }}
          />
          <select
            value={industryFilter}
            onChange={(e) => {
              setIndustryFilter(e.target.value);
              setPagination((prev) => ({ ...prev, page: 1 }));
            }}
            className="px-4 py-2 border rounded-lg"
            style={{ borderColor: ONETRUTH.colors.border }}
          >
            {industries.map((ind) => (
              <option key={ind} value={ind} className="capitalize">
                {ind}
              </option>
            ))}
          </select>
          <select
            value={levelFilter}
            onChange={(e) => {
              setLevelFilter(e.target.value);
              setPagination((prev) => ({ ...prev, page: 1 }));
            }}
            className="px-4 py-2 border rounded-lg"
            style={{ borderColor: ONETRUTH.colors.border }}
          >
            {levels.map((lvl) => (
              <option key={lvl.value} value={lvl.value}>
                {lvl.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* NAICS Codes Table */}
      <div className="rounded-lg shadow overflow-hidden" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        {loading ? (
          <div className="p-8 text-center" style={{ color: ONETRUTH.colors.textLight }}>
            Loading...
          </div>
        ) : (
          <>
            <table className="w-full">
              <thead style={{ backgroundColor: ONETRUTH.colors.backgroundDark, color: ONETRUTH.colors.textInverse }}>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">Code</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">Tags</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y" style={{ borderColor: ONETRUTH.colors.border }}>
                {codes.map((code) => (
                  <tr key={code.code} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap font-mono text-sm font-bold">{code.code}</td>
                    <td className="px-6 py-4">
                      <div className="font-medium">{code.title}</div>
                      <div className="text-sm text-gray-500">{code.description?.substring(0, 80)}...</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className="px-2 py-1 rounded text-xs font-semibold capitalize"
                        style={{
                          backgroundColor: getNAICSColor(code.category || code.industry) + "20",
                          color: getNAICSColor(code.category || code.industry),
                        }}
                      >
                        {code.category || code.industry}
                      </span>
                      {code.custom_category && (
                        <div className="mt-1">
                          <span className="px-2 py-1 rounded text-xs bg-purple-100 text-purple-800">
                            {code.custom_category}
                          </span>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {code.tags && code.tags.length > 0 ? (
                          code.tags.map((tag, idx) => (
                            <span key={idx} className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">
                              {tag}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-gray-400">No tags</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleEdit(code)}
                          className="px-3 py-1 rounded text-sm font-medium text-white"
                          style={{ backgroundColor: ONETRUTH.colors.info }}
                          disabled={dataSource !== "server"}
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(code)}
                          className="px-3 py-1 rounded text-sm font-medium text-white"
                          style={{ backgroundColor: ONETRUTH.colors.error }}
                          disabled={dataSource !== "server"}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination Controls */}
            {dataSource === "server" && pagination.total_pages > 1 && (
              <div className="px-6 py-4 flex items-center justify-between border-t" style={{ borderColor: ONETRUTH.colors.border }}>
                <div className="text-sm" style={{ color: ONETRUTH.colors.textLight }}>
                  Showing {(pagination.page - 1) * pagination.page_size + 1} to{" "}
                  {Math.min(pagination.page * pagination.page_size, pagination.total)} of {pagination.total} results
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handlePageChange(1)}
                    disabled={pagination.page === 1}
                    className="px-3 py-1 rounded text-sm disabled:opacity-50"
                    style={{ backgroundColor: ONETRUTH.colors.primary, color: "white" }}
                  >
                    First
                  </button>
                  <button
                    onClick={() => handlePageChange(pagination.page - 1)}
                    disabled={pagination.page === 1}
                    className="px-3 py-1 rounded text-sm disabled:opacity-50"
                    style={{ backgroundColor: ONETRUTH.colors.primary, color: "white" }}
                  >
                    Previous
                  </button>
                  <span className="px-4 py-1 rounded" style={{ backgroundColor: ONETRUTH.colors.surface }}>
                    Page {pagination.page} of {pagination.total_pages}
                  </span>
                  <button
                    onClick={() => handlePageChange(pagination.page + 1)}
                    disabled={pagination.page === pagination.total_pages}
                    className="px-3 py-1 rounded text-sm disabled:opacity-50"
                    style={{ backgroundColor: ONETRUTH.colors.primary, color: "white" }}
                  >
                    Next
                  </button>
                  <button
                    onClick={() => handlePageChange(pagination.total_pages)}
                    disabled={pagination.page === pagination.total_pages}
                    className="px-3 py-1 rounded text-sm disabled:opacity-50"
                    style={{ backgroundColor: ONETRUTH.colors.primary, color: "white" }}
                  >
                    Last
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Edit Modal */}
      {showEditModal && selectedCode && (
        <Modal
          title={`Edit NAICS Code: ${selectedCode.code}`}
          onClose={() => setShowEditModal(false)}
        >
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">Official Information (Read-Only)</h4>
              <p className="text-sm"><strong>Title:</strong> {selectedCode.title}</p>
              <p className="text-sm"><strong>Category:</strong> {selectedCode.category || selectedCode.industry}</p>
              <p className="text-sm"><strong>Description:</strong> {selectedCode.description}</p>
            </div>

            <hr />

            <div>
              <h4 className="font-semibold mb-2">Admin Fields (Editable)</h4>

              <TagInput
                label="Tags"
                value={formData.tags}
                onChange={(tags) => setFormData({ ...formData, tags })}
                placeholder="Add tags..."
              />

              <FormInput
                label="Custom Category"
                value={formData.custom_category}
                onChange={(e) => setFormData({ ...formData, custom_category: e.target.value })}
                placeholder="e.g., Priority Industries, High Demand"
              />

              <FormTextarea
                label="Admin Notes"
                value={formData.admin_notes}
                onChange={(e) => setFormData({ ...formData, admin_notes: e.target.value })}
                placeholder="Internal notes and comments..."
                rows={4}
              />
            </div>

            <div className="flex gap-2 justify-end">
              <FormButton
                variant="secondary"
                onClick={() => setShowEditModal(false)}
              >
                Cancel
              </FormButton>
              <FormButton onClick={handleUpdateCode}>
                Save Changes
              </FormButton>
            </div>
          </div>
        </Modal>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedCode && (
        <Modal
          title="Delete NAICS Code"
          onClose={() => setShowDeleteModal(false)}
        >
          <div className="space-y-4">
            <p className="text-red-600 font-semibold">
              ⚠️ WARNING: This action cannot be undone!
            </p>
            <p>
              Are you sure you want to delete NAICS code <strong>{selectedCode.code}</strong>?
            </p>
            <p className="text-sm text-gray-600">
              <strong>Title:</strong> {selectedCode.title}
            </p>
            <p className="text-xs text-gray-500">
              This should only be done for test or invalid codes. Official NAICS codes should not be deleted.
            </p>

            <div className="flex gap-2 justify-end">
              <FormButton
                variant="secondary"
                onClick={() => setShowDeleteModal(false)}
              >
                Cancel
              </FormButton>
              <FormButton
                variant="danger"
                onClick={handleDeleteConfirm}
                style={{ backgroundColor: ONETRUTH.colors.error }}
              >
                Delete Permanently
              </FormButton>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
