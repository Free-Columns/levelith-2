/**
 * Modal Component
 *
 * Reusable modal dialog for forms and confirmations.
 */

import React, { useEffect } from "react";
import ONETRUTH from "../config/theme";

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
  showCloseButton = true,
}) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }

    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const sizes = {
    sm: "max-w-md",
    md: "max-w-2xl",
    lg: "max-w-4xl",
    xl: "max-w-6xl",
  };

  return (
    <div
      className="fixed inset-0 flex items-center justify-center z-50"
      style={{ zIndex: ONETRUTH.zIndex.modal }}
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black opacity-50"
        onClick={onClose}
        style={{ zIndex: ONETRUTH.zIndex.modalBackdrop }}
      />

      {/* Modal Content */}
      <div
        className={`relative ${sizes[size]} w-full mx-4 rounded-lg shadow-xl overflow-hidden`}
        style={{
          backgroundColor: ONETRUTH.colors.surface,
          zIndex: ONETRUTH.zIndex.modal,
        }}
      >
        {/* Header */}
        <div
          className="px-6 py-4 border-b flex items-center justify-between"
          style={{ borderColor: ONETRUTH.colors.border }}
        >
          <h2
            className="text-xl font-semibold"
            style={{
              color: ONETRUTH.colors.textDark,
              fontFamily: ONETRUTH.fonts.heading,
            }}
          >
            {title}
          </h2>
          {showCloseButton && (
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              <svg
                className="w-6 h-6"
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
          )}
        </div>

        {/* Body */}
        <div className="px-6 py-4 max-h-[calc(100vh-200px)] overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
}
