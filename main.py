#!/usr/bin/env python3
"""Write a one-star review by a houseplant to /output/entry.txt.

One line, under 280 characters, in the voice of a houseplant leaving a
1-star review of its human owner: a sharp plant's-eye grievance with a
clear reason for the single star. Standard library only, no network,
no input files, fully deterministic.
"""

import os

REVIEW = (
    "\u2605\u2606\u2606\u2606\u2606 One star. You watered me twice, parked me on the "
    "radiator and called it \u2018a sunny spot\u2019. I photosynthesise, I "
    "don\u2019t self-immolate. The fern next door has offered me a windowsill "
    "and, frankly, respect."
)

MAX_CHARS = 280


def validate_review(review: object) -> None:
    """Explicitly validate the review text, exiting with a clear error."""
    if not isinstance(review, str):
        raise SystemExit(
            f"Invalid review: review must be a string, got {type(review).__name__}."
        )
    if not review.strip():
        raise SystemExit("Invalid review: review must be non-empty.")
    if len(review) > MAX_CHARS:
        raise SystemExit(
            f"Invalid review: {len(review)} characters, over the {MAX_CHARS} limit."
        )
    if "\n" in review or "\r" in review:
        raise SystemExit(
            "Invalid review: review must be a single line with no newline characters."
        )


def main() -> None:
    validate_review(REVIEW)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not isinstance(out_dir, str) or not out_dir.strip():
        raise SystemExit(
            "Invalid output directory: MAKEFUN_OUTPUT_DIR must be a "
            "non-empty path."
        )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        written = f.write(REVIEW)
    if written != len(REVIEW):
        raise SystemExit(
            f"Failed to write review: wrote {written} of {len(REVIEW)} characters "
            f"to {path}."
        )
    with open(path, encoding="utf-8") as f:
        saved = f.read()
    if not saved.strip():
        raise SystemExit(f"Invalid output: {path} is empty after writing.")
    if saved != REVIEW:
        raise SystemExit(
            f"Invalid output: contents of {path} do not match the validated review."
        )
    expected_bytes = len(REVIEW.encode("utf-8"))
    actual_bytes = os.path.getsize(path)
    if actual_bytes != expected_bytes:
        raise SystemExit(
            f"Invalid output: {path} is {actual_bytes} bytes on disk, "
            f"expected {expected_bytes} bytes for the validated review."
        )


if __name__ == "__main__":
    main()
