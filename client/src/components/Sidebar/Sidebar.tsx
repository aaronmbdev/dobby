import StatusDot from '../StatusDot/StatusDot'
import ThreadItem from '../ThreadItem/ThreadItem'
import NewThreadButton from '../NewThreadButton/NewThreadButton'
import styles from './Sidebar.module.css'

interface Props {
  threads: string[]
  activeThread: string | null
  onSelectThread: (id: string) => void
  onNewThread: (name: string) => void
  onDeleteThread: (id: string) => void
}

export default function Sidebar({
  threads,
  activeThread,
  onSelectThread,
  onNewThread,
  onDeleteThread,
}: Props) {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <StatusDot />
        <span className={styles.appName}>Dobby</span>
      </div>

      <div className={styles.body}>
        <span className={styles.sectionLabel}>Threads</span>

        {threads.length === 0 ? (
          <div className={styles.empty}>no threads yet</div>
        ) : (
          threads.map((id) => (
            <ThreadItem
              key={id}
              id={id}
              isActive={id === activeThread}
              onClick={() => onSelectThread(id)}
              onDelete={() => onDeleteThread(id)}
            />
          ))
        )}
      </div>

      <NewThreadButton onConfirm={onNewThread} />
    </aside>
  )
}
