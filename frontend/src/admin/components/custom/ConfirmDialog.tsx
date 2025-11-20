/**
 * ConfirmDialog Component
 *
 * @module admin/components/custom/ConfirmDialog
 */

import * as React from 'react'
import { AlertTriangle, Info, AlertCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface ConfirmDialogProps {
  /**
   * Show/hide dialog
   */
  isOpen: boolean
  /**
   * Dialog title
   */
  title: string
  /**
   * Dialog description/message
   */
  description: string
  /**
   * Confirm button text
   */
  confirmText?: string
  /**
   * Cancel button text
   */
  cancelText?: string
  /**
   * Variant for styling
   */
  variant?: 'default' | 'destructive' | 'warning'
  /**
   * Callback when confirmed
   */
  onConfirm: () => void | Promise<void>
  /**
   * Callback when canceled
   */
  onCancel: () => void
  /**
   * Loading state
   */
  isLoading?: boolean
}

const variantConfig = {
  default: {
    icon: Info,
    iconColor: 'text-blue-500',
    confirmClass: 'bg-primary hover:bg-primary/90 text-primary-foreground',
  },
  destructive: {
    icon: AlertTriangle,
    iconColor: 'text-destructive',
    confirmClass: 'bg-destructive hover:bg-destructive/90 text-destructive-foreground',
  },
  warning: {
    icon: AlertCircle,
    iconColor: 'text-yellow-500',
    confirmClass: 'bg-yellow-500 hover:bg-yellow-600 text-white',
  },
}

/**
 * Confirmation dialog with customizable actions
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false)
 *
 * <ConfirmDialog
 *   isOpen={isOpen}
 *   title="Delete User"
 *   description="Are you sure you want to delete this user? This action cannot be undone."
 *   variant="destructive"
 *   confirmText="Delete"
 *   cancelText="Cancel"
 *   onConfirm={async () => {
 *     await deleteUser(userId)
 *     setIsOpen(false)
 *   }}
 *   onCancel={() => setIsOpen(false)}
 * />
 * ```
 */
export function ConfirmDialog({
  isOpen,
  title,
  description,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'default',
  onConfirm,
  onCancel,
  isLoading = false,
}: ConfirmDialogProps) {
  const config = variantConfig[variant]
  const Icon = config.icon

  if (!isOpen) return null

  const handleConfirm = async () => {
    await onConfirm()
  }

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
        onClick={onCancel}
        aria-hidden="true"
      />

      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className="relative w-full max-w-lg rounded-lg border bg-background p-6 shadow-lg"
          role="dialog"
          aria-modal="true"
          aria-labelledby="dialog-title"
          aria-describedby="dialog-description"
        >
          {/* Icon */}
          <div className="mb-4 flex items-center gap-3">
            <div className={cn('rounded-full p-2 bg-muted', config.iconColor)}>
              <Icon className="h-6 w-6" />
            </div>
            <h2 id="dialog-title" className="text-lg font-semibold">
              {title}
            </h2>
          </div>

          {/* Description */}
          <p id="dialog-description" className="mb-6 text-sm text-muted-foreground">
            {description}
          </p>

          {/* Actions */}
          <div className="flex justify-end gap-2">
            <button
              onClick={onCancel}
              disabled={isLoading}
              className={cn(
                'rounded-md px-4 py-2 text-sm font-medium',
                'border border-input bg-background hover:bg-accent',
                'disabled:cursor-not-allowed disabled:opacity-50'
              )}
            >
              {cancelText}
            </button>
            <button
              onClick={handleConfirm}
              disabled={isLoading}
              className={cn(
                'rounded-md px-4 py-2 text-sm font-medium',
                config.confirmClass,
                'disabled:cursor-not-allowed disabled:opacity-50'
              )}
            >
              {isLoading ? 'Processing...' : confirmText}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

/**
 * Hook for managing confirm dialog state
 *
 * @example
 * ```tsx
 * const confirm = useConfirmDialog()
 *
 * const handleDelete = async () => {
 *   const confirmed = await confirm.show({
 *     title: 'Delete User',
 *     description: 'Are you sure?',
 *     variant: 'destructive',
 *   })
 *
 *   if (confirmed) {
 *     await deleteUser()
 *   }
 * }
 * ```
 */
export function useConfirmDialog() {
  const [state, setState] = React.useState<{
    isOpen: boolean
    config: Omit<ConfirmDialogProps, 'isOpen' | 'onConfirm' | 'onCancel'>
    resolve: ((value: boolean) => void) | null
  }>({
    isOpen: false,
    config: { title: '', description: '' },
    resolve: null,
  })

  const show = (config: Omit<ConfirmDialogProps, 'isOpen' | 'onConfirm' | 'onCancel'>) => {
    return new Promise<boolean>((resolve) => {
      setState({
        isOpen: true,
        config,
        resolve,
      })
    })
  }

  const handleConfirm = () => {
    state.resolve?.(true)
    setState({ isOpen: false, config: { title: '', description: '' }, resolve: null })
  }

  const handleCancel = () => {
    state.resolve?.(false)
    setState({ isOpen: false, config: { title: '', description: '' }, resolve: null })
  }

  const ConfirmDialogComponent = () => (
    <ConfirmDialog
      {...state.config}
      isOpen={state.isOpen}
      onConfirm={handleConfirm}
      onCancel={handleCancel}
    />
  )

  return {
    show,
    ConfirmDialog: ConfirmDialogComponent,
  }
}
