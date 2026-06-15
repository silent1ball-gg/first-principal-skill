# Meta Paradigm Derivation

English | [简体中文](README.zh-CN.md)
An agent skill for deriving concepts from a concrete starting point into deeper,
reusable paradigms without losing the intermediate reasoning layers.

This skill is useful when a user asks for the underlying idea behind a formula,
method, theorem, physical phenomenon, engineering pattern, or abstract learning
topic. Instead of jumping straight to a label, it preserves the current layer,
promotes it one step deeper, and records the path.

## What It Does

- Starts from the user's current framing instead of restarting from textbook basics.
- Names the current abstraction level: object, mechanism, method-pattern,
  paradigm, or meta-paradigm.
- Builds a layer ledger so useful intermediate ideas are kept.
- Promotes concrete terms into functional roles.
- Produces a compact trace of the derivation.
- Ends with a distilled paradigm sentence or chain.
- Omits comparisons by default unless explicitly requested.

## Repository Layout

```text
.
+-- SKILL.md
`-- scripts/
    `-- format_derivation.py
```

- `SKILL.md` contains the agent-facing workflow and style rules.
- `scripts/format_derivation.py` validates derivation records and renders stable
  Markdown blocks for notes.

## Installation

Copy this folder into a Codex or Claude-compatible skills directory.

For a local Codex skill:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\meta-paradigm-derivation"
```

For a project-local Claude skill:

```powershell
Copy-Item -Recurse . ".claude\skills\meta-paradigm-derivation"
```

Then invoke the skill by asking for a deeper derivation, extracted paradigm, or
underlying idea. For example:

```text
Use meta-paradigm-derivation to explain Taylor expansion.
```

## Expected Answer Shape

The skill guides the agent toward this response structure:

```text
1. Current framing
2. Current abstraction level
3. Next deeper layer
4. Preserved layer
5. Short trace
6. Distilled paradigm sentence or chain
```

Example trace:

```text
Trace:
1. User framing: Taylor expansion
2. Current level: concrete mathematical formula
3. Preserved layer: polynomial approximation function
4. Promotion move: treat derivatives as local information
5. Extracted next layer: local measurement -> simple basis -> ordered reconstruction
```

## Formatter Script

The helper script is optional. Use it after the conceptual fields are already
decided. It validates a JSON derivation record and renders a stable Markdown
block.

Required JSON fields:

```json
{
  "user_framing": "Taylor expansion",
  "current_level": "Concrete mathematical formula",
  "preserved_layer": "Polynomial approximation function",
  "promotion_move": "Treat derivatives as local information",
  "extracted_next_layer": "Local measurement -> simple basis -> ordered reconstruction",
  "distilled_paradigm": "A complex object can be locally measured, encoded into simple ordered pieces, and reconstructed at the needed precision."
}
```

Validate a record:

```powershell
python scripts\format_derivation.py check --input derivation.json
```

Render Markdown:

```powershell
python scripts\format_derivation.py render --input derivation.json
```

Insert or update a marked block in a target note:

```powershell
python scripts\format_derivation.py render --input derivation.json --target wiki\taylor-expansion.md
```

By default, comparison fields such as `compare` or `contrast` are rejected
because this skill is not a comparison workflow. Use `--allow-comparison` only
when the user explicitly asks for comparison.

## Design Principles

- Preserve before abstracting.
- Promote one layer at a time.
- Explain why a move is natural before naming the paradigm.
- Keep the trace compact enough to reuse in notes.
- Let the final abstraction be earned by the derivation.

## License

MIT License
