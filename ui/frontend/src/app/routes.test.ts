import { viewFromHash } from './routes'

test('hash navigation accepts only known product views', () => {
  expect(viewFromHash('#/laboratory')).toBe('laboratory')
  expect(viewFromHash('#runs')).toBe('runs')
  expect(viewFromHash('#/unknown')).toBe('overview')
})
