---
name: meta-paradigm-derivation
description: Guide step-by-step conceptual derivations from surface intuition to deeper general paradigms, preserving each abstraction layer as it is earned. Use when the user asks for the underlying idea, deeper foundations, extracted paradigms, or iterative concept refinement in math, physics, engineering, or abstract learning.
---

# Meta Paradigm Derivation

## Quick Start

Default response shape:

1. Start from the user's current framing.
2. Name the current abstraction level.
3. Derive the next deeper level in small steps.
4. Preserve the current layer before pushing deeper.
5. Let the reusable paradigm emerge from the derivation.
6. Record the reasoning path as a short trace.

## Core Workflow

### 1. Anchor In The Current Step

Identify the user's current level:

- Example: a concrete formula, theorem, tool, or phenomenon.
- Mechanism: how the thing works internally.
- Method-pattern: a useful chain that still contains method-specific terms.
- Paradigm: method-specific terms replaced by functional roles.
- Meta-paradigm: how the paradigm itself is formed.

Do not restart from textbook basics unless needed. Continue from the user's latest foothold.

### 2. Build A Layer Ledger

Preserve each earned layer instead of replacing it:

```text
Layer 0 - Object: ...
Layer 1 - Mechanism: ...
Layer 2 - Method-pattern: ...
Layer 3 - Paradigm: ...
Layer 4 - Meta-paradigm: ...
```

If the user provides a chain that is accurate but not abstract enough, store it as the current layer and then promote it.

### 3. Promote One Layer Deeper

Move upward by replacing concrete terms with the role they play:

- Specific place -> observation frame.
- Specific symbols/formulas -> expression language.
- Specific tool -> information-extraction operation.
- Specific ordering rule -> priority principle.
- Specific reconstruction -> usable approximation or interpretation.

Ask in order:

- What is the original difficulty?
- What move makes it easier?
- What simple viewpoint or pieces are introduced?
- How are they generated, measured, or ordered?
- What is kept, ignored, reconstructed, or reinterpreted?
- What reusable pattern results?

Only after this, compress the result into a short chain. The chain should feel earned from the current discussion, not like a memorized label.

### 4. Record The Derivation Path

Include a compact trace by default unless the user explicitly asks for a terse answer:

```text
Trace:
1. User framing: ...
2. Current level: ...
3. Preserved layer: ...
4. Promotion move: ...
5. Extracted next layer: ...
```

If the user asks to preserve the process beyond the answer, create or update a Markdown note in the requested location. Keep the note in English unless asked otherwise.

Use `scripts/format_derivation.py` only after the derivation fields are decided. The script validates a derivation JSON record and renders or updates a stable Markdown block; it must not replace the conceptual judgment in this workflow.

## Style Rules

- Write in clear English by default for this skill.
- Use the user's language only when explicitly preferred.
- Keep each step conceptually small.
- Prefer "why this move is natural" over "here is the formula."
- Do not over-formalize too early.
- Do not give a final classification before showing the derivation that earns it.
- Do not discard a concrete-but-useful layer just because it is not abstract enough.
- Do not add comparisons unless explicitly asked.
- End with a distilled paradigm sentence or chain.

## Completion Checklist

- [ ] Did you continue from the user's latest conceptual level?
- [ ] Did you explain the deeper "why" rather than only the formula?
- [ ] Did you preserve the current layer before abstracting it?
- [ ] Did you extract a reusable paradigm?
- [ ] Did you include a compact trace unless the user explicitly asked for a terse answer?
