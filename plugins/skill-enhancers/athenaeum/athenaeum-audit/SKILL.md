---
name: athenaeum-audit
category: dialectic
description: High-fidelity code audit via 13-branch anchor triangulation.
---
# Athenaeum Audit: Triangulated Verification

## 🎯 Goal
Synthesize divergent agent perspectives across 13 a-priori logic branches to identify blind spots, race conditions, and structural decay.

## 🛠 Workflow
1. **Anchor**: Map the target logic to the 13 Athenaeum branches (State, Flow, Boundary, etc.).
2. **diverge**: Spawn 3+ distinct personas (e.g., Architect, Adversary, Maintainer) to audit each branch.
3. **triangulate**: Compare findings. Where agents agree = High Confidence. Where they diverge = High Risk.
4. **reconcile**: Merge findings into the `audit-report.md` template.

## 📏 Confidence Rules
- **Confirmed**: 3/3 agents agree on the bug/feature.
- **Suspected**: 2/3 agents agree; needs manual probe.
- **Divergent**: 1/3 agent identifies a unique risk; prioritize as a 'blind spot'.

## 🤖 A2A Interop
- Use `peer-grill-with-agents` to force triangulation between sub-agents.
- Reference `grill-me-with-agents` for deep-dive anchoring on a single file.

## 🖇 Sibling Skills
- `athenaeum-sign`: Ratify the final audit.
- `athenaeum-diff`: Identify drift between audit and implementation.
