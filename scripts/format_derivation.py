#!/usr/bin/env python3
"""Validate and render meta-paradigm derivation records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "user_framing",
    "current_level",
    "preserved_layer",
    "promotion_move",
    "extracted_next_layer",
    "distilled_paradigm",
)

COMPARISON_KEYS = {"compare", "comparison", "comparisons", "contrast", "contrasts"}
PLACEHOLDERS = {"", "...", "todo", "tbd", "n/a", "na", "none", "null"}
START_MARKER = "<!-- meta-paradigm-derivation:start -->"
END_MARKER = "<!-- meta-paradigm-derivation:end -->"


def load_record(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(path).read_text(encoding="utf-8")
    raw = raw.lstrip("\ufeff")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")

    return data


def normalize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def validate_record(data: dict[str, Any], allow_comparison: bool = False) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        value = normalize_value(data.get(field))
        if value.lower() in PLACEHOLDERS:
            errors.append(f"Missing or placeholder value for '{field}'.")

    if not allow_comparison:
        present = sorted(COMPARISON_KEYS.intersection(data.keys()))
        if present:
            errors.append(
                "Comparison fields are present but this skill omits comparisons by default: "
                + ", ".join(present)
            )

    return errors


def heading_from_record(data: dict[str, Any], explicit_heading: str | None) -> str:
    heading = explicit_heading or normalize_value(data.get("title")) or normalize_value(
        data.get("user_framing")
    )
    return heading or "Derived Paradigm"


def render_markdown(data: dict[str, Any], heading: str | None = None) -> str:
    title = heading_from_record(data, heading)
    lines = [
        START_MARKER,
        f"### {title}",
        "",
        "Trace:",
        f"1. **User framing:** {normalize_value(data['user_framing'])}",
        f"2. **Current level:** {normalize_value(data['current_level'])}",
        f"3. **Preserved layer:** {normalize_value(data['preserved_layer'])}",
        f"4. **Promotion move:** {normalize_value(data['promotion_move'])}",
        f"5. **Extracted next layer:** {normalize_value(data['extracted_next_layer'])}",
        "",
        f"**Distilled paradigm:** {normalize_value(data['distilled_paradigm'])}",
        END_MARKER,
        "",
    ]
    return "\n".join(lines)


def replace_marked_block(markdown: str, block: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\n?",
        flags=re.DOTALL,
    )
    if pattern.search(markdown):
        return pattern.sub(block, markdown, count=1), True
    return markdown, False


def insert_or_update_target(path: Path, block: str, section_title: str) -> str:
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = ""

    updated, replaced = replace_marked_block(text, block)
    if replaced:
        path.write_text(ensure_final_newline(updated), encoding="utf-8")
        return "updated existing derivation block"

    section_pattern = re.compile(rf"(?m)^## {re.escape(section_title)}\s*$")
    match = section_pattern.search(text)
    if match:
        insert_at = match.end()
        updated = text[:insert_at] + "\n\n" + block + text[insert_at:]
    else:
        prefix = ensure_final_newline(text) if text else ""
        updated = prefix + f"## {section_title}\n\n" + block

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ensure_final_newline(updated), encoding="utf-8")
    return "inserted derivation block"


def ensure_final_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def command_check(args: argparse.Namespace) -> int:
    try:
        data = load_record(args.input)
        errors = validate_record(data, allow_comparison=args.allow_comparison)
    except ValueError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    print("ok")
    return 0


def command_render(args: argparse.Namespace) -> int:
    try:
        data = load_record(args.input)
        errors = validate_record(data, allow_comparison=args.allow_comparison)
    except ValueError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    block = render_markdown(data, heading=args.heading)

    if args.target:
        target = Path(args.target)
        result = insert_or_update_target(target, block, args.section_title)
        print(f"{result}: {target}")
    else:
        sys.stdout.write(block)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and render meta-paradigm derivation records."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Validate a derivation JSON record.")
    check.add_argument("--input", required=True, help="JSON file path, or '-' for stdin.")
    check.add_argument(
        "--allow-comparison",
        action="store_true",
        help="Allow comparison fields in the record.",
    )
    check.set_defaults(func=command_check)

    render = subparsers.add_parser(
        "render", help="Render a derivation JSON record as Markdown."
    )
    render.add_argument("--input", required=True, help="JSON file path, or '-' for stdin.")
    render.add_argument(
        "--target",
        help="Optional Markdown file to insert or update. Prints Markdown when omitted.",
    )
    render.add_argument("--heading", help="Override the generated Markdown heading.")
    render.add_argument(
        "--section-title",
        default="Paradigms",
        help="Target H2 section title when inserting into a Markdown file.",
    )
    render.add_argument(
        "--allow-comparison",
        action="store_true",
        help="Allow comparison fields in the record.",
    )
    render.set_defaults(func=command_render)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
