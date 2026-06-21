import { apiFetch } from './client'

export interface ThreadsResponse {
  threads: string[]
}

export async function listThreads(): Promise<string[]> {
  const data = await apiFetch<ThreadsResponse>('/api/threads')
  return data.threads
}

export async function deleteThread(threadId: string): Promise<void> {
  await apiFetch<void>(`/api/threads/${encodeURIComponent(threadId)}`, {
    method: 'DELETE',
  })
}
