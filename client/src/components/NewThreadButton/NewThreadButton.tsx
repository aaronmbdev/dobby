import { useState, useRef, useEffect } from 'react'
import styles from './NewThreadButton.module.css'

interface Props {
  onConfirm: (name: string) => void
}

export default function NewThreadButton({ onConfirm }: Props) {
  const [isEditing, setIsEditing] = useState(false)
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isEditing])

  const commit = () => {
    const trimmed = value.trim()
    setIsEditing(false)
    setValue('')
    if (trimmed) onConfirm(trimmed)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      commit()
    }
    if (e.key === 'Escape') {
      setIsEditing(false)
      setValue('')
    }
  }

  if (isEditing) {
    return (
      <div className={styles.row}>
        <span className={styles.prefix}>›</span>
        <input
          ref={inputRef}
          className={styles.input}
          type="text"
          placeholder="thread name"
          autoComplete="off"
          spellCheck={false}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={commit}
        />
      </div>
    )
  }

  return (
    <button className={styles.btn} onClick={() => setIsEditing(true)}>
      <svg
        viewBox="0 0 12 12"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      >
        <path d="M6 1v10M1 6h10" />
      </svg>
      new thread
    </button>
  )
}
