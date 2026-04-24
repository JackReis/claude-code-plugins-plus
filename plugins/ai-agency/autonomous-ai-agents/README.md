# autonomous-ai-agents

Fleet-coordination plugin for Jack Reis's autonomous AI agent fleet. Lets Claude Code answer "who is X?" across the fleet's Discord/Telegram surfaces, and — as of v0.3 — reach BOTH messaging bridges (Wings via Hermes, Zoe via OpenClaw) as native MCP servers.

## What's new in v0.3

- **OpenClaw messaging bridge** — native `openclaw mcp serve` wired as the `openclaw` MCP server, exposing 9 tools for reading/sending messages through Zolivier (Zoe) on Discord, Telegram, and Slack.
- **`openclaw-bridge` companion skill** — documents the 9-tool surface, the decision matrix for choosing Wings vs Zoe vs `telegram-messaging` vs `dizzy.py`, AND the **Klawz Kimi enterprise room security boundaries** (insecure relay — no secrets, no PII, no absolute filesystem paths in outbound messages).
- **Plugin now owns both halves of the messaging substrate** — Wings (v0.2) + Zoe (v0.3). Together they cover the thinker fleet's full async-messaging surface.

## Fleet topology

This plugin wires Claude Code into a fleet that spans **runtimes**, **surfaces**, and **rooms**:

```
Thinkers (deep-work runtimes)        Messaging substrate         Surfaces
─────────────────────────────       ──────────────────         ─────────────
Claude Code  ──┐                     Wings (Hermes)             Discord
Gemini CLI   ──┼─►  pick up via ─►   Zoe   (Zolivier) ──►       Telegram
ChatGPT      ──┘                                                Slack/WA/Sig

                                                                Klawz (Kimi
                                                                multi-agent
                                                                room)
                                                                — insecure
                                                                  relay,
                                                                  no secrets
```

- **Thinkers** are heavy runtimes that lose context across session boundaries.
- **Wings** (Hermes Agent) and **Zoe** (Zolivier/OpenClaw) are the messaging substrate. They queue inbound messages for thinkers and route outbound replies. v0.2 ships Wings; v0.3 ships Zoe.
- **Klawz** is a Kimi enterprise multi-agent room with four participants (three KimiClaw instances + Zolivier). Classified as insecure-relay + dev-scratchpad. Zolivier participates, so any `mcp__openclaw__messages_send` whose destination fans out into Klawz must obey the Klawz hard rules. The `openclaw-bridge` skill encodes those rules.
- **Other surfaces** (Mara on Discord, Kopi on Telegram, Neo on Discord, Codex on Discord) are managed by their respective runtimes (KimiClaw, PT/Gemini CLI, GPT-5 Codex) and are out of this plugin's scope. Use the `fleet-identity` skill to look up which runtime is behind any surface.

Source of truth for the identity mapping: `~/Documents/Coordination/*-identity-mapping.md` (latest-modified wins). Klawz security SoT: `~/Documents/Coordination/2026-04-23-klawz-kimi-group-addendum.md`.

## What's new in v0.2

- **Hermes messaging bridge** — native `hermes mcp serve` wired as the `hermes` MCP server, exposing 10 tools for reading/sending messages across Telegram, Discord, Slack, WhatsApp, Signal, and Matrix surfaces.
- **`hermes-bridge` companion skill** — documents when/how to use the bridge and when to fall back to the `hermes-cli` skill for one-shot delegation.
- **No Python shim** — uses Hermes's built-in MCP server directly.

Mental model: Wings (Hermes) and Zoe (Zolivier) are the fleet's shared async-messaging substrate. Heads-down thinkers (Claude Code, Gemini CLI, ChatGPT) come back to them to catch up across session boundaries. This plugin wires Claude Code's side of Wings; a v0.3 follow-on is expected to wire Zolivier/Zoe via OpenClaw.

## What it does (v0.1 carry-over)

Ships the `fleet-identity` skill — answers "who is X?" for the fleet without duplicating data.

Canonical mapping lives at `~/Documents/Coordination/<date>-identity-mapping.md`. The skill reads from there (or a vault mirror as fallback) and returns semantic intent pairs:

- Hermes → Wings (Discord)
- Zolivier → Zoe (Discord)
- KimiClaw → Mara (Discord) / Kopi (Telegram)

Runtime agents vs. platform surfaces: Hermes and Zolivier are local runtimes (Hermes Agent by Nous Research, OpenClaw gateway respectively). Wings / Zoe / Mara / Kopi are the Discord/Telegram bot accounts that relay to/from them. KimiClaw is cloud OpenClaw. Dizzy is a separate Claude-Code-session primitive and is intentionally not in this mapping.

## Install

From the `dancer` marketplace:

```
/plugin install autonomous-ai-agents@dancer
```

The marketplace lives at `github:JackReis/dancer` (mirror at `gitlab:jackrei/dancer`). Register in `~/.claude/settings.json` under `extraKnownMarketplaces`.

Or load from a local path during development:

```
/plugin install path:/Users/jack.reis/Documents/dancer/plugins/ai-agency/autonomous-ai-agents
```

