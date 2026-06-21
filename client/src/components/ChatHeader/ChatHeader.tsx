import styles from './ChatHeader.module.css'

interface Props {
  activeThread: string | null
  onShowThreads: () => void
}

export default function ChatHeader({ activeThread, onShowThreads }: Props) {
  return (
    <header className={styles.header}>
      {/* Back button only visible on mobile via CSS */}
      <button className={styles.backBtn} onClick={onShowThreads} aria-label="Show threads">
        ← threads
      </button>
      <span className={styles.slash}>thread /</span>
      <span className={styles.thread}>{activeThread ?? '—'}</span>
    </header>
  )
}
