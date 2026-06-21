import DOMPurify from 'dompurify'

// Tags and attributes produced by our own renderer — nothing more is allowed.
const PURIFY_CONFIG: DOMPurify.Config = {
  ALLOWED_TAGS: [
    'p', 'br', 'strong', 'em', 'code', 'pre',
    'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'hr',
  ],
  ALLOWED_ATTR: [],
}

export function renderMarkdown(raw: string): string {
  let t = raw
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // Code blocks (must come before inline code)
  t = t.replace(/```(?:\w+)?\n?([\s\S]*?)```/g, (_match, code: string) =>
    `<pre><code>${code.trimEnd()}</code></pre>`,
  )

  // Inline code
  t = t.replace(/`([^`\n]+)`/g, '<code>$1</code>')

  // Bold
  t = t.replace(/\*\*(.+?)\*\*/gs, '<strong>$1</strong>')

  // Italic
  t = t.replace(/\*(.+?)\*/gs, '<em>$1</em>')

  // Headings
  t = t.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  t = t.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  t = t.replace(/^# (.+)$/gm, '<h1>$1</h1>')

  // Horizontal rule
  t = t.replace(/^---$/gm, '<hr>')

  // List items
  t = t.replace(/^[*-] (.+)$/gm, '<li>$1</li>')
  t = t.replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`)

  // Paragraphs
  const BLOCK = /^<(h[1-6]|ul|ol|pre|hr)/
  t = t
    .split(/\n{2,}/)
    .map((chunk) => {
      chunk = chunk.trim()
      if (!chunk || BLOCK.test(chunk)) return chunk
      return `<p>${chunk.replace(/\n/g, '<br>')}</p>`
    })
    .filter(Boolean)
    .join('\n')

  return DOMPurify.sanitize(t, PURIFY_CONFIG)
}
