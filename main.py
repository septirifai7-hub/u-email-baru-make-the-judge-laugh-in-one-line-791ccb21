#!/usr/bin/env python3
"""Entry for make.fun bounty "Make the Judge Laugh in One Line".

One funny line on any topic. This program writes exactly that
one line, 1 to 200 characters, as UTF-8 text to entry.txt in the
output directory, with no trailing newline. The judge compares
it pairwise against the other entries, weighing first whether a
stranger gets the joke in one read, then surprise, then
tightness, then freshness, then whether it reads cleanly aloud.
The line needs no shared knowledge: anyone who has sat through
a dull meeting or a long review recognises the feeling at once,
and the doctor's deadpan delivery sells it.

The joke sets up a familiar scene — a patient asking a doctor
for sleep help — and breaks it with an unexpected prescription:
the speaker's own code reviews, so boring they work faster than
any medicine. The punch lands on the last words, "under four
minutes", which turns a vague complaint into a measured dose.
The program holds the line as a constant, checks it against the
gate before writing anything, and writes it byte-for-byte. If
the line ever drifted outside the gate, it fails loudly instead
of producing an invalid entry. The output directory defaults to
/output and can be overridden with MAKEFUN_OUTPUT_DIR, which is
how the grading sandbox points the program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = "I asked my doctor for something to help me sleep and he prescribed my own code reviews, which knock me out in under four minutes."

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the gate: 1-200 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\t" in text:
        raise ValueError("entry must not contain tab characters")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")
    # The grader collects the output as another user, so the file
    # must stay readable by everyone, not just its owner.
    target.chmod(0o644)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
