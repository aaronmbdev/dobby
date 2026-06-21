import { useEffect, useRef } from 'react'
import { type Message } from '../../hooks/useChat'
import AIMessage from '../AIMessage/AIMessage'
import UserMessage from '../UserMessage/UserMessage'
import EmptyState from '../EmptyState/EmptyState'
import styles from './MessageList.module.css'

interface Props {
  messages: Message[]
  emptyLabel: string
}

export default function MessageList({ messages, emptyLabel }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className={styles.list}>
      {messages.length === 0 ? (
        <EmptyState label={emptyLabel} />
      ) : (
        messages.map((msg) => {
          if (msg.role === 'user') {
            return <UserMessage key={msg.id} content={msg.content} />
          }
          if (msg.role === 'thinking') {
            return <AIMessage key={msg.id} content="" isThinking />
          }
          if (msg.role === 'error') {
            return (
              <div key={msg.id} className={styles.error}>
                ⚠&nbsp;&nbsp;{msg.content}
              </div>
            )
          }
          return <AIMessage key={msg.id} content={msg.content} />
        })
      )}
      <div ref={bottomRef} />
    </div>
  )
}
