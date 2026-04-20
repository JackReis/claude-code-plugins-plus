# autonomous-ai-agents

Fleet-identity lookup for Jack Reis's autonomous AI agent fleet.

## What it does

Exposes a single Claude Code skill — `fleet-identity` — that answers "who is X?" for the agent fleet without duplicating data.

Canonical mapping lives at `~/Documents/Coordination/<date>-identity-mapping.md`. The skill reads from there (or a vault mirror as fallback) and returns semantic intent pairs:

- Hermes → Wings (Discord)
- Zolivier → Zoe (Discord)
- KimiClaw → Mara (Discord) / Kopi (Telegram)

Runtime agents vs. platform surfaces: Hermes and Zolivier are local runtimes (Hermes Agent by Nous Research, OpenClaw gateway respectively). Wings, Zoe, Mara, Kopi are the Discord/Telegram bot accounts that relay to/from them. KimiClaw is cloud OpenClaw. Dizzy is a separate Claude-Code-session primitive and is intentionally not in this mapping.

## Install

From the `jack-plugins` marketplace (Jack's fork of claude-code-plugins-plus, registered as a distinct marketplace to avoid name collision with Jeremy Longshore's upstream):

```
/plugin install autonomous-ai-agents@jack-plugins
```

Or load from a local path during development:

```
/plugin install path:/Users/jack.reis/Documents/claude-code-plugins-plus/plugins/ai-agency/autonomous-ai-agents
```

The `jack-plugins` marketplace is registered in `~/.claude/settings.json` under `extraKnownMarketplaces` and points at `github:JackReis/claude-code-plugins-plus`.

## Usage

Trigger phrases:

- "Who is Wings?" / "Who runs Kopi?" / "What agent is Zoe?"
- "Fleet identity" / "fleet mapping" / "agent mapping" / "identity map"
- "Autonomous ai agent"

The skill finds the latest `*-identity-mapping.md` in `~/Documents/Coordination/` and returns the relevant rows.

## Data source

The plugin **does not bundle** the mapping. It points at the canonical file Jack maintains in his Documents/Coordination folder so there's exactly one source of truth.

Updating the mapping (e.g., adding a new agent:surface pair): edit `~/Documents/Coordination/<today>-identity-mapping.md` directly. The skill picks up changes on next invocation — no plugin reinstall.

If `~/Documents/Coordination/` is missing or empty, the skill falls back to the vault mirror at `=notes/inbox/agent-coordination.md`.

## Roadmap

- **v0.1** (this release) — `fleet-identity` skill only.
- **v0.2** (planned) — Hermes MCP integration: wire the Nous Research Hermes Agent multi-platform gateway as an MCP server so Claude Code can delegate tasks directly to Hermes, parallel to the existing OpenClaw MCP wiring for Zolivier. Scoped in a separate `/superplan` (see `docs/plans/2026-04-21-autonomous-ai-agent-Hermes-MCP.md` in the vault when that superplan ships).

## Related

- OpenClaw MCP (already wired in Jack's Claude Code config, 2026-04-19) — handles Zolivier-side delegation.
- `dizzy.py` IDENTITIES (in `=notes/claude/scripts/`) — Discord routing primitive (tokens, channels). Different concern from semantic identity.
- Hermes Agent: <https://hermes-agent.nousresearch.com/>

## License

MIT — see LICENSE.
