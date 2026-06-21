import { useState, useCallback } from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import ChatHeader from '../../components/ChatHeader/ChatHeader'
import MessageList from '../../components/MessageList/MessageList'
import ChatInput from '../../components/ChatInput/ChatInput'
import ConfirmDialog from '../../components/ConfirmDialog/ConfirmDialog'
import { useThreads } from '../../hooks/useThreads'
import { useChat } from '../../hooks/useChat'
import styles from './ChatPage.module.css'

export default function ChatPage() {
  const [activeThread, setActiveThread] = useState<string | null>(null)
  const [showThreads, setShowThreads] = useState(true)
  const [confirmThread, setConfirmThread] = useState<string | null>(null)

  const { threads, deleteThread, addThreadToCache } = useThreads()
  const { messages, isLoading, sendMessage, loadHistory, clearMessages } = useChat()

  const handleSelectThread = useCallback(
    (id: string) => {
      if (id === activeThread) {
        setShowThreads(false)
        return
      }
      setActiveThread(id)
      setShowThreads(false)
      loadHistory(id)
    },
    [activeThread, loadHistory],
  )

  const handleNewThread = useCallback(
    (name: string) => {
      addThreadToCache(name)
      setActiveThread(name)
      setShowThreads(false)
      clearMessages()
    },
    [addThreadToCache, clearMessages],
  )

  const handleDeleteRequest = useCallback((id: string) => {
    setConfirmThread(id)
  }, [])

  const handleDeleteConfirm = useCallback(() => {
    if (!confirmThread) return
    deleteThread(confirmThread)
    if (confirmThread === activeThread) {
      setActiveThread(null)
      clearMessages()
      setShowThreads(true)
    }
    setConfirmThread(null)
  }, [confirmThread, activeThread, deleteThread, clearMessages])

  const handleSend = useCallback(
    (text: string) => {
      if (!activeThread) return
      addThreadToCache(activeThread)
      sendMessage(text, activeThread)
    },
    [activeThread, addThreadToCache, sendMessage],
  )

  const emptyLabel = activeThread ? 'say something…' : 'select a thread'

  return (
    <div className={styles.app}>
      {/* Sidebar — always rendered on desktop; shown/hidden on mobile */}
      <div className={`${styles.sidebarWrapper} ${showThreads ? styles.sidebarVisible : ''}`}>
        <Sidebar
          threads={threads}
          activeThread={activeThread}
          onSelectThread={handleSelectThread}
          onNewThread={handleNewThread}
          onDeleteThread={handleDeleteRequest}
        />
      </div>

      {/* Main chat — hidden on mobile when thread list is showing */}
      <div className={`${styles.main} ${showThreads ? styles.mainHidden : ''}`}>
        <ChatHeader
          activeThread={activeThread}
          onShowThreads={() => setShowThreads(true)}
        />
        <MessageList messages={messages} emptyLabel={emptyLabel} />
        <ChatInput onSend={handleSend} disabled={isLoading || !activeThread} />
      </div>

      {confirmThread && (
        <ConfirmDialog
          threadId={confirmThread}
          onConfirm={handleDeleteConfirm}
          onCancel={() => setConfirmThread(null)}
        />
      )}
    </div>
  )
}
