/**
 * Data Source Switcher Component
 *
 * Allows switching between local mock data and server API data.
 * Displays in the application header.
 */

import React from "react";
import { useDataSource, DATA_SOURCES } from "../context/DataSourceContext";
import ONETRUTH from "../config/theme";

export default function DataSourceSwitcher() {
  const { dataSource, switchDataSource } = useDataSource();

  const isLocal = dataSource === DATA_SOURCES.LOCAL;

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm font-medium text-gray-700">Data Source:</span>
      <div className="inline-flex rounded-lg border border-gray-300 bg-white p-1">
        <button
          onClick={() => switchDataSource(DATA_SOURCES.LOCAL)}
          className={`px-4 py-1.5 text-sm font-medium rounded-md transition-all ${
            isLocal
              ? "bg-blue-500 text-white shadow-sm"
              : "text-gray-600 hover:text-gray-800"
          }`}
          style={{
            backgroundColor: isLocal ? ONETRUTH.colors.primary : "transparent",
            color: isLocal ? ONETRUTH.colors.textInverse : ONETRUTH.colors.text,
          }}
        >
          <span className="flex items-center gap-2">
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Local (Mock)
          </span>
        </button>
        <button
          onClick={() => switchDataSource(DATA_SOURCES.SERVER)}
          className={`px-4 py-1.5 text-sm font-medium rounded-md transition-all ${
            !isLocal
              ? "bg-blue-500 text-white shadow-sm"
              : "text-gray-600 hover:text-gray-800"
          }`}
          style={{
            backgroundColor: !isLocal ? ONETRUTH.colors.primary : "transparent",
            color: !isLocal
              ? ONETRUTH.colors.textInverse
              : ONETRUTH.colors.text,
          }}
          disabled={true}
          title="Server API integration coming soon"
        >
          <span className="flex items-center gap-2">
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"
              />
            </svg>
            Server API
            {!isLocal && <span className="text-xs">(Coming Soon)</span>}
          </span>
        </button>
      </div>
    </div>
  );
}
