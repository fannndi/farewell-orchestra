"""
validate_output.py — Programmatic validation for LLM output.
Validates format, file:line references, and TAG usage.

Usage:
  python validate_output.py --agent researcher --output "src/auth.py:42 — [P] JWT tanpa expiry"
  python validate_output.py --agent reviewer --output "[BLOCKING] src/auth.py:42 — JWT tanpa expiry"
  python validate_output.py --agent executor --output "Done. 1 file changed. Verified: pytest pass"
"""

import json, os, re, sys
from pathlib import Path

WORKTREE = os.environ.get("WORKTREE", os.getcwd())

# Patterns
RESEARCHER_PATTERN = r"([\w./\\-]+\.\w+):(\d+) — \[([PWOE])\] (.+)"
REVIEWER_PATTERN = r"\[(BLOCKING|SHOULD|NICE|FYI)\] ([\w./\\-]+\.\w+):(\d+) — (.+)"
EXECUTOR_PATTERN = r"Done\. (\d+) file\(s\) changed\.\nVerified: (.+)"

# Uncertainty markers
UNCERTAINTY_MARKERS = [
    "I think",
    "probably",
    "maybe",
    "perhaps",
    "seems like",
    "I believe",
    "I assume",
    "I guess",
    "in my opinion",
    "sepertinya",
    "kayaknya",
    "mungkin",
    "harusnya",
    "seharusnya",
]


def validate_researcher(output: str) -> dict:
    """Validate researcher output format."""
    errors = []
    warnings = []

    # Check non-empty
    if not output.strip():
        return {"valid": False, "errors": ["Empty output"], "warnings": []}

    # Check format
    matches = re.findall(RESEARCHER_PATTERN, output)
    if not matches:
        errors.append("No valid findings found. Expected: file:line — [LEVEL] desc")

    # Check file:line exists
    for match in matches:
        fpath, line, level, desc = match
        fpath_full = Path(WORKTREE) / fpath
        if not fpath_full.exists():
            errors.append(f"File not found: {fpath}")
        else:
            try:
                total_lines = len(fpath_full.read_text(encoding="utf-8").splitlines())
                if int(line) > total_lines:
                    errors.append(f"Line {line} > total lines {total_lines} in {fpath}")
            except Exception:
                warnings.append(f"Cannot read file: {fpath}")

    # Check uncertainty markers
    for marker in UNCERTAINTY_MARKERS:
        if marker.lower() in output.lower():
            warnings.append(f"Uncertainty marker found: '{marker}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "findings_count": len(matches),
    }


def validate_reviewer(output: str) -> dict:
    """Validate reviewer output format."""
    errors = []
    warnings = []

    # Check non-empty
    if not output.strip():
        return {"valid": False, "errors": ["Empty output"], "warnings": []}

    # Check format
    matches = re.findall(REVIEWER_PATTERN, output)
    if not matches:
        errors.append("No valid findings found. Expected: [TAG] file:line — desc")

    # Check file:line exists
    for match in matches:
        tag, fpath, line, desc = match
        fpath_full = Path(WORKTREE) / fpath
        if not fpath_full.exists():
            errors.append(f"File not found: {fpath}")
        else:
            try:
                total_lines = len(fpath_full.read_text(encoding="utf-8").splitlines())
                if int(line) > total_lines:
                    errors.append(f"Line {line} > total lines {total_lines} in {fpath}")
            except Exception:
                warnings.append(f"Cannot read file: {fpath}")

    # Check BLOCKING has file:line
    blockings = re.findall(r"\[BLOCKING\].*?(?:\n|$)", output)
    for blocking in blockings:
        if not re.search(r"[\w./\\-]+\.\w+:\d+", blocking):
            errors.append(f"BLOCKING without file:line: {blocking.strip()}")

    # Check uncertainty markers
    for marker in UNCERTAINTY_MARKERS:
        if marker.lower() in output.lower():
            warnings.append(f"Uncertainty marker found: '{marker}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "findings_count": len(matches),
    }


def validate_executor(output: str) -> dict:
    """Validate executor output format."""
    errors = []
    warnings = []

    # Check non-empty
    if not output.strip():
        return {"valid": False, "errors": ["Empty output"], "warnings": []}

    # Check format
    if not re.search(r"Done\. \d+ file\(s\) changed\.", output):
        errors.append("Missing 'Done. X file(s) changed.'")

    if not re.search(r"Verified: .+", output):
        errors.append("Missing 'Verified: ...'")

    # Check for "should work"
    if "should work" in output.lower():
        errors.append("Contains 'should work' — must verify with command")

    # Check uncertainty markers
    for marker in UNCERTAINTY_MARKERS:
        if marker.lower() in output.lower():
            warnings.append(f"Uncertainty marker found: '{marker}'")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate LLM output")
    parser.add_argument(
        "--agent", required=True, choices=["researcher", "reviewer", "executor"]
    )
    parser.add_argument("--output", required=True, help="LLM output to validate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.agent == "researcher":
        result = validate_researcher(args.output)
    elif args.agent == "reviewer":
        result = validate_reviewer(args.output)
    elif args.agent == "executor":
        result = validate_executor(args.output)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"✅ VALID ({result.get('findings_count', 0)} findings)")
        else:
            print(f"❌ INVALID")
            for error in result["errors"]:
                print(f"  - {error}")

        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"  ⚠️ {warning}")


if __name__ == "__main__":
    main()
