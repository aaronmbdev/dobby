import { useRef, useCallback } from 'react'
import styles from './ChatInput.module.css'

interface Props {
  onSend: (text: string) => void
  disabled: boolean
}

export default function ChatInput({ onSend, disabled }: Props) {
  const ref = useRef<HTMLTextAreaElement>(null)

  const resize = useCallback(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 150) + 'px'
  }, [])

  const submit = useCallback(() => {
    const el = ref.current
    if (!el) return
    const text = el.value.trim()
    if (!text || disabled) return
    onSend(text)
    el.value = ''
    el.style.height = 'auto'
  }, [onSend, disabled])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className={styles.area}>
      <div className={styles.row}>
        <span className={styles.prefix} aria-hidden="true">›</span>
        <textarea
          ref={ref}
          className={styles.input}
          rows={1}
          placeholder="say something…"
          autoComplete="off"
          spellCheck={false}
          disabled={disabled}
          onInput={resize}
          onKeyDown={handleKeyDown}
          aria-label="Message input"
        />
        <button
          className={styles.sendBtn}
          onClick={submit}
          disabled={disabled}
          aria-label="Send message"
          title="Send (Enter)"
        >
          <svg
            viewBox="0 0 16 16"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M14 2L8 8M14 2L10 14L8 8L2 6L14 2Z" />
          </svg>
        </button>
      </div>
      <p className={styles.hint}>enter — send · shift+enter — newline</p>
    </div>
  )
}
