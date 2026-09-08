/**
 * Presentation of backend-emitted identifiers.
 *
 * Backend trace stages, states, and sources are lower-case snake_case identifiers. They must not be
 * rendered through CSS `text-transform: capitalize`, which uppercases only the first letter and so
 * corrupts domain vocabulary: `bb84` becomes "Bb84" and `qkd` becomes "Qkd". These helpers title-case
 * the words while preserving the canonical spelling of known acronyms and algorithm names.
 *
 * Only presentation changes here. The underlying backend facts are never rewritten.
 */

/** Canonical spellings, keyed by the lower-case token they replace. */
const CANONICAL_TOKENS: Record<string, string> = {
  bb84: 'BB84',
  b92: 'B92',
  e91: 'E91',
  bbm92: 'BBM92',
  qkd: 'QKD',
  pqc: 'PQC',
  qber: 'QBER',
  kem: 'KEM',
  hqc: 'HQC',
  aes: 'AES',
  gcm: 'GCM',
  hkdf: 'HKDF',
  hmac: 'HMAC',
  sha: 'SHA',
  dsa: 'DSA',
  ml: 'ML',
  rng: 'RNG',
  its: 'ITS',
  api: 'API',
  id: 'ID',
  a: 'A',
  b: 'B',
  x: 'X',
  z: 'Z',
}

function formatToken(token: string): string {
  if (!token) return token
  const canonical = CANONICAL_TOKENS[token.toLowerCase()]
  if (canonical) return canonical
  return token.charAt(0).toUpperCase() + token.slice(1)
}

/**
 * Render a snake_case backend identifier as a human label with canonical acronym spelling.
 *
 * `classical_authentication` -> `Classical authentication`
 * `bb84`                     -> `BB84`
 * `finished_b`               -> `Finished B`
 */
export function formatIdentifier(value: string): string {
  const tokens = value.split(/[\s_]+/).filter(Boolean)
  if (tokens.length === 0) return value
  return tokens
    .map((token, index) => {
      const canonical = CANONICAL_TOKENS[token.toLowerCase()]
      if (canonical) return canonical
      // Only the first word is capitalised; later words stay lower-case for sentence-style labels.
      return index === 0 ? formatToken(token) : token.toLowerCase()
    })
    .join(' ')
}

/**
 * Render a trace source (`session`, `qkd`, `pqc`, `hybrid`) with canonical acronym spelling.
 */
export function formatSource(value: string): string {
  return formatIdentifier(value)
}
