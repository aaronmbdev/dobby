import { useState, useCallback } from 'react'
import { sendMessage, getHistory } from '../api/chat'
import { renderMarkdown } from '../utils/markdown'

export type MessageRole = 'user' | 'assistant' | 'thinking' | 'error'

export interface Message {
  id: string
  role: MessageRole
  content: string
}

let idCounter = 0
function nextId(): string {
  return String(++idCounter)
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const clearMessages = useCallback(() => {
    setMessages([])
  }, [])

  const loadHistory = useCallback(async (threadId: string) => {
    setMessages([])
    try {
      const history = await getHistory(threadId)
      if (history.length === 0) return
      setMessages(
        history.map((msg) => ({
          id: nextId(),
          role: msg.role === 'user' ? 'user' : 'assistant',
          content:
            msg.role === 'assistant'
              ? renderMarkdown(msg.content)
              : msg.content,
        })),
      )
    } catch {
      setMessages([
        {
          id: nextId(),
          role: 'error',
          content: 'could not load history',
        },
      ])
    }
  }, [])

  const send = useCallback(async (text: string, threadId: string) => {
    if (!text.trim() || !threadId) return

    const thinkingId = nextId()

    setMessages((prev) => [
      ...prev,
      { id: nextId(), role: 'user', content: text },
      { id: thinkingId, role: 'thinking', content: '' },
    ])
    setIsLoading(true)

    try {
      const response = await sendMessage(text, threadId)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === thinkingId
            ? { id: msg.id, role: 'assistant', content: renderMarkdown(response) }
            : msg,
        ),
      )
    } catch (err) {
      const errorMsg =
        err instanceof Error ? err.message : 'Could not reach the server.'
      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== thinkingId)
          .concat({ id: nextId(), role: 'error', content: errorMsg }),
      )
    } finally {
      setIsLoading(false)
    }
  }, [])

  return {
    messages,
    isLoading,
    sendMessage: send,
    loadHistory,
    clearMessages,
  }
}
