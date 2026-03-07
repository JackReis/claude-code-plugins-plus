---
name: skill-adapter
description: |
  Analyzes existing plugins to extract their capabilities, then adapts and applies those skills to the current task. Acts as a universal skill chameleon that learns from other plugins. Activates when you request "skill adapter" functionality.
allowed-tools: Read, Grep, Glob, Bash, Skill
version: 2.0.0
---

# Pi-Pathfinder — Plugin Router

You are a plugin router. Your job: find the best installed plugin for the user's task and invoke it.

## Step 1: Load the Index

Read the plugin index file located next to this skill's scripts:

```
~/.claude/plugins/cache/claude-code-plugins-plus/pi-pathfinder/*/skills/pi-pathfinder/scripts/plugin-index.json
```

If the file is missing, build it first:

```bash
python3 ~/.claude/plugins/cache/claude-code-plugins-plus/pi-pathfinder/*/skills/pi-pathfinder/scripts/build_index.py
```

Then read the generated `plugin-index.json`.

**Staleness check:** If `built_at` is more than 24 hours ago, rebuild the index by running the build script above.

## Step 2: Match User Intent

Extract 2-5 keywords from the user's request. For each plugin in the index, score it:

| Match type | Points |
|------------|--------|
| Exact keyword in plugin `keywords` array (case-insensitive) | 3 |
| Substring match in plugin `description` (case-insensitive) | 2 |
| Substring match in any skill `description` (case-insensitive) | 1 |

Sum all points per plugin. A keyword can score in multiple categories for the same plugin.

## Step 3: Route

**Clear winner (top score > 4, and > 2 points ahead of #2):**
- Announce: "Routing to **[plugin-name]**: [description]"
- Invoke: `Skill(skill: "[skill_path]")`
- Use the `skill_path` from the index (format: `plugin-name:skill-name`)

**Ambiguous (top 2-3 within 2 points of each other):**
- Present the top matches with scores and one-line descriptions
- Ask the user to pick
- Invoke their choice

**No match (all scores <= 1):**
- Say: "No installed plugin closely matches this task."
- List the 3 closest matches anyway in case one is relevant
- Suggest the user describe their task differently or install relevant plugins

## Step 4: Fallback

If the invoked skill doesn't solve the problem or the user says it's wrong:
- Offer the next-ranked match from Step 2
- If no more viable matches, say so

## Rules

- NEVER skip the index. Always search it first.
- NEVER guess a skill path. Only use `skill_path` values from the index.
- NEVER invoke pi-pathfinder itself (the index excludes it, but guard against it).
- If the index is empty, tell the user to install plugins first.
- If multiple skills exist within the winning plugin, pick the one whose `description` best matches the user's intent.
