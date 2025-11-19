/**
 * Form Input Component
 *
 * Reusable input field with label, validation, and error display.
 */

import React from "react";
import ONETRUTH from "../../config/theme";

export default function FormInput({
  label,
  name,
  type = "text",
  value,
  onChange,
  placeholder,
  required = false,
  error,
  disabled = false,
  helpText,
  ...props
}) {
  const inputId = `input-${name}`;

  return (
    <div className="mb-4">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium mb-2"
          style={{ color: ONETRUTH.colors.text }}
        >
          {label}
          {required && (
            <span style={{ color: ONETRUTH.colors.error }}> *</span>
          )}
        </label>
      )}
      <input
        id={inputId}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
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
      />
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
