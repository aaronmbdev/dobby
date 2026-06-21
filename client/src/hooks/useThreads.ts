import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { listThreads, deleteThread } from '../api/threads'

export const THREADS_KEY = ['threads'] as const

export function useThreads() {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: THREADS_KEY,
    queryFn: listThreads,
  })

  const deleteMutation = useMutation({
    mutationFn: deleteThread,
    onMutate: async (threadId: string) => {
      await queryClient.cancelQueries({ queryKey: THREADS_KEY })
      const previous = queryClient.getQueryData<string[]>(THREADS_KEY)
      queryClient.setQueryData<string[]>(THREADS_KEY, (old) =>
        old ? old.filter((id) => id !== threadId) : [],
      )
      return { previous }
    },
    onError: (_err, _threadId, context) => {
      if (context?.previous) {
        queryClient.setQueryData(THREADS_KEY, context.previous)
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: THREADS_KEY })
    },
  })

  const addThreadToCache = (threadId: string) => {
    queryClient.setQueryData<string[]>(THREADS_KEY, (old) => {
      if (!old) return [threadId]
      if (old.includes(threadId)) return old
      return [...old, threadId]
    })
  }

  return {
    threads: query.data ?? [],
    isLoading: query.isLoading,
    isError: query.isError,
    deleteThread: deleteMutation.mutate,
    addThreadToCache,
  }
}
