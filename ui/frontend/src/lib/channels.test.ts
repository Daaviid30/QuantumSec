import { capabilitiesFixture } from '../test/fixtures'
import { createChannelDraft, serializeChannels, validateChannels } from './channels'

test('channel configuration is serialized without UI-only identifiers', () => {
  const draft = createChannelDraft(capabilitiesFixture.channels[0], 42)
  draft.parameters.p = 0.17

  expect(serializeChannels([draft])).toEqual([{ type: 'depolarizing', p: 0.17 }])
})

test('channel validation uses server-provided parameter ranges', () => {
  const draft = createChannelDraft(capabilitiesFixture.channels[0], 1)
  draft.parameters.p = 1.2

  expect(validateChannels([draft], capabilitiesFixture.channels)).toMatch(/between 0 and 1/i)
})
