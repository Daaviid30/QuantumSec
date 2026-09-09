import { formatIdentifier, formatSource, formatTechnicalText } from './labels'

test('canonical protocol and domain acronyms survive label formatting', () => {
  expect(formatIdentifier('bb84')).toBe('BB84')
  expect(formatSource('qkd')).toBe('QKD')
  expect(formatSource('pqc')).toBe('PQC')
  expect(formatSource('hybrid')).toBe('Hybrid')
})

test('snake_case backend identifiers become sentence-style labels', () => {
  expect(formatIdentifier('classical_authentication')).toBe('Classical authentication')
  expect(formatIdentifier('assumed_not_executed')).toBe('Assumed not executed')
  expect(formatIdentifier('server_offer_authentication')).toBe('Server offer authentication')
  expect(formatIdentifier('key_release')).toBe('Key release')
  expect(formatIdentifier('qkd_bitstring')).toBe('QKD bitstring')
})

test('single-letter role suffixes stay upper-case', () => {
  expect(formatIdentifier('finished_a')).toBe('Finished A')
  expect(formatIdentifier('finished_b')).toBe('Finished B')
  expect(formatIdentifier('ml_dsa_65')).toBe('ML-DSA-65')
  expect(formatIdentifier('wegman_carter')).toBe('Wegman–Carter')
})

test('normalizes embedded technical identifiers without rewriting surrounding prose', () => {
  expect(formatTechnicalText('QKD classical authentication: ml_dsa_65')).toBe(
    'QKD classical authentication: ML-DSA-65',
  )
  expect(formatTechnicalText('Executed intercept_resend after BB84')).toBe(
    'Executed Intercept-resend after BB84',
  )
})
