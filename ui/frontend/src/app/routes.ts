export type AppView = 'overview' | 'laboratory' | 'runs' | 'compare'

const views = new Set<AppView>(['overview', 'laboratory', 'runs', 'compare'])

export function viewFromHash(hash: string): AppView {
  const candidate = hash.replace(/^#\/?/, '') as AppView
  return views.has(candidate) ? candidate : 'overview'
}

export const viewTitles: Record<AppView, { eyebrow: string; title: string }> = {
  overview: { eyebrow: 'Research workspace', title: 'Overview' },
  laboratory: { eyebrow: 'Configure · Run · Observe', title: 'Laboratory' },
  runs: { eyebrow: 'Reproducible evidence', title: 'Runs' },
  compare: { eyebrow: 'Two-record analysis', title: 'Compare' },
}
