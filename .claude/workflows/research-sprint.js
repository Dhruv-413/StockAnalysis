export const meta = {
  name: 'research-sprint',
  description: 'Multi-front research sprint: parallel scouts per front, adversarial verification of key claims, evidence-graded synthesis',
  whenToUse: 'Researching tools, libraries, vendors, languages or methods for StockAnalysis. args = {question: string, fronts?: string[], constraints?: string}',
  phases: [
    { title: 'Scout', detail: 'one researcher per independent front' },
    { title: 'Verify', detail: 'skeptics try to refute decision-critical claims' },
    { title: 'Synthesize', detail: 'ranked recommendation + radar entries' },
  ],
}

const A = args || {}
const QUESTION = A.question || 'What new tools could make the StockAnalysis quick-response (fetch -> decide -> notify) system faster and more reliable?'
const CONSTRAINTS = A.constraints || 'Small team (1-3). US equities/ETFs. Data rights per docs/production-plan/04 §6. Evidence-first product; no live trading in MVP. Any language allowed if justified.'
const FRONTS = (A.fronts && A.fronts.length) ? A.fronts : [
  'languages and runtimes for low-latency event processing',
  'stream processing and incremental computation engines',
  'decision and rule engines with explainability',
  'market data, news and filings feeds and client libraries',
  'storage, messaging and fan-out to users',
  'tools and services released in the last 12 months',
]

const FINDINGS = {
  type: 'object',
  required: ['front', 'candidates'],
  properties: {
    front: { type: 'string' },
    candidates: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'what', 'relevance', 'license', 'latest_release', 'evidence_url', 'confidence', 'critical_claim'],
        properties: {
          name: { type: 'string' },
          what: { type: 'string' },
          relevance: { type: 'string' },
          license: { type: 'string' },
          data_rights_note: { type: 'string' },
          latest_release: { type: 'string' },
          perf_claim_and_method: { type: 'string' },
          cost: { type: 'string' },
          evidence_url: { type: 'string' },
          confidence: { type: 'string', enum: ['H', 'M', 'L'] },
          critical_claim: { type: 'string', description: 'the one claim the recommendation would depend on' },
        },
      },
    },
    unverified: { type: 'array', items: { type: 'string' } },
  },
}

const VERDICT = {
  type: 'object',
  required: ['refuted', 'reason'],
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string' }, source: { type: 'string' } },
}

log(`Question: ${QUESTION} | fronts: ${FRONTS.length}`)

const perFront = await pipeline(
  FRONTS,
  (front, _item, i) => agent(
    `Research front ${i + 1}: "${front}" for the question: ${QUESTION}\nConstraints: ${CONSTRAINTS}\n` +
    'Use WebSearch/WebFetch (load via ToolSearch if deferred). Primary sources only for versions, dates, licences and prices ' +
    '(registries such as PyPI JSON, crates.io, Maven Central and GitHub releases). ' +
    'Do NOT download, install or execute any package. ' +
    'Return 3-5 candidates, best first. Treat benchmarks and marketing as leads ' +
    'and record their methodology. Keep the software licence separate from data rights. Do not write files.',
    { label: `scout:${front}`, phase: 'Scout', schema: FINDINGS, agentType: 'tech-scout' }),
  async (res, front) => {
    if (!res) return null
    const MAX = 5
    if (res.candidates.length > MAX) log(`${front}: verifying top ${MAX} of ${res.candidates.length}; dropped: ${res.candidates.slice(MAX).map(c => c.name).join(', ')}`)
    const top = res.candidates.slice(0, MAX)
    const checked = await parallel(top.map(c => () =>
      parallel([1, 2].map(k => () => agent(
        `Skeptic ${k}: try to REFUTE this claim about ${c.name}: "${c.critical_claim}" (cited: ${c.evidence_url}). ` +
        'Check the primary source yourself. Default to refuted=true if you cannot confirm it.',
        { label: `verify:${c.name}#${k}`, phase: 'Verify', schema: VERDICT, effort: 'low' })))
        .then(vs => ({ ...c, verified: vs.filter(Boolean).filter(v => !v.refuted).length === 2,
          skeptic_notes: vs.filter(Boolean).map(v => v.reason) }))))
    return { front, candidates: checked.filter(Boolean), unverified: res.unverified || [] }
  },
)

const ok = perFront.filter(Boolean)
log(`Fronts completed: ${ok.length}/${FRONTS.length}`)

phase('Synthesize')
const report = await agent(
  `Synthesize a research-sprint report for: ${QUESTION}\nConstraints: ${CONSTRAINTS}\n` +
  `Findings (JSON): ${JSON.stringify(ok)}\n` +
  'Write markdown with these sections: 1) decision question; 2) recommendation with a latency/complexity tier; ' +
  '3) comparison table (name, front, relevance, licence, latest release, verified yes/no, confidence, URL); ' +
  '4) tech-radar entries (Adopt/Trial/Assess/Hold) with a one-line reason each; 5) what would change the answer; ' +
  '6) unverified or refuted claims. Mark unverified candidates clearly. Do not invent sources.',
  { label: 'synthesis' })

return { report, fronts: ok.length }
