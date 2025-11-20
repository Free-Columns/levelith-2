/**
 * Button Component
 *
 * Reusable button with multiple variants and sizes.
 */

import React from "react";
import ONETRUTH from "../../config/theme";

export default function Button({
  children,
  onClick,
  type = "button",
  variant = "primary",
  size = "md",
  disabled = false,
  fullWidth = false,
  icon,
  ...props
}) {
  const variants = {
    primary: {
      bg: ONETRUTH.colors.primary,
      hoverBg: ONETRUTH.colors.primaryDark,
      text: ONETRUTH.colors.textInverse,
    },
    secondary: {
      bg: ONETRUTH.colors.secondary,
      hoverBg: ONETRUTH.colors.secondaryDark,
      text: ONETRUTH.colors.textInverse,
    },
    danger: {
      bg: ONETRUTH.colors.error,
      hoverBg: ONETRUTH.colors.accentDark,
      text: ONETRUTH.colors.textInverse,
    },
    outline: {
      bg: "transparent",
      hoverBg: ONETRUTH.colors.primaryLight,
      text: ONETRUTH.colors.primary,
      border: ONETRUTH.colors.primary,
    },
    ghost: {
      bg: "transparent",
      hoverBg: ONETRUTH.colors.backgroundDark,
      text: ONETRUTH.colors.text,
    },
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  const style = variants[variant];

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${sizes[size]}
        ${fullWidth ? "w-full" : ""}
        font-medium rounded-lg
        transition-all duration-200
        flex items-center justify-center gap-2
        ${disabled ? "opacity-50 cursor-not-allowed" : "hover:shadow-md"}
        ${variant === "outline" ? "border-2" : "border-0"}
      `}
      style={{
        backgroundColor: disabled ? ONETRUTH.colors.borderLight : style.bg,
        color: style.text,
        borderColor: style.border || "transparent",
        fontFamily: ONETRUTH.fonts.body,
      }}
      onMouseEnter={(e) => {
        if (!disabled && variant !== "outline") {
          e.currentTarget.style.backgroundColor = style.hoverBg;
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled) {
          e.currentTarget.style.backgroundColor = style.bg;
        }
      }}
      {...props}
    >
      {icon && <span>{icon}</span>}
      {children}
    </button>
  );
}
