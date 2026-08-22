import type {
  ChannelCapability,
  ChannelConfiguration,
  ChannelDraft,
} from '../types/api'

export function createChannelDraft(capability: ChannelCapability, id: number): ChannelDraft {
  return {
    id,
    type: capability.id,
    parameters: Object.fromEntries(
      capability.parameters.map((parameter) => [parameter.key, parameter.default]),
    ),
  }
}

export function serializeChannels(channels: ChannelDraft[]): ChannelConfiguration[] {
  return channels.map(({ type, parameters }) => ({ type, ...parameters }))
}

export function validateChannels(
  channels: ChannelDraft[],
  capabilities: ChannelCapability[],
): string | null {
  for (const channel of channels) {
    const capability = capabilities.find((candidate) => candidate.id === channel.type)
    if (!capability?.implemented) {
      return `Channel ${channel.type} is not available.`
    }

    for (const parameter of capability.parameters) {
      const value = channel.parameters[parameter.key]
      if (!Number.isFinite(value) || value < parameter.minimum || value > parameter.maximum) {
        return `${parameter.label} must be between ${parameter.minimum} and ${parameter.maximum}.`
      }
    }

    if (
      channel.type === 'pauli' &&
      (channel.parameters.px ?? 0) +
        (channel.parameters.py ?? 0) +
        (channel.parameters.pz ?? 0) >
        1
    ) {
      return 'Pauli probabilities must add up to 1 or less.'
    }
  }

  return null
}
