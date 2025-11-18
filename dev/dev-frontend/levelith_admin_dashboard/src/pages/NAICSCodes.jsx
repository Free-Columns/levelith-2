/**
 * NAICS Codes Management Page
 *
 * Comprehensive NAICS code browser with industry filtering and visualization
 */

import React, { useState, useEffect } from "react";
import { useDataSource } from "../context/DataSourceContext";
import ONETRUTH, { getNAICSColor } from "../config/theme";

export default function NAICSCodes() {
  const { getNAICSCodes } = useDataSource();
  const [codes, setCodes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [industryFilter, setIndustryFilter] = useState("all");

  useEffect(() => {
    loadCodes();
  }, [searchTerm, industryFilter]);

  const loadCodes = async () => {
    const filters = {
      search: searchTerm || undefined,
      industry: industryFilter !== "all" ? industryFilter : undefined,
    };
    const results = await getNAICSCodes(filters);
    setCodes(results);
  };

  const industries = ["all", "general", "technology", "education", "healthcare", "finance", "retail", "manufacturing", "services"];

  const industryStats = codes.reduce((acc, code) => {
    acc[code.industry] = (acc[code.industry] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(industryStats).map(([industry, count]) => (
          <div
            key={industry}
            className="p-4 rounded-lg shadow"
            style={{ backgroundColor: ONETRUTH.colors.surface }}
          >
            <p className="text-sm font-medium capitalize" style={{ color: getNAICSColor(industry) }}>
              {industry}
            </p>
            <p className="text-2xl font-bold">{count}</p>
          </div>
        ))}
      </div>

      <div className="p-4 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <div className="flex gap-4">
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
