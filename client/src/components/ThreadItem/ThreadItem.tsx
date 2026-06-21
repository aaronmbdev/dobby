import styles from './ThreadItem.module.css'

interface Props {
  id: string
  isActive: boolean
  onClick: () => void
  onDelete: () => void
}

export default function ThreadItem({ id, isActive, onClick, onDelete }: Props) {
  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    onDelete()
  }

  return (
    <div
      className={`${styles.item} ${isActive ? styles.active : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      aria-current={isActive ? 'true' : undefined}
    >
      <span className={styles.name}>{id}</span>
      <button
        className={styles.deleteBtn}
        onClick={handleDelete}
        title="Delete thread"
        aria-label={`Delete ${id}`}
      >
        <svg
          viewBox="0 0 12 12"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M2 3h8M5 3V2h2v1M4 3v6h4V3" />
        </svg>
      </button>
    </div>
  )
}