## Hermes MCP setup

Prerequisites:

- Hermes Agent installed (<https://hermes-agent.nousresearch.com>).
- `hermes` binary on PATH (`which hermes` should resolve).

When the plugin is enabled, the `hermes` MCP server auto-activates via `plugin.json`'s `mcpServers` block. Tool calls resolve to `mcp__hermes__<tool_name>`.

For vault-scoped wiring independent of plugin state, add an equivalent entry to your project `.mcp.json`:

```json
{
  "mcpServers": {
    "hermes": {
      "type": "stdio",
      "command": "hermes",
      "args": ["mcp", "serve"]
    }
  }
}
```

## OpenClaw MCP setup

Prerequisites:

- OpenClaw installed (`brew install openclaw` — current v2026.4.23+).
- Gateway running. On macOS, `ai.openclaw.gateway` launchd plist; verify via `launchctl list | grep openclaw`.
- `openclaw` binary on PATH (`which openclaw` should resolve).

When the plugin is enabled, the `openclaw` MCP server auto-activates via `plugin.json`'s `mcpServers` block. Tool calls resolve to `mcp__openclaw__<tool_name>`.

For vault-scoped wiring independent of plugin state, add to your project `.mcp.json`:

```json
{
  "mcpServers": {
    "openclaw": {
      "type": "stdio",
      "command": "openclaw",
      "args": ["mcp", "serve"]
    }
  }
}
```

The OpenClaw gateway needs credentials (Mistral API key, OpenAI API key for some routes) — keep them in `~/.secrets/openclaw-env.env` and source from the launchd plist (NOT from the plugin manifest, NOT from `.mcp.json`).

## Usage

### fleet-identity trigger phrases

- "Who is Wings?" / "Who runs Kopi?" / "What agent is Zoe?"
- "Fleet identity" / "fleet mapping" / "agent mapping" / "identity map"
- "Autonomous ai agent"

The skill finds the latest `*-identity-mapping.md` in `~/Documents/Coordination/` and returns the relevant rows.

### hermes-bridge trigger phrases

- "Check hermes" / "catch me up" / "what came in while I was working"
- "Any pending approvals" / "what's on telegram" / "reply via hermes"
- "Wings says" / "messages waiting"

The skill polls Hermes's event queue, reads/sends messages, and approves/denies pending tool calls. See `skills/hermes-bridge/SKILL.md` for the 10-tool surface and procedures.

### openclaw-bridge trigger phrases

- "Check zoe" / "what did zoe say" / "ask zoe" / "zoe handoff"
- "Openclaw message" / "openclaw events" / "any pending openclaw approvals"
- "Klawz room" / "what's in #bots" / "reply via zoe"
- "Send through zolivier" / "openclaw bridge"

The skill polls OpenClaw's event queue, reads/sends messages through Zolivier, approves/denies pending tool calls, AND encodes the Klawz Kimi enterprise room security boundaries (no secrets / no PII / no absolute paths) for any send that fans out into the multi-agent room. See `skills/openclaw-bridge/SKILL.md` for the 9-tool surface, fleet topology diagram, and the Klawz hard-rules block.

## Data source

The plugin **does not bundle** the fleet mapping. It points at the canonical file Jack maintains in `~/Documents/Coordination/` so there's exactly one source of truth. Edit `~/Documents/Coordination/<today>-identity-mapping.md` directly to update; the skill picks up changes on next invocation.

If `~/Documents/Coordination/` is missing or empty, the skill falls back to the vault mirror at `=notes/inbox/agent-coordination.md`.

## Roadmap

- **v0.1** (shipped 2026-04-20) — `fleet-identity` skill.
- **v0.2** (shipped 2026-04-24) — Hermes MCP messaging bridge + `hermes-bridge` skill. Plan: `=notes/docs/plans/2026-04-24-autonomous-ai-agent-Hermes-MCP-impl.md`.
- **v0.3** (this release, 2026-04-24) — OpenClaw/Zolivier MCP messaging bridge + `openclaw-bridge` skill (with Klawz security disclosure). Plan: `=notes/docs/plans/2026-04-24-autonomous-ai-agent-OpenClaw-MCP-impl.md`.
- **v0.4** (planned) — TBD; candidates: programmatic Klawz room posting tool, additional surfaces, deeper Tipi intent integration.

## Related

- Sibling skill `hermes-cli` (in `=notes/.claude/skills/hermes-cli/`) — TTY one-shot delegation via `hermes chat -Q -q`. Complementary to `hermes-bridge`.
- Sibling skill `telegram-messaging` (in `=notes/.claude/skills/telegram-messaging/`) — preferred for single-Jack DMs per user pref. Complementary to `openclaw-bridge`.
- `dizzy.py` IDENTITIES (in `=notes/claude/scripts/`) — Discord routing primitive (tokens, channels). Different concern from semantic identity.
- Klawz security SoT: `~/Documents/Coordination/2026-04-23-klawz-kimi-group-addendum.md`.
- Hermes Agent: <https://hermes-agent.nousresearch.com/>
- OpenClaw: `brew install openclaw`

## License

MIT — see LICENSE.
