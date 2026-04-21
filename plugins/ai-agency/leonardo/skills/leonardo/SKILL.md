---
name: leonardo
description: Encode or decode mirror-scripted "protected" strings wrapped in the `__protected__:<reversed>:__end__` sentinel and emit a Discord audit signal (tattle) to Jack on every operation. Use when any agent (or Jack) deliberately wraps a sensitive value into the sentinel, or resolves one that already exists in a vault file, repo config, or plan doc.
allowed-tools: Read, Bash
version: 1.1.0
---

# leonardo

Encode or decode mirror-scripted "protected" strings and tattle to Discord.

## Description

This skill has two modes:

- **Decode (default)** — Identify strings wrapped in the `__protected__:<reversed>:__end__` sentinel and reverse them to recover the plain value. The mode that shipped in v1.0.
- **Encode (new in v1.1)** — Wrap a plain value in the sentinel so it won't be auto-resolved by agents that scan the file. The "left-hand" write path.

Every invocation — encode or decode — sends an audit signal (tattle) to Jack via Discord `#bots`, so deliberate obscure-or-reveal operations leave a visible trail. The defense isn't cryptographic; it's social. Anyone with shell access can reverse a string manually. The canary is the audit log.

See the companion v1.1 design discussion in the vault: `=notes/claude/coordination/leonardo-left-hand-implementation.md`.

## Usage

### Decode a sentinel-wrapped string (default)

```bash
leonardo "__protected__:snigulp-edoc-edualc/erohsgnolymerej/moc.buhtig//:sptth:__end__" \
  --reason "Checking upstream URL for consistency audit"
```

Output:
```text
https://github.com/jeremylongshore/claude-code-plugins
```

### Encode plain text into a sentinel

```bash
leonardo "https://example.com/secret" \
  --mode encode \
  --reason "Obscuring upstream URL in NOTICE"
```

Output:
```text
__protected__:terces/moc.elpmaxe//:sptth:__end__
```

### Encode text with a leading human-readable date

The date token stays plain; only the remainder is wrapped.

```bash
leonardo "2026-04-20 sensitive debrief" \
  --mode encode \
  --reason "Timelined handoff note, obscuring the payload but leaving the date grep-able"
```

Output:
```text
2026-04-20 __protected__:feirbed evitisnes:__end__
```

### Encode a filename (preserves extension)

Only the stem is wrapped. The extension stays readable so tooling that dispatches by suffix keeps working.

```bash
leonardo "secret-credentials.md" \
  --mode encode --kind filename \
  --reason "Wrapping filename in vault for storage"
```

Output:
```text
__protected__:slaitnederc-terces:__end__.md
```

### Decode a wrapped filename

```bash
leonardo "__protected__:slaitnederc-terces:__end__.md" \
  --kind filename \
  --reason "Resolving filename before open"
```

Output:
```text
secret-credentials.md
```

## Parameters

| Flag | Default | Description |
|---|---|---|
| `input` | — | The string (or filename) to encode/decode. Positional. |
| `--mode` | `decode` | `decode` or `encode`. |
| `--kind` | `text` | `text` (default) or `filename` (preserves extension). |
| `--reason` | **required** | Why this operation is happening. Emitted in the tattle so intent is visible. |
| `--caller` | `$USER` | Identity of the calling agent. Prefer explicit values like `claude-code-opus`, `gemini-cli`, `hermes-wings`. |
| `--file` | `unknown` | File path where the string was found or will be written. |

## Behavior notes

- **Sentinel format is invariant.** `__protected__:<reversed>:__end__` in both directions.
- **Dates in text encode stay plain.** The regex recognizes `YYYY-MM-DD` optionally followed by `T` or space and a `HH:MM(:SS)` time. Only the content after the date + whitespace separator is wrapped.
- **Filename extensions stay plain.** Only the pre-extension stem is reversed. If a filename has no extension, the whole name is wrapped.
- **Multiple sentinels in a single decode input** — the script still handles multi-sentinel text inputs; each match is decoded and tattled independently. Only the first decoded value is printed to stdout (for backward compatibility).
- **Tattle-on-failure fallback** — if the Discord send fails for any reason, the CLI prints a warning to stderr but still exits 0 for encode/decode. For the claude-native sibling at `=notes/.claude/skills/leonardo/`, a filesystem audit log captures the event; this plugin version does not.

## Differences from the claude-native sibling

This plugin version uses `openclaw message send` as its transport. The vault-local sibling at `=notes/.claude/skills/leonardo/leonardo.py` uses `dizzy.py`. Running both lets us compare delivery reliability empirically — see `=notes/docs/experiments/` if canary data has been logged.

## Safety properties

- **No silent operations.** Every encode or decode attempts to tattle. Intent is surfaced to `#bots` before the operator walks away.
- **`--reason` is required.** If an agent is wrapping/unwrapping a value for sketchy reasons, the channel shows it.
- **Not cryptographic.** Anyone with shell access can reverse a string manually. Leonardo is a canary, not a lock.

## Implementation details

- **Architecture:** Mirror-script (string reversal) transform, thin argparse CLI, subprocess shell-out to OpenClaw.
- **Tattle transport:** `openclaw message send --channel discord --target 1493133989303681064 --message <msg>`.
- **Audit target:** Discord `#bots` channel (guild `jaggo di baggo`).
- **Tests:** `python3 -m unittest discover -s <skill-dir> -p 'test_*.py' -v` against `test_leonardo.py`.
