import styles from './EmptyState.module.css'

interface Props {
  label: string
}

export default function EmptyState({ label }: Props) {
  return (
    <div className={styles.wrapper}>
      <span className={styles.glyph} aria-hidden="true">◈</span>
      <span className={styles.label}>{label}</span>
    </div>
  )
}
