/**
 * Form Button Component
 *
 * Reusable button component with variant styles (primary, secondary, danger).
 */

import React from "react";
import ONETRUTH from "../../config/theme";

export default function FormButton({
  children,
  variant = "primary",
  onClick,
  disabled = false,
  type = "button",
  className = "",
  style = {},
  ...props
}) {
  // Determine button styles based on variant
  const getVariantStyles = () => {
    switch (variant) {
      case "secondary":
        return {
          backgroundColor: ONETRUTH.colors.backgroundDark,
          color: ONETRUTH.colors.text,
          border: `1px solid ${ONETRUTH.colors.border}`,
        };
      case "danger":
        return {
          backgroundColor: ONETRUTH.colors.error,
          color: "white",
          border: "none",
        };
      case "primary":
      default:
        return {
          backgroundColor: ONETRUTH.colors.primary,
          color: "white",
          border: "none",
        };
    }
  };

  const variantStyles = getVariantStyles();

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 ${
        disabled ? "opacity-50 cursor-not-allowed" : "hover:opacity-90 cursor-pointer"
      } ${className}`}
      style={{
        ...variantStyles,
        fontFamily: ONETRUTH.fonts.body,
        ...style, // Allow custom styles to override defaults
      }}
      {...props}
    >
      {children}
    </button>
  );
}
