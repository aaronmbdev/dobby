import ThinkingIndicator from '../ThinkingIndicator/ThinkingIndicator'
import styles from './AIMessage.module.css'

interface Props {
  content: string
  isThinking?: boolean
}

export default function AIMessage({ content, isThinking }: Props) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.avatar} aria-hidden="true">D</div>
      <div className={styles.content}>
        {isThinking ? (
          <ThinkingIndicator />
        ) : (
          <div dangerouslySetInnerHTML={{ __html: content }} />
        )}
      </div>
    </div>
  )
}
