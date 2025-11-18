/**
 * Dashboard - Overview and Analytics
 *
 * Displays statistics, visualizations, and key metrics
 */

import React, { useState, useEffect } from "react";
import { useDataSource } from "../context/DataSourceContext";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import ONETRUTH, { getCategoryColor, getNAICSColor } from "../config/theme";

export default function Dashboard() {
  const { getStats } = useDataSource();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const data = getStats();
    setStats(data);
  }, []);

  if (!stats) {
    return <div>Loading...</div>;
  }

  // Prepare chart data
  const categoryData = Object.entries(stats.experiences.byCategory).map(([category, count]) => ({
    name: category.charAt(0).toUpperCase() + category.slice(1),
    value: count,
    color: getCategoryColor(category),
  }));

  const industryData = Object.entries(stats.experiences.byIndustry).map(([industry, count]) => ({
    name: industry.charAt(0).toUpperCase() + industry.slice(1),
    value: count,
    color: getNAICSColor(industry),
  }));

  const typeData = Object.entries(stats.experiences.byType).map(([type, count]) => ({
    name: type.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
    count,
  }));

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Total Users
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.primary }}>
            {stats.users.total}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Active Users
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.success }}>
            {stats.users.active}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Total Experiences
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.secondary }}>
            {stats.experiences.total}
          </p>
        </div>
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <p className="text-sm font-medium" style={{ color: ONETRUTH.colors.textLight }}>
            Verified Users
          </p>
          <p className="text-4xl font-bold mt-2" style={{ color: ONETRUTH.colors.info }}>
            {stats.users.verified}
          </p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Experience by Category */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Experiences by Category
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Experience by Type */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Experiences by Type
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={typeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill={ONETRUTH.colors.primary} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Industry Distribution */}
      <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
          Industry Distribution (NAICS)
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {industryData.map((industry) => (
            <div key={industry.name} className="p-4 rounded border-l-4" style={{ borderColor: industry.color }}>
              <p className="text-sm font-medium capitalize" style={{ color: industry.color }}>
                {industry.name}
              </p>
              <p className="text-2xl font-bold">{industry.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* User Growth Over Time */}
      <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
          User Growth (Last 12 Months)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={stats.users.growth}>
            <defs>
              <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={ONETRUTH.colors.primary} stopOpacity={0.8} />
                <stop offset="95%" stopColor={ONETRUTH.colors.primary} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="users"
              stroke={ONETRUTH.colors.primary}
              fillOpacity={1}
              fill="url(#colorUsers)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* User Activity Timeline (Last 30 Days) */}
      <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
          User Activity (Last 30 Days)
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={stats.users.activity}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              angle={-45}
              textAnchor="end"
              height={80}
              interval={4}
            />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="logins"
              stroke={ONETRUTH.colors.success}
              strokeWidth={2}
              dot={{ fill: ONETRUTH.colors.success, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top Skills & Geographic Distribution Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Skills Trending */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Top Skills Trending
          </h3>
          {stats.skills.top.length > 0 ? (
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={stats.skills.top} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="skill" type="category" width={120} />
                <Tooltip />
                <Bar dataKey="count" fill={ONETRUTH.colors.secondary} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center py-8" style={{ color: ONETRUTH.colors.textLight }}>
              No skills data available yet
            </p>
          )}
        </div>

        {/* Geographic Distribution */}
        <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
          <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
            Geographic Distribution
          </h3>
          {stats.geography.locations.length > 0 ? (
            <div className="space-y-3">
              {stats.geography.locations.map((loc, index) => {
                const maxCount = stats.geography.locations[0].count;
                const percentage = (loc.count / maxCount) * 100;
                return (
                  <div key={index} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{loc.location}</span>
                      <span style={{ color: ONETRUTH.colors.textLight }}>{loc.count} users</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full transition-all"
                        style={{
                          width: `${percentage}%`,
                          backgroundColor: ONETRUTH.colors.info,
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-center py-8" style={{ color: ONETRUTH.colors.textLight }}>
              No location data available yet
            </p>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="p-6 rounded-lg shadow" style={{ backgroundColor: ONETRUTH.colors.surface }}>
        <h3 className="text-lg font-semibold mb-4" style={{ color: ONETRUTH.colors.textDark }}>
          Quick Actions
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <a
            href="/users"
            className="p-4 rounded-lg border-2 hover:shadow-md transition-all text-center"
            style={{ borderColor: ONETRUTH.colors.primary, color: ONETRUTH.colors.primary }}
          >
            <p className="font-semibold">Manage Users</p>
          </a>
          <a
            href="/experiences"
            className="p-4 rounded-lg border-2 hover:shadow-md transition-all text-center"
            style={{ borderColor: ONETRUTH.colors.secondary, color: ONETRUTH.colors.secondary }}
          >
            <p className="font-semibold">Manage Experiences</p>
          </a>
          <a
            href="/naics"
            className="p-4 rounded-lg border-2 hover:shadow-md transition-all text-center"
            style={{ borderColor: ONETRUTH.colors.info, color: ONETRUTH.colors.info }}
          >
            <p className="font-semibold">Browse NAICS</p>
          </a>
          <a
            href="/settings"
            className="p-4 rounded-lg border-2 hover:shadow-md transition-all text-center"
            style={{ borderColor: ONETRUTH.colors.textLight, color: ONETRUTH.colors.textLight }}
          >
            <p className="font-semibold">Settings</p>
          </a>
        </div>
      </div>
    </div>
  );
}