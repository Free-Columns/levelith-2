/**
 * Form Select Component
 *
 * Reusable select/dropdown field with label and validation.
 */

import React from "react";
import ONETRUTH from "../../config/theme";

export default function FormSelect({
  label,
  name,
  value,
  onChange,
  options = [],
  placeholder = "Select an option",
  required = false,
  error,
  disabled = false,
  helpText,
  ...props
}) {
  const selectId = `select-${name}`;

  return (
    <div className="mb-4">
      {label && (
        <label
          htmlFor={selectId}
          className="block text-sm font-medium mb-2"
          style={{ color: ONETRUTH.colors.text }}
        >
          {label}
          {required && (
            <span style={{ color: ONETRUTH.colors.error }}> *</span>
          )}
        </label>
      )}
      <select
        id={selectId}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-all ${
          error
            ? "border-red-500 focus:ring-red-200"
            : "border-gray-300 focus:ring-blue-200"
        } ${disabled ? "bg-gray-100 cursor-not-allowed" : "bg-white"}`}
        style={{
          borderColor: error ? ONETRUTH.colors.error : ONETRUTH.colors.border,
          fontFamily: ONETRUTH.fonts.body,
        }}
        {...props}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
          >
            {option.label}
          </option>
        ))}
      </select>
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
