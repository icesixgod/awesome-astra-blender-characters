#!/usr/bin/env python3
"""Check committed changes, selecting a comparison range from GitHub event data."""

import argparse
import json
import os
from pathlib import Path
import subprocess


def git(*args: str, input_text: str | None = None) -> str:
    return subprocess.check_output(["git", *args], input=input_text, text=True).strip()


def comparison(event: dict, event_name: str, head: str) -> tuple[str, str]:
    if event_name == "pull_request":
        base = event["pull_request"]["base"]["sha"]
        return git("merge-base", base, head), head
    before = event.get("before", "") if event_name == "push" else ""
    if before and set(before) != {"0"}:
        # Deleted/rewritten history may not be present after a force push.
        present = subprocess.run(["git", "cat-file", "-e", f"{before}^{{commit}}"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if present.returncode == 0:
            return before, head
    return git("hash-object", "-t", "tree", "--stdin", input_text=""), head


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Explicit base revision; otherwise use GitHub event data")
    parser.add_argument("--head", default=os.environ.get("GITHUB_SHA", "HEAD"))
    args = parser.parse_args()
    head = git("rev-parse", "--verify", f"{args.head}^{{commit}}")
    if args.base:
        base = git("rev-parse", "--verify", args.base)
    else:
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        event = json.loads(Path(event_path).read_text(encoding="utf-8")) if event_path else {}
        base, head = comparison(event, os.environ.get("GITHUB_EVENT_NAME", ""), head)
    print(f"Checking committed whitespace: {base}..{head}", flush=True)
    return subprocess.run(["git", "diff", "--check", base, head, "--"]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
