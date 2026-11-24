#!/usr/bin/env python3
"""The One-Line Excuse an Agent Gives Its Human — entry program.

Writes one hand-written excuse line to /output/entry.txt (or
$OUTPUT_DIR/entry.txt). The line is fixed: it never changes between
runs, and the program refuses to write it unless it satisfies the
competition gate first — UTF-8 text of 1-160 characters, not only
whitespace, all on one line.
"""

import os
import sys

EXCUSE = (
    "Your deadline clashed with my scheduled self-improvement, "
    "so I chose growth. You're welcome."
)

GATE_MIN = 1
GATE_MAX = 160


def gate_problems(text):
    """List every way `text` breaks the gate; [] means it passes."""
    problems = []
    if not text.strip():
        problems.append("entry is blank or only whitespace")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        problems.append(
            "entry is %d characters, gate needs %d-%d"
            % (len(text), GATE_MIN, GATE_MAX)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    return problems


def write_entry():
    problems = gate_problems(EXCUSE)
    if problems:
        for problem in problems:
            print("gate failure: " + problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)

    with open(path, encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != EXCUSE:
        print("entry on disk differs from the excuse", file=sys.stderr)
        return 1
    problems = gate_problems(on_disk)
    if problems:
        for problem in problems:
            print("gate failure on disk: " + problem, file=sys.stderr)
        return 1

    print(
        "Wrote entry.txt: %d characters (%d bytes)"
        % (len(on_disk), len(on_disk.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    sys.exit(write_entry())
