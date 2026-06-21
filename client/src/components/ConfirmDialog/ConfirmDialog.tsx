import { useEffect } from 'react'
import styles from './ConfirmDialog.module.css'

interface Props {
  threadId: string
  onConfirm: () => void
  onCancel: () => void
}

export default function ConfirmDialog({ threadId, onConfirm, onCancel }: Props) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCancel()
      if (e.key === 'Enter') onConfirm()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onCancel, onConfirm])

  return (
    <div className={styles.overlay} onClick={onCancel} role="dialog" aria-modal="true">
      <div className={styles.box} onClick={(e) => e.stopPropagation()}>
        <p className={styles.title}>Delete thread</p>
        <p className={styles.body}>
          Delete thread <strong className={styles.threadName}>{threadId}</strong>?
          This cannot be undone.
        </p>
        <div className={styles.actions}>
          <button className={styles.btnCancel} onClick={onCancel}>
            Cancel
          </button>
          <button className={styles.btnDelete} onClick={onConfirm} autoFocus>
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}
