/**
 * Tag Input Component
 *
 * Input field for managing arrays of tags (skills, achievements, etc.)
 */

import React, { useState } from "react";
import ONETRUTH from "../../config/theme";

export default function TagInput({
  label,
  name,
  value = [],
  onChange,
  placeholder = "Type and press Enter",
  required = false,
  error,
  helpText,
}) {
  const [inputValue, setInputValue] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && inputValue.trim()) {
      e.preventDefault();
      if (!value.includes(inputValue.trim())) {
        onChange([...value, inputValue.trim()]);
      }
      setInputValue("");
    } else if (e.key === "Backspace" && !inputValue && value.length > 0) {
      onChange(value.slice(0, -1));
    }
  };

  const removeTag = (indexToRemove) => {
    onChange(value.filter((_, index) => index !== indexToRemove));
  };

  return (
    <div className="mb-4">
      {label && (
        <label
          className="block text-sm font-medium mb-2"
          style={{ color: ONETRUTH.colors.text }}
        >
          {label}
          {required && (
            <span style={{ color: ONETRUTH.colors.error }}> *</span>
          )}
        </label>
      )}
      <div
        className="w-full px-3 py-2 border rounded-lg flex flex-wrap gap-2 items-center"
        style={{ borderColor: error ? ONETRUTH.colors.error : ONETRUTH.colors.border }}
      >
        {value.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center gap-1 px-2 py-1 rounded text-sm"
            style={{
              backgroundColor: ONETRUTH.colors.primaryLight,
              color: ONETRUTH.colors.textInverse,
            }}
          >
            {tag}
            <button
              type="button"
              onClick={() => removeTag(index)}
              className="hover:opacity-75 transition-opacity"
            >
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </span>
        ))}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={value.length === 0 ? placeholder : ""}
          className="flex-1 min-w-[120px] outline-none"
          style={{ fontFamily: ONETRUTH.fonts.body }}
        />
      </div>
      {error && (
        <p
          className="mt-1 text-sm"
          style={{ color: ONETRUTH.colors.error }}
        >
          {error}
        </p>
      )}
      {helpText && !error && (
        <p
          className="mt-1 text-sm"
          style={{ color: ONETRUTH.colors.textLight }}
        >
          {helpText}
        </p>
      )}
    </div>
  );
}
