/**
 * Hook for managing open/close state (dialogs, modals, dropdowns, etc.)
 *
 * @module admin/hooks/useDisclosure
 */

import { useState, useCallback } from 'react'

/**
 * Disclosure state and controls
 */
export interface UseDisclosureReturn {
  isOpen: boolean
  open: () => void
  close: () => void
  toggle: () => void
}

/**
 * Manage open/close state for UI elements
 *
 * @param initialState - Initial open state (default: false)
 * @returns Disclosure state and controls
 *
 * @example
 * ```tsx
 * const dialog = useDisclosure()
 *
 * return (
 *   <>
 *     <button onClick={dialog.open}>Open Dialog</button>
 *     <Dialog open={dialog.isOpen} onClose={dialog.close}>
 *       <DialogContent>Hello!</DialogContent>
 *     </Dialog>
 *   </>
 * )
 * ```
 */
export function useDisclosure(initialState = false): UseDisclosureReturn {
  const [isOpen, setIsOpen] = useState(initialState)

  const open = useCallback(() => {
    setIsOpen(true)
  }, [])

  const close = useCallback(() => {
    setIsOpen(false)
  }, [])

  const toggle = useCallback(() => {
    setIsOpen((prev) => !prev)
  }, [])

  return {
    isOpen,
    open,
    close,
    toggle,
  }
}
