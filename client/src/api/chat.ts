import { apiFetch } from './client'

export interface ChatMessage {
  role: string
  content: string
}

export interface ChatResponse {
  response: string
}

export interface HistoryResponse {
  thread_id: string
  messages: ChatMessage[]
}

export async function sendMessage(
  message: string,
  threadId: string,
): Promise<string> {
  const data = await apiFetch<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message, thread_id: threadId }),
  })
  return data.response
}

export async function getHistory(threadId: string): Promise<ChatMessage[]> {
  const data = await apiFetch<HistoryResponse>(
    `/api/chat/history?thread_id=${encodeURIComponent(threadId)}`,
  )
  return data.messages
}
