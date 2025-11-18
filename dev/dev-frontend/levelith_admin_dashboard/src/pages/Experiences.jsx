/**
 * Experiences Page - Comprehensive CRUD for all 9 experience types
 *
 * NOTE: This is a placeholder implementation showing experience listing.
 * Full CRUD functionality with type-specific forms to be completed.
 */

import React, { useState, useEffect } from "react";
import { useDataSource } from "../context/DataSourceContext";
import ONETRUTH, { getCategoryColor } from "../config/theme";

export default function Experiences() {
  const { getExperiences } = useDataSource();
  const [experiences, setExperiences] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    loadExperiences();
  }, [categoryFilter, searchTerm]);

  const loadExperiences = async () => {
    const filters = {
      category: categoryFilter !== "all" ? categoryFilter : undefined,
      search: searchTerm || undefined,
      limit: 50,
    };
    const response = await getExperiences(filters);
    setExperiences(response.results);
  };

  const categoryCounts = {
    all: experiences.length,
    education: experiences.filter((e) => e.category === "education").length,
    workplace: experiences.filter((e) => e.category === "workplace").length,
    skills: experiences.filter((e) => e.category === "skills").length,
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {Object.entries(categoryCounts).map(([category, count]) => (
          <div
            key={category}
            className="p-6 rounded-lg shadow cursor-pointer transition-all"
            style={{
              backgroundColor: ONETRUTH.colors.surface,
              borderLeft: categoryFilter === category ? `4px solid ${getCategoryColor(category)}` : "none",
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

      <div className="p-4 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <input
          type="text"
          placeholder="Search experiences..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
          style={{ borderColor: ONETRUTH.colors.border }}
        />
      </div>

      <div className="rounded-lg shadow overflow-hidden" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <table className="w-full">
          <thead style={{ backgroundColor: ONETRUTH.colors.backgroundDark, color: ONETRUTH.colors.textInverse }}>
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
            {experiences.map((exp) => (
              <tr key={exp.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 font-medium">{exp.title}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-xs font-semibold capitalize">{exp.experience_type.replace("_", " ")}</span>
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
                  {new Date(exp.start_date).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    className="mr-3 hover:opacity-75"
                    style={{ color: ONETRUTH.colors.primary }}
                  >
                    Edit
                  </button>
                  <button
                    className="hover:opacity-75"
                    style={{ color: ONETRUTH.colors.error }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="p-6 rounded-lg border-2 border-dashed" style={{ borderColor: ONETRUTH.colors.border }}>
        <p className="text-center" style={{ color: ONETRUTH.colors.textLight }}>
          <strong>Note:</strong> Full CRUD functionality with create/edit forms for all 9 experience types (Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill) to be implemented.
        </p>
      </div>
    </div>
  );
}