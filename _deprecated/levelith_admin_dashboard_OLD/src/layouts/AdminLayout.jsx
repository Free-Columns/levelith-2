import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import DataSourceSwitcher from "../components/DataSourceSwitcher";
import ONETRUTH from "../config/theme";

export default function AdminLayout() {
  const location = useLocation();

  const isActive = (path) => {
    if (path === "/" && location.pathname === "/") return true;
    if (path !== "/" && location.pathname.startsWith(path)) return true;
    return false;
  };

  const navItems = [
    { path: "/admin", label: "Admin Dashboard", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" },
    { path: "/admin/users", label: "Users", icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" },
    { path: "/admin/experiences", label: "Experiences", icon: "M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" },
    { path: "/admin/naics", label: "NAICS Codes", icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" },
    { path: "/admin/settings", label: "Settings", icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" },
  ];

  return (
    <div className="flex h-screen" style={{ backgroundColor: ONETRUTH.colors.background }}>
      {/* Sidebar */}
      <aside
        className="w-64 p-6 shadow-lg"
        style={{ backgroundColor: ONETRUTH.colors.surfaceDark }}
      >
        {/* Logo/Title */}
        <div className="mb-8">
          <h2
            className="text-2xl font-bold"
            style={{
              color: ONETRUTH.colors.textInverse,
              fontFamily: ONETRUTH.fonts.heading,
            }}
          >
            Levelith Admin
          </h2>
          <p
            className="text-sm mt-1"
            style={{ color: ONETRUTH.colors.textLight }}
          >
            Development Dashboard
          </p>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className="flex items-center gap-3 px-4 py-3 rounded-lg transition-all"
              style={{
                backgroundColor: isActive(item.path)
                  ? ONETRUTH.colors.primary
                  : "transparent",
                color: isActive(item.path)
                  ? ONETRUTH.colors.textInverse
                  : ONETRUTH.colors.textLight,
              }}
            >
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
                  d={item.icon}
                />
              </svg>
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header
          className="px-6 py-4 shadow-sm border-b flex items-center justify-between"
          style={{
            backgroundColor: ONETRUTH.colors.surface,
            borderColor: ONETRUTH.colors.border,
          }}
        >
          <h1
            className="text-2xl font-semibold"
            style={{
              color: ONETRUTH.colors.textDark,
              fontFamily: ONETRUTH.fonts.heading,
            }}
          >
            {navItems.find((item) => isActive(item.path))?.label || "Dashboard"}
          </h1>
          <DataSourceSwitcher />
        </header>

        {/* Main Content */}
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
