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
    sm: {maxWidth: '28rem'}, // 448px
    md: {maxWidth: '42rem'}, // 672px
    lg: {maxWidth: '56rem'}, // 896px
    xl: {maxWidth: '72rem'}, // 1152px
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: ONETRUTH.zIndex.modal
      }}
    >
      {/* Backdrop */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: ONETRUTH.zIndex.modalBackdrop
        }}
        onClick={onClose}
      />

      {/* Modal Content */}
      <div
        style={{
          position: 'relative',
          ...sizes[size],
          width: '100%',
          margin: '0 16px',
          borderRadius: '8px',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          overflow: 'hidden',
          backgroundColor: ONETRUTH.colors.surface,
          zIndex: ONETRUTH.zIndex.modal
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '1.5rem',
            borderBottom: `1px solid ${ONETRUTH.colors.border}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <h2
            style={{
              fontSize: '1.25rem',
              fontWeight: 600,
              color: ONETRUTH.colors.textDark,
              fontFamily: ONETRUTH.fonts.heading
            }}
          >
            {title}
          </h2>
          {showCloseButton && (
            <button
              onClick={onClose}
              style={{
                color: ONETRUTH.colors.textLight,
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px',
                transition: 'color 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.color = ONETRUTH.colors.textDark}
              onMouseLeave={(e) => e.currentTarget.style.color = ONETRUTH.colors.textLight}
            >
              <svg
                style={{width: '24px', height: '24px'}}
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
        <div style={{
          padding: '1.5rem',
          maxHeight: 'calc(100vh - 200px)',
          overflowY: 'auto'
        }}>
          {children}
        </div>
      </div>
    </div>
  );
}
