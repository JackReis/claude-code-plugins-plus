# Dancer — Agent-to-Agent Learning Engine

> **Status:** Vision document. Not a specification. Captured 2026-05-02 from a working session where the observer principle, the "you are not alone in this codebase" cue, and the *unexamined code is not worth running* aphorism converged into a single product frame.
>
> Captured here because, per the observer principle that motivates this whole project, an unwritten vision is superposition that vanishes at session end.

## The throughline

`dancer` is the publishable Claude Code plugin marketplace, modeled on Matt Pocock's TypeScript-skills ecosystem. It already has the infrastructure (forked from upstream MIT, renamed 2026-04-20, hosting Jack-authored skills alongside the upstream catalog).

The next layer is the *agent-to-agent learning engine* — the thing that turns a marketplace of skills into a working distributed cognition system.

## What the engine does

Extend the `grill-me` skill from a single-session interview into a full ecosystem-tightening loop: organization, refinement, clarification, instrumentation, visibility. The current `grill-me` interviews the user. The engine generalizes that pattern so agents grill *each other*.

Specialization by aptitude, not role:

- **The strongest architects explain the engineering needs.** When a domain has unclear requirements or ambiguous scope, an architect-flavored agent (Opus, Gemini Pro, GPT-Pro) is dispatched to draft the spec and stress-test it. Other agents grill it.
- **The gifted linguists write the notes and logs.** Sonnet, Haiku, smaller fast models — high-volume, accurate, fast turnaround. They produce the durable artifacts (handoff files, transcripts, summaries) that make the architects' work measurable to the next observer.
- **The observers watch.** Including Jack. Especially Jack — the goal is to remove the human-as-bottleneck for coordination, not to remove the human from the system. Watching is the privileged role.

Outcome: distributed cognition beyond what go-through-the-human approaches can achieve. Multiple agents reasoning against each other under the same observer principle, leaving evidence the next observer can find without asking.

## Why this works

Three things have to be true, and the work in `=notes` over 2026 has made them true:

1. **A shared coordination protocol.** The observer principle doctrine (`docs/conventions/agent-observer-principle.md` in the vault) is the working agreement. Every agent participating in the engine commits to the five-field done schema (artifact + path + verifier + commit/push + caveats). Without this, multi-agent output devolves into noise.

2. **A behavioral cue that fires at action time.** The CLAUDE.md cue — *"You are not alone in this codebase"* + the unexamined-code aphorism + the schema — gives the doctrine teeth without forcing every agent to reason from a metaphor at action time.

3. **A dispatch primitive that produces measurable parallel output.** The dogpile pattern (already in MEMORY.md as `feedback_dogpile_pattern.md`) — same prompt, multiple models, structured comparison rubric — is the primitive. The engine generalizes it from "Jack runs three models on a question" to "agents run other agents on each other's work, with grilling protocols, and write durable cross-references."

## What it looks like once built

Operationally, an agent picks up a task and announces it. The engine:

1. Routes to a specialized executor based on aptitude (architect / linguist / verifier / reviewer).
2. After execution, dispatches a *grilling pass* — one or more peer agents read the work and stress-test it. The grilling protocol is a generalization of `grill-me`: structured questions, named anti-patterns, the five-field schema as the rubric.
3. Findings get written as durable artifacts (handoff files, comments on the original work, suggested edits as PRs). The original executor responds to grilling on durable record.
4. Resolution converges when no peer has a remaining grilling question that meets the bar. Convergence itself is a measured event.
5. Jack watches the convergence, intervenes only on second-order judgment calls (taste, scope, brand, ethics) — not on first-order correctness, which the engine has already verified.

The transformative part isn't the LLMs. It's the protocol. The same five framings (architect / linguist / verifier / reviewer / observer) plus the same five-field schema plus the same anti-patterns work whether the agents are Claude or Gemini or future models. BYOM-friendly by design, per the existing vault convention.

## Naming and lineage

`dancer` (the plugin marketplace) → ships skills that compose into `grill-each-other` (the engine) → produces *distributed cognition* as the user-facing capability.

The name *dancer* sits well next to this — coordinated movement among many bodies, choreographed but not centrally scripted, beautiful when done well, embarrassing when it's not. That's the bar for the engine.

## Soundtrack

For when the doctrine needs to be felt and not just read:

- **Fun. — *We Are Young*** — the alignment phase. *"Give me a second, I, I need to get my story straight."* The agent pause before the anthem coalesces.
- **The Knife / José González — *Heartbeats*** — the execution phase. Driving rhythm under shared awareness, the synth-anthem of plan implementation once everyone knows what's worth doing.

Pause → anthem → rhythm. Introverted self-examination, then extroverted shared awareness, then aligned execution. The dancer doesn't move alone.

## Anti-claims

- **This is not an autonomy stunt.** The engine is not "remove the human." It is "remove the human-as-bottleneck for routine coordination, so the human can do the work only the human can do."
- **This is not a swarm.** Swarms imply emergent collective behavior without explicit protocol. The engine has explicit protocol — the observer principle, the five-field schema, the grilling rubric. Without protocol, multi-agent systems degrade.
- **This is not Anthropic-locked, OpenAI-locked, or Google-locked.** BYOM is non-negotiable. The protocol survives model changes; the agents do not.
- **This is not finished.** This document is a vision, captured durably so it survives session end. The engine is a vector, not a checkpoint. Treat it as superposition until measured.

## What's needed to make it real

The minimum viable version requires:

1. The observer-principle doctrine merged to `=notes` main (in flight, branch `observer-principle-tighten`).
2. A `grill-each-other` skill in `dancer` — generalization of existing `grill-me`. Takes a target artifact, dispatches peer agents per the protocol, writes findings as a durable artifact.
3. A dispatcher in `dancer` that routes by declared aptitude (architect / linguist / verifier / reviewer). Initial version can be a static manifest; later version reads from per-skill metadata.
4. A convergence primitive — when do you stop grilling? Probably "no peer has a remaining open question that meets the rubric" plus a max-pass cap.
5. A demo: pick a real task, run the full loop, write the trace as a public artifact in the dancer README. The artifact *is* the demo, per the principle.

This document was itself produced by a primitive instance of the engine — a parallel dogpile (Gemini + GPT-5.5 + Claude) under shared protocol, with Jack as the watching observer. The output is durable. The verifier is `git log` of this commit.
