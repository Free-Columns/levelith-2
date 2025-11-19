/**
 * Form Textarea Component
 *
 * Reusable textarea field with label and validation.
 */

import React from "react";
import ONETRUTH from "../../config/theme";

export default function FormTextarea({
  label,
  name,
  value,
  onChange,
  placeholder,
  required = false,
  error,
  disabled = false,
  helpText,
  rows = 4,
  ...props
}) {
  const textareaId = `textarea-${name}`;

  return (
    <div className="mb-4">
      {label && (
        <label
          htmlFor={textareaId}
          className="block text-sm font-medium mb-2"
          style={{ color: ONETRUTH.colors.text }}
        >
          {label}
          {required && (
            <span style={{ color: ONETRUTH.colors.error }}> *</span>
          )}
        </label>
      )}
      <textarea
        id={textareaId}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        rows={rows}
        className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-all resize-vertical ${
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
