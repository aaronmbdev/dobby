import styles from './UserMessage.module.css'

interface Props {
  content: string
}

export default function UserMessage({ content }: Props) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.bubble}>{content}</div>
    </div>
  )
}
