/**
 * NAICS Codes Management Page
 *
 * Comprehensive NAICS code browser with industry filtering and visualization
 */

import React, { useState, useEffect } from "react";
import { useDataSource } from "../context/DataSourceContext";
import ONETRUTH, { getNAICSColor } from "../config/theme";
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
  const { getNAICSCodes } = useDataSource();
  const [codes, setCodes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [industryFilter, setIndustryFilter] = useState("all");
  const [levelFilter, setLevelFilter] = useState("all");

  useEffect(() => {
    loadCodes();
  }, [searchTerm, industryFilter, levelFilter]);

  const loadCodes = async () => {
    const filters = {
      search: searchTerm || undefined,
      industry: industryFilter !== "all" ? industryFilter : undefined,
      level: levelFilter !== "all" ? parseInt(levelFilter) : undefined,
    };
    const results = await getNAICSCodes(filters);
    setCodes(results);
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
    acc[code.industry] = (acc[code.industry] || 0) + 1;
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
            {codes.length}
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
            Hierarchy Levels
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.info }}>
            {Object.keys(levelStats).length}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Active Codes
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.success }}>
            {codes.filter((c) => c.is_active !== false).length}
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Industry Distribution Chart */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Distribution by Category
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={industryChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count">
                {industryChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Level Distribution Chart */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Distribution by Hierarchy Level
          </h3>
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
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg"
            style={{ borderColor: ONETRUTH.colors.border }}
          />
          <select
            value={industryFilter}
            onChange={(e) => setIndustryFilter(e.target.value)}
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
            onChange={(e) => setLevelFilter(e.target.value)}
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

      <div className="rounded-lg shadow overflow-hidden" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <table className="w-full">
          <thead style={{ backgroundColor: ONETRUTH.colors.backgroundDark, color: ONETRUTH.colors.textInverse }}>
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase">Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase">Industry</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y" style={{ borderColor: ONETRUTH.colors.border }}>
            {codes.map((code) => (
              <tr key={code.code} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-mono text-sm font-bold">{code.code}</td>
                <td className="px-6 py-4 font-medium">{code.title}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className="px-2 py-1 rounded text-xs font-semibold capitalize"
                    style={{
                      backgroundColor: getNAICSColor(code.industry) + "20",
                      color: getNAICSColor(code.industry),
                    }}
                  >
                    {code.industry}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm" style={{ color: ONETRUTH.colors.textLight }}>
                  {code.description}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
